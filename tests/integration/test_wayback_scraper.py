from __future__ import annotations

import gzip
import io
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from types import TracebackType

import pytest

from college_majors.domain import salaries as col
from college_majors.infrastructure import wayback_scraper as ws
from college_majors.infrastructure.csv_repository import read_payscale_majors

# (rank, major, degree type, early pay text, mid pay text, meaning text)
Row = tuple[int, str, str, str, str, str]


def _page(rows: list[Row]) -> str:
    """Markup shaped like the real report: a desktop cell per value and a repeating mobile table."""
    body = ""
    for rank, major, degree, early, mid, meaning in rows:
        cells = "".join(
            f'<td class="pxl-hidden-sm-down text-center"><span>{text}</span></td>'
            for text in (rank, f'<a href="/x">{major}</a>', degree, early, mid, meaning)
        )
        mobile = (
            '<td class="pxl-hidden-md-up"><table class="mobileRoiTable"><tbody><tr>'
            f'<td class="small header">Early Career Pay</td><td><span>{early}</span></td>'
            "</tr></tbody></table></td>"
        )
        body += f'<tr id="row-{rank}">{cells}{mobile}</tr>'
    return f"<table><thead><tr><th>Rank</th></tr></thead><tbody>{body}</tbody></table>"


def _data_table_page(rows: list[Row]) -> str:
    """Markup of the newer report: a data-table row whose cells hold title and value spans."""
    body = ""
    for rank, major, degree, early, mid, meaning in rows:
        values = (rank, major, degree, early, mid, meaning)
        cells = "".join(
            f'<td class="data-table__cell csr-col--{name} ">'
            f'<span class="data-table__title">{name}<!-- -->:</span>'
            f'<span class="data-table__value">{value}</span></td>'
            for name, value in zip(
                ("rank", "major", "type", "early", "mid", "meaning"), values, strict=True
            )
        )
        body += f'<tr class="data-table__row">{cells}</tr>'
    return f'<table><tbody><tr class="other"><td>x</td></tr>{body}</tbody></table>'


def _rows(first: int, last: int) -> list[Row]:
    return [
        (n, f"Major {n}", "Bachelor&#x27;s", "$50,000", "$100,000", "40%")
        for n in range(first, last + 1)
    ]


def _url(timestamp: str) -> str:
    return f"http://web.archive.org/web/{timestamp}id_/https://www.payscale.com/x"


def test_parse_page_reads_rank_major_pays_and_meaning_from_the_desktop_table() -> None:
    html = _page([(1, "Petroleum Engineering", "Bachelor&#x27;s", "$94,500", "$176,900", "72%")])

    assert ws.parse_page(html) == [
        ws.MajorPay(1, "Petroleum Engineering", "Bachelor's", 94500, 176900, 72)
    ]


def test_parse_page_gives_none_for_a_missing_percentage() -> None:
    html = _page([(2, "Physics", "Bachelor&#x27;s", "$60,000", "$110,000", "")])

    assert ws.parse_page(html)[0].high_meaning_pct is None


def test_parse_page_accepts_a_row_without_the_percentage_cell() -> None:
    html = (
        '<tr id="row-3">'
        + "".join(
            f'<td class="pxl-hidden-sm-down"><span>{t}</span></td>'
            for t in ("3", "Law", "Bachelor&#x27;s", "$1,000", "$2,000")
        )
        + "</tr>"
    )

    assert ws.parse_page(html) == [ws.MajorPay(3, "Law", "Bachelor's", 1000, 2000, None)]


def test_parse_page_ignores_the_mobile_tables_and_other_degree_types() -> None:
    html = _page(
        [
            (1, "Keep", "Bachelor&#x27;s", "$1,000", "$2,000", "1%"),
            (2, "Drop", "Master&#x27;s", "$1,000", "$2,000", "1%"),
        ]
    )

    assert [row.major for row in ws.parse_page(html)] == ["Keep"]


def test_parse_page_skips_short_rows_and_rows_with_unreadable_pay() -> None:
    short = '<tr id="row-1"><td class="pxl-hidden-sm-down">1</td></tr>'
    bad_pay = _page([(2, "Odd", "Bachelor&#x27;s", "n/a", "$2,000", "")])

    assert ws.parse_page(short + bad_pay) == []


def test_parse_page_reads_the_newer_data_table_markup() -> None:
    html = _data_table_page(
        [
            (26, "Petroleum Geology", "Bachelors", "$60,100", "$122,900", "-"),
            (27, "Nuclear Engineering", "Bachelors", "$72,400", "$122,200", "44%"),
        ]
    )

    assert ws.parse_page(html) == [
        ws.MajorPay(26, "Petroleum Geology", "Bachelor's", 60100, 122900, None),
        ws.MajorPay(27, "Nuclear Engineering", "Bachelor's", 72400, 122200, 44),
    ]


def test_parse_page_keeps_only_bachelors_in_the_newer_markup() -> None:
    html = _data_table_page(
        [
            (1, "Keep", "Bachelors", "$1,000", "$2,000", "1%"),
            (2, "Drop", "Masters", "$1,000", "$2,000", "1%"),
        ]
    )

    assert [row.major for row in ws.parse_page(html)] == ["Keep"]


def test_parse_page_ignores_cells_outside_a_data_row_and_a_row_with_short_data() -> None:
    html = (
        '<td class="data-table__cell csr-col--rank"><span class="data-table__value">9</span></td>'
        '<tr class="data-table__row"><td class="data-table__cell csr-col--rank">'
        '<span class="data-table__value">1</span></td><td>no class</td></tr>'
    )

    assert ws.parse_page(html) == []


def test_parse_page_returns_nothing_for_markup_without_rows() -> None:
    assert ws.parse_page("<html><body>No data</body></html>") == []


def test_capture_timestamp_reads_the_digits_from_a_wayback_url() -> None:
    assert ws.capture_timestamp(_url("20200214154915")) == "20200214154915"


def test_capture_timestamp_rejects_a_url_without_one() -> None:
    with pytest.raises(ws.WaybackError, match="no capture timestamp"):
        ws.capture_timestamp("https://example.org/")


class _FakeResponse:
    def __init__(self, url: str, body: bytes) -> None:
        self._url, self._body = url, body

    def __enter__(self) -> _FakeResponse:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        return None

    def geturl(self) -> str:
        return self._url

    def read(self) -> bytes:
        return self._body


def test_http_get_sends_the_generic_user_agent_and_a_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    def fake_urlopen(request: urllib.request.Request, timeout: float) -> _FakeResponse:
        captured["agent"] = request.get_header("User-agent")
        captured["timeout"] = timeout
        return _FakeResponse("http://final", b"body")

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

    assert ws._http_get("http://start") == ("http://final", b"body")
    assert captured == {"agent": "college-majors-learning-project", "timeout": ws.TIMEOUT_SECONDS}


def _raising(error: Exception) -> object:
    def fake_urlopen(request: urllib.request.Request, timeout: float) -> _FakeResponse:
        raise error

    return fake_urlopen


def _http_error(code: int) -> urllib.error.HTTPError:
    return urllib.error.HTTPError("http://x", code, "msg", {}, io.BytesIO(b""))  # type: ignore[arg-type]


def test_http_get_maps_404_to_page_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(urllib.request, "urlopen", _raising(_http_error(404)))

    with pytest.raises(ws.PageNotFoundError):
        ws._http_get("http://x")


def test_http_get_maps_other_http_errors_to_wayback_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(urllib.request, "urlopen", _raising(_http_error(503)))

    with pytest.raises(ws.TransientWaybackError, match="HTTP 503"):
        ws._http_get("http://x")


def test_http_get_does_not_treat_other_client_errors_as_transient(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(urllib.request, "urlopen", _raising(_http_error(403)))

    with pytest.raises(ws.WaybackError, match="HTTP 403") as info:
        ws._http_get("http://x")

    assert not isinstance(info.value, ws.TransientWaybackError | ws.PageNotFoundError)


def test_http_get_maps_network_errors_and_keeps_the_cause(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(urllib.request, "urlopen", _raising(urllib.error.URLError("down")))

    with pytest.raises(ws.TransientWaybackError, match="could not reach") as info:
        ws._http_get("http://x")

    assert isinstance(info.value.__cause__, urllib.error.URLError)


_ARCHIVE = "http://web.archive.org/web/"
_DAY = "20200214"


def _stamp(page: int, day: str = _DAY) -> str:
    return f"{day}{page:06d}"


class _FakeArchive:
    """A fake CDX index and replay server; it records requests and the pauses between them."""

    def __init__(self, pages: dict[int, str], stamps: dict[int, list[str]] | None = None) -> None:
        self.pages = pages
        self.stamps = stamps or {page: [_stamp(page)] for page in pages}
        self.base_only = False  # page 1 has captures only under the base report URL
        self.raw_redirects: dict[int, str] = {}  # id_ replay answers with another timestamp
        self.never_replays: dict[int, str] = {}  # no form replays the exact capture
        self.urls: list[str] = []
        self.pauses: list[float] = []

    def opener(self, url: str) -> tuple[str, bytes]:
        self.urls.append(url)
        if "/cdx/search/cdx" in url:
            return url, self._cdx(url)
        return self._replay(url)

    def _page_of(self, original: str) -> int:
        return 1 if original.endswith("bachelors") else int(original.rsplit("/", 1)[1])

    def _cdx(self, url: str) -> bytes:
        query = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        original = query["url"][0]
        page = self._page_of(original)
        if page == 1 and self.base_only != original.endswith("bachelors"):
            return b""
        first, last = query["from"][0], query["to"][0]
        stamps = [s for s in self.stamps.get(page, []) if first <= s[:8] <= last]
        return "".join(f"{stamp}\n" for stamp in stamps).encode()

    def _replay(self, url: str) -> tuple[str, bytes]:
        stamp, original = url.removeprefix(_ARCHIVE).split("/", 1)
        raw = stamp.endswith("id_")
        stamp = stamp.removesuffix("id_")
        page = self._page_of(original)
        if page not in self.pages:
            raise ws.PageNotFoundError(url)
        served = stamp
        if page in self.never_replays or (raw and page in self.raw_redirects):
            served = self.never_replays.get(page) or self.raw_redirects[page]
        return f"{_ARCHIVE}{served}{'id_' if raw else ''}/{original}", self.pages[page].encode()


def _scrape(archive: _FakeArchive, **kwargs: int) -> ws.ScrapeResult:
    return ws.scrape(_DAY, opener=archive.opener, sleep=archive.pauses.append, **kwargs)


def test_resolve_capture_returns_the_nearest_capture_inside_the_window() -> None:
    stamps = {2: ["20200101000000", "20200210000000", "20200301000000"]}
    archive = _FakeArchive({2: _page(_rows(1, 1))}, stamps)

    capture = ws.resolve_capture(2, _DAY, 60, archive.opener)

    assert capture == ws.Capture("20200210000000", f"{ws.REPORT_URL}/page/2")
    assert "from=20191216&to=20200414" in archive.urls[0]
    assert "filter=statuscode:200" in archive.urls[0]
    assert "collapse=timestamp:8" in archive.urls[0]


def test_resolve_capture_ignores_captures_outside_the_window() -> None:
    archive = _FakeArchive({2: _page(_rows(1, 1))}, {2: ["20190101000000", "20201231000000"]})

    assert ws.resolve_capture(2, _DAY, 60, archive.opener) is None


def test_resolve_capture_prefers_the_earlier_capture_on_a_tie() -> None:
    archive = _FakeArchive({2: _page(_rows(1, 1))}, {2: ["20200216000000", "20200212000000"]})

    capture = ws.resolve_capture(2, _DAY, 60, archive.opener)

    assert capture is not None
    assert capture.timestamp == "20200212000000"


def test_resolve_capture_falls_back_to_the_base_url_for_page_one() -> None:
    archive = _FakeArchive({1: _page(_rows(1, 1))})
    archive.base_only = True

    capture = ws.resolve_capture(1, _DAY, 60, archive.opener)

    assert capture == ws.Capture(_stamp(1), ws.REPORT_URL)


def test_resolve_capture_does_not_fall_back_for_later_pages() -> None:
    archive = _FakeArchive({2: _page(_rows(1, 1))})
    archive.base_only = True

    assert ws.resolve_capture(3, _DAY, 60, archive.opener) is None
    assert len(archive.urls) == 1


def test_resolve_capture_rejects_an_unexpected_cdx_answer() -> None:
    with pytest.raises(ws.WaybackError, match="unexpected answer"):
        ws.resolve_capture(1, _DAY, 60, lambda url: (url, b"<html>error</html>"))


def test_resolve_capture_unzips_a_gzip_answer() -> None:
    body = gzip.compress(b"20200214123456\n")

    capture = ws.resolve_capture(2, _DAY, 60, lambda url: (url, body))

    assert capture is not None
    assert capture.timestamp == "20200214123456"


def test_fetch_capture_asks_for_the_exact_timestamp_in_raw_form() -> None:
    archive = _FakeArchive({2: _page(_rows(1, 1))})
    capture = ws.Capture(_stamp(2), f"{ws.REPORT_URL}/page/2")

    fetched = ws.fetch_capture(capture, 2, archive.opener)

    assert archive.urls == [f"{_ARCHIVE}{_stamp(2)}id_/{ws.REPORT_URL}/page/2"]
    assert "Major 1" in fetched.html


def test_fetch_capture_uses_the_rewritten_form_when_the_raw_form_is_redirected() -> None:
    archive = _FakeArchive({2: _page(_rows(1, 1))})
    archive.raw_redirects[2] = "20190923000000"
    capture = ws.Capture(_stamp(2), f"{ws.REPORT_URL}/page/2")

    fetched = ws.fetch_capture(capture, 2, archive.opener)

    assert ws.capture_timestamp(fetched.url) == _stamp(2)
    assert len(archive.urls) == 2


def test_fetch_capture_refuses_a_capture_that_no_form_replays() -> None:
    archive = _FakeArchive({2: _page(_rows(1, 1))})
    archive.never_replays[2] = "20190923000000"
    capture = ws.Capture(_stamp(2), f"{ws.REPORT_URL}/page/2")

    with pytest.raises(ws.WaybackError, match=f"does not replay capture {_stamp(2)}"):
        ws.fetch_capture(capture, 2, archive.opener)


def test_fetch_capture_reports_a_broken_gzip_body() -> None:
    capture = ws.Capture(_stamp(1), ws.REPORT_URL)
    served = f"{_ARCHIVE}{_stamp(1)}id_/x"

    with pytest.raises(ws.WaybackError, match="not valid gzip"):
        ws.fetch_capture(capture, 1, lambda url: (served, b"\x1f\x8bnot gzip"))


def test_scrape_collects_pages_until_one_has_no_capture_and_pauses_between_requests() -> None:
    archive = _FakeArchive({1: _page(_rows(1, 2)), 2: _page(_rows(3, 4))})

    result = _scrape(archive, max_pages=10)

    assert [row.rank for row in result.rows] == [1, 2, 3, 4]
    assert result.snapshot == "2020-02-14"
    assert result.page_captures == (_stamp(1), _stamp(2))
    # CDX + replay for pages 1 and 2, then one CDX request that finds nothing for page 3
    assert len(archive.urls) == 5
    assert archive.pauses == [2.0] * 4


def test_scrape_stops_at_an_empty_page() -> None:
    archive = _FakeArchive({1: _page(_rows(1, 2)), 2: _page([])})

    assert len(_scrape(archive).rows) == 2


def test_scrape_stops_when_the_replay_of_a_later_page_is_a_404() -> None:
    archive = _FakeArchive({1: _page(_rows(1, 2)), 2: _page(_rows(3, 3))})
    original_opener = archive.opener

    def opener(url: str) -> tuple[str, bytes]:
        if "page/2" in url and "/cdx/" not in url:
            raise ws.PageNotFoundError(url)
        return original_opener(url)

    result = ws.scrape(_DAY, opener=opener, sleep=archive.pauses.append)

    assert len(result.rows) == 2


def test_scrape_uses_the_base_url_when_page_one_only_has_that_capture() -> None:
    archive = _FakeArchive({1: _page(_rows(1, 2))})
    archive.base_only = True

    assert len(_scrape(archive).rows) == 2


def test_scrape_fails_when_page_one_has_no_capture_in_the_window() -> None:
    with pytest.raises(ws.PageNotFoundError, match="no capture of page 1"):
        _scrape(_FakeArchive({}))


def test_scrape_fails_when_the_replay_of_page_one_is_a_404() -> None:
    def opener(url: str) -> tuple[str, bytes]:
        if "/cdx/" in url:
            return url, b"20200214000001\n"
        raise ws.PageNotFoundError(url)

    with pytest.raises(ws.PageNotFoundError):
        ws.scrape(_DAY, opener=opener, sleep=lambda _: None)


def test_scrape_stops_when_a_page_repeats_earlier_ranks() -> None:
    archive = _FakeArchive({1: _page(_rows(1, 2)), 2: _page(_rows(1, 2)), 3: _page(_rows(3, 4))})

    assert [row.rank for row in _scrape(archive).rows] == [1, 2]


def test_scrape_stops_at_max_pages() -> None:
    archive = _FakeArchive({n: _page(_rows(n, n)) for n in range(1, 6)})

    assert len(_scrape(archive, max_pages=3).rows) == 3


def test_scrape_accepts_tied_ranks_inside_and_across_pages() -> None:
    tied = [
        (1, "A", "Bachelor&#x27;s", "$1", "$9", ""),
        (2, "B", "Bachelor&#x27;s", "$1", "$8", ""),
    ]
    more = [
        (2, "C", "Bachelor&#x27;s", "$1", "$8", ""),
        (4, "D", "Bachelor&#x27;s", "$1", "$7", ""),
    ]
    archive = _FakeArchive({1: _page(tied), 2: _page(more)})

    assert [row.rank for row in _scrape(archive).rows] == [1, 2, 2, 4]


def test_scrape_refuses_a_gap_in_the_ranks_between_pages() -> None:
    archive = _FakeArchive({1: _page(_rows(1, 25)), 2: _page(_rows(27, 30))})

    with pytest.raises(ws.WaybackError, match="rank 27 follows rank 25 after 25 rows"):
        _scrape(archive)


def test_scrape_continues_the_ranks_across_the_markup_change() -> None:
    old = _page(_rows(1, 25))
    new = _data_table_page(
        [(n, f"Major {n}", "Bachelors", "$1,000", "$2,000", "-") for n in range(26, 29)]
    )
    archive = _FakeArchive({1: old, 2: new})

    result = _scrape(archive)

    assert [row.rank for row in result.rows][-4:] == [25, 26, 27, 28]


def test_scrape_reports_the_range_when_captures_lie_within_the_window() -> None:
    stamps = {1: ["20200101000000"], 2: ["20200214000000"]}
    archive = _FakeArchive({1: _page(_rows(1, 1)), 2: _page(_rows(2, 2))}, stamps)

    result = _scrape(archive)

    assert result.snapshot == "2020-01-01..2020-02-14"


def test_scrape_refuses_captures_spread_over_more_than_the_window() -> None:
    stamps = {1: ["20191220000000"], 2: ["20200410000000"]}
    archive = _FakeArchive({1: _page(_rows(1, 1)), 2: _page(_rows(2, 2))}, stamps)

    with pytest.raises(ws.WaybackError, match="more than 60 days"):
        _scrape(archive)


def test_scrape_window_is_a_parameter() -> None:
    stamps = {1: ["20190601000000"], 2: ["20200214000000"]}
    archive = _FakeArchive({1: _page(_rows(1, 1)), 2: _page(_rows(2, 2))}, stamps)

    assert len(_scrape(archive, max_spread_days=400).rows) == 2


def test_scrape_repeats_a_request_after_a_transient_failure_with_a_longer_pause() -> None:
    archive = _FakeArchive({1: _page(_rows(1, 2))})
    original_opener = archive.opener
    failures = [ws.TransientWaybackError("timeout")]

    def flaky(url: str) -> tuple[str, bytes]:
        if failures:
            raise failures.pop()
        return original_opener(url)

    result = ws.scrape(_DAY, opener=flaky, sleep=archive.pauses.append)

    assert len(result.rows) == 2
    assert archive.pauses[0] == 4.0  # the second attempt of the first request waits twice the delay


def test_scrape_gives_up_after_the_last_retry() -> None:
    calls: list[str] = []

    def always_failing(url: str) -> tuple[str, bytes]:
        calls.append(url)
        raise ws.TransientWaybackError("down")

    with pytest.raises(ws.TransientWaybackError):
        ws.scrape(_DAY, opener=always_failing, sleep=lambda _: None)

    assert len(calls) == ws.DEFAULT_RETRIES + 1


def test_write_csv_and_read_payscale_majors_round_trip(tmp_path: Path) -> None:
    rows = [
        ws.MajorPay(1, "Finance, Applied", "Bachelor's", 61000, 120000, 40),
        ws.MajorPay(2, "Physics", "Bachelor's", 60000, 110000, None),
    ]
    path = tmp_path / "out.csv"

    ws.write_csv(rows, path, "2019-02-22")
    frame = read_payscale_majors(path)

    assert list(frame.columns) == list(ws.CSV_HEADER)
    assert frame[col.MAJOR].tolist() == ["Finance, Applied", "Physics"]
    assert frame[col.EARLY_CAREER].tolist() == [61000, 60000]
    assert frame[col.HIGH_MEANING].isna().tolist() == [False, True]
    assert set(frame[col.SNAPSHOT]) == {"2019-02-22"}
    assert b"\r" not in path.read_bytes()


def test_packaged_payscale_csv_holds_at_least_100_majors() -> None:
    frame = read_payscale_majors()

    assert len(frame) >= 100
    assert set(frame[col.DEGREE_TYPE]) == {col.BACHELORS}
