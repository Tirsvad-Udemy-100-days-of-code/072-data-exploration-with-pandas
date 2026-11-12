"""Scrapes the archived PayScale college salary report from the Wayback Machine.

Standard library only. Politeness: one request per page, a pause between pages, a generic
User-Agent and a timeout.
"""

from __future__ import annotations

import csv
import gzip
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from html.parser import HTMLParser
from pathlib import Path

from college_majors.domain import salaries as col

USER_AGENT = "college-majors-learning-project"
REPORT_URL = "https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors"
# The raw form ("id_") is tried first; some captures only replay in the rewritten form.
WAYBACK_URLS = (
    "http://web.archive.org/web/{timestamp}id_/{url}",
    "http://web.archive.org/web/{timestamp}/{url}",
)
CDX_URL = (
    "http://web.archive.org/cdx/search/cdx?url={url}&output=txt&filter=statuscode:200"
    "&from={first}&to={last}&fl=timestamp&collapse=timestamp:8"
)
TIMEOUT_SECONDS = 60.0
DEFAULT_DELAY_SECONDS = 2.0
DEFAULT_MAX_PAGES = 60
DEFAULT_MAX_SPREAD_DAYS = 60
DEFAULT_RETRIES = 2
CSV_HEADER = (
    col.RANK,
    col.MAJOR,
    col.DEGREE_TYPE,
    col.EARLY_CAREER,
    col.MID_CAREER_NOW,
    col.HIGH_MEANING,
    col.SNAPSHOT,
)

_GZIP_MAGIC = b"\x1f\x8b"
_TIMESTAMP_LENGTH = 14
_DAY_FORMAT = "%Y%m%d"
_CAPTURE_PATTERN = re.compile(r"/web/(\d{14})")
_DESKTOP_CELL_CLASS = "pxl-hidden-sm-down"
_ROW_CLASS = "data-table__row"
_CELL_CLASS = "csr-col--"
_VALUE_CLASS = "data-table__value"
_MIN_CELLS = 5
_NOT_FOUND = 404
_SERVER_ERROR = 500


class WaybackError(Exception):
    """The Wayback Machine could not deliver a page."""


class TransientWaybackError(WaybackError):
    """A timeout, a dropped connection or a server error; the request may work when repeated."""


class PageNotFoundError(WaybackError):
    """The archive has no capture of the requested page."""


@dataclass(frozen=True, slots=True)
class MajorPay:
    """One row of the PayScale report: a major and its pay."""

    rank: int
    major: str
    degree_type: str
    early_career_pay: int
    mid_career_pay: int
    high_meaning_pct: int | None


@dataclass(frozen=True, slots=True)
class FetchedPage:
    """The text of a page and the URL the archive finally served it from."""

    url: str
    html: str


@dataclass(frozen=True, slots=True)
class ScrapeResult:
    """The rows of all pages and their capture date, or "first..last" when the pages differ."""

    rows: list[MajorPay]
    snapshot: str
    page_captures: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Capture:
    """One archived copy: its 14 digit timestamp and the original URL it was taken from."""

    timestamp: str
    url: str


Opener = Callable[[str], tuple[str, bytes]]


class _ReportParser(HTMLParser):
    """Collects the cells of the desktop table; the small mobile tables repeat them."""

    def __init__(self) -> None:
        super().__init__()
        self.rows: list[list[str]] = []
        self._cell: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "tr" and (values.get("id") or "").startswith("row-"):
            self.rows.append([])
        elif tag == "td" and self.rows and _DESKTOP_CELL_CLASS in (values.get("class") or ""):
            self._cell = []

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            self._cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "td" and self._cell is not None:
            self.rows[-1].append(" ".join("".join(self._cell).split()))
            self._cell = None


class _DataTableParser(HTMLParser):
    """Collects the cells of the newer markup, where each value sits in a data-table__value span."""

    def __init__(self) -> None:
        super().__init__()
        self.rows: list[list[str]] = []
        self._in_cell = False
        self._value: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes = (dict(attrs).get("class") or "").split()
        if tag == "tr" and _ROW_CLASS in classes:
            self.rows.append([])
        elif tag == "td" and self.rows and any(c.startswith(_CELL_CLASS) for c in classes):
            self._in_cell = True
        elif tag == "span" and self._in_cell and _VALUE_CLASS in classes:
            self._value = []

    def handle_data(self, data: str) -> None:
        if self._value is not None:
            self._value.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "span" and self._value is not None:
            self.rows[-1].append(" ".join("".join(self._value).split()))
            self._value = None
        elif tag == "td":
            self._in_cell = False


def _parse_int(text: str) -> int | None:
    digits = re.sub(r"[^\d]", "", text)
    return int(digits) if digits else None


def _degree_type(text: str) -> str:
    """Read "Bachelors" and "Bachelor's" as the same degree."""
    return col.BACHELORS if text.replace("'", "") == "Bachelors" else text


def _to_major_pay(cells: list[str]) -> MajorPay | None:
    if len(cells) < _MIN_CELLS:
        return None
    rank, early, mid = _parse_int(cells[0]), _parse_int(cells[3]), _parse_int(cells[4])
    if rank is None or early is None or mid is None:
        return None
    meaning = _parse_int(cells[5]) if len(cells) > _MIN_CELLS else None
    return MajorPay(rank, cells[1], _degree_type(cells[2]), early, mid, meaning)


def parse_page(html: str) -> list[MajorPay]:
    """Return the Bachelor's rows of one report page; rows that do not parse are skipped.

    The two markups the archive holds (the 2019 table and the newer data table) are told apart by
    what the page contains.
    """
    parser = _DataTableParser() if _ROW_CLASS in html else _ReportParser()
    parser.feed(html)
    parser.close()
    parsed = (_to_major_pay(cells) for cells in parser.rows)
    return [row for row in parsed if row is not None and row.degree_type == col.BACHELORS]


def capture_timestamp(url: str) -> str:
    """Return the 14 digit capture timestamp in a Wayback URL."""
    match = _CAPTURE_PATTERN.search(url)
    if match is None:
        msg = f"no capture timestamp in {url!r}"
        raise WaybackError(msg)
    return match.group(1)


def _http_get(url: str) -> tuple[str, bytes]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})  # noqa: S310
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:  # noqa: S310
            return response.geturl(), response.read()
    except urllib.error.HTTPError as error:
        if error.code == _NOT_FOUND:
            msg = f"no capture for {url}"
            raise PageNotFoundError(msg) from error
        msg = f"the archive answered HTTP {error.code} for {url}"
        if error.code >= _SERVER_ERROR:
            raise TransientWaybackError(msg) from error
        raise WaybackError(msg) from error
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        msg = f"could not reach the archive for {url}: {error}"
        raise TransientWaybackError(msg) from error


def _decode(body: bytes, what: str) -> str:
    if body.startswith(_GZIP_MAGIC):
        try:
            body = gzip.decompress(body)
        except (OSError, EOFError) as error:
            msg = f"{what} is not valid gzip"
            raise WaybackError(msg) from error
    return body.decode("utf-8", errors="replace")


def _page_urls(page: int) -> list[str]:
    """Return the original URLs that can hold a page; page 1 is also the base report URL."""
    urls = [f"{REPORT_URL}/page/{page}"]
    return [*urls, REPORT_URL] if page == 1 else urls


def _lookup_timestamps(url: str, target: date, window_days: int, opener: Opener) -> list[str]:
    """Ask the CDX index for the successful captures of the URL near the target day."""
    reach = timedelta(days=window_days)
    query = CDX_URL.format(
        url=urllib.parse.quote(url, safe=""),
        first=(target - reach).strftime(_DAY_FORMAT),
        last=(target + reach).strftime(_DAY_FORMAT),
    )
    _, body = opener(query)
    stamps = _decode(body, "the CDX answer").split()
    for stamp in stamps:
        if not (stamp.isdigit() and len(stamp) == _TIMESTAMP_LENGTH):
            msg = f"unexpected answer from the CDX index: {stamp!r}"
            raise WaybackError(msg)
    return stamps


def resolve_capture(
    page: int, day: str, window_days: int = DEFAULT_MAX_SPREAD_DAYS, opener: Opener = _http_get
) -> Capture | None:
    """Find the capture of a page nearest to the day (YYYYMMDD) within the window, or None."""
    target = datetime.strptime(day, _DAY_FORMAT).date()  # noqa: DTZ007
    for url in _page_urls(page):
        stamps = _lookup_timestamps(url, target, window_days, opener)
        if stamps:
            nearest = min(stamps, key=lambda stamp: (abs(_capture_day(stamp) - target), stamp))
            return Capture(nearest, url)
    return None


def fetch_capture(capture: Capture, page: int, opener: Opener = _http_get) -> FetchedPage:
    """Fetch the page text of one exact capture; a replay of another capture is refused."""
    for template in WAYBACK_URLS:
        final_url, body = opener(template.format(timestamp=capture.timestamp, url=capture.url))
        if capture_timestamp(final_url) == capture.timestamp:
            return FetchedPage(final_url, _decode(body, f"page {page}"))
    msg = f"the archive does not replay capture {capture.timestamp} of page {page}"
    raise WaybackError(msg)


def _capture_day(timestamp: str) -> date:
    return datetime.strptime(timestamp[:8], _DAY_FORMAT).date()  # noqa: DTZ007


def _snapshot(days: list[date]) -> str:
    first, last = min(days), max(days)
    return first.isoformat() if first == last else f"{first.isoformat()}..{last.isoformat()}"


def _paced(opener: Opener, delay: float, sleep: Callable[[float], None]) -> Opener:
    """Wrap the opener: wait delay seconds before every request after the first.

    A transient failure is repeated up to DEFAULT_RETRIES times, waiting longer each time.
    """
    requests = 0

    def once(url: str, attempt: int) -> tuple[str, bytes]:
        nonlocal requests
        if requests:
            sleep(delay * (attempt + 1))
        requests += 1
        return opener(url)

    def paced(url: str) -> tuple[str, bytes]:
        for attempt in range(DEFAULT_RETRIES):
            try:
                return once(url, attempt)
            except TransientWaybackError:
                continue
        return once(url, DEFAULT_RETRIES)

    return paced


def _check_ranks(known: list[MajorPay], page_rows: list[MajorPay], page: int) -> None:
    """Require the ranks to run on from the earlier pages: a tie repeats, else rank = row number."""
    previous = known[-1].rank if known else 0
    count = len(known)
    for row in page_rows:
        if row.rank != previous and row.rank != count + 1:
            msg = f"page {page}: rank {row.rank} follows rank {previous} after {count} rows"
            raise WaybackError(msg)
        previous = row.rank
        count += 1


def scrape(
    day: str,
    max_pages: int = DEFAULT_MAX_PAGES,
    delay: float = DEFAULT_DELAY_SECONDS,
    opener: Opener = _http_get,
    sleep: Callable[[float], None] = time.sleep,
    max_spread_days: int = DEFAULT_MAX_SPREAD_DAYS,
) -> ScrapeResult:
    """Fetch page 1, 2, ... using for each page the capture nearest to the day (YYYYMMDD).

    The nearest capture within max_spread_days is looked up in the CDX index and fetched by its
    exact timestamp, so the archive never substitutes another one. The captures used must lie
    within max_spread_days of each other and the ranks must run on across pages, otherwise
    WaybackError is raised. The scrape ends at a page with no capture, a 404, an empty page or a
    page that repeats earlier ranks.
    """
    paced = _paced(opener, delay, sleep)
    rows: list[MajorPay] = []
    stamps: list[str] = []
    for page in range(1, max_pages + 1):
        capture = resolve_capture(page, day, max_spread_days, paced)
        if capture is None:
            if page == 1:
                msg = f"the archive has no capture of page 1 within {max_spread_days} days of {day}"
                raise PageNotFoundError(msg)
            break
        try:
            fetched = fetch_capture(capture, page, paced)
        except PageNotFoundError:
            if page == 1:
                raise
            break
        page_rows = parse_page(fetched.html)
        if not page_rows or (rows and page_rows[0].rank < rows[-1].rank):
            break
        _check_ranks(rows, page_rows, page)
        stamps.append(capture.timestamp)
        days = [_capture_day(stamp) for stamp in stamps]
        if (max(days) - min(days)).days > max_spread_days:
            msg = f"captures span more than {max_spread_days} days: {_snapshot(days)} (page {page})"
            raise WaybackError(msg)
        rows.extend(page_rows)
    return ScrapeResult(rows, _snapshot([_capture_day(s) for s in stamps]), tuple(stamps))


def write_csv(rows: list[MajorPay], path: Path, snapshot: str) -> None:
    """Write the rows to a CSV file with LF line ends, tagging each with the snapshot date."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(CSV_HEADER)
        for row in rows:
            meaning = "" if row.high_meaning_pct is None else row.high_meaning_pct
            writer.writerow(
                [
                    row.rank,
                    row.major,
                    row.degree_type,
                    row.early_career_pay,
                    row.mid_career_pay,
                    meaning,
                    snapshot,
                ]
            )
