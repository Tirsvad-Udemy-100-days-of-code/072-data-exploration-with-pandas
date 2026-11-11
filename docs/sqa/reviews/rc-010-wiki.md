# Review of the wiki

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-010 |
| CrossReference | [WIKI-001], [QC-WIKI-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-11 | Deprecated | Jens Tirsvad Nielsen | AI as stand-in for S02 | Initial version | [e6dff98] |
| 2026-11-11 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S02 | Criterion 14 checked on the published wiki; verdict Go | pending |

---

## Artifact Under Review

- Instance reviewed: [WIKI-001]
- Checklist used: [QC-WIKI-001]
- Scope: full review
- Language and domain: en, da, ms (wiki, no language row)
- Language reviewer: none (the stand-in reads English and knows the IT domain)
- Mode: autonomous, not independent (`AI as stand-in for S02`)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | The wiki has a `_Sidebar.md`, because the host lists subpages only through it | Pass | docs/wiki/_Sidebar.md exists. |
| 2 | The sidebar starts with the wiki's title in bold, then one list of the pages in the primary language (English), `Home` first | Pass | Starts with the bold title, then one English page list, Home first. |
| 3 | The page list holds a link to every English page of the wiki, and no link points to a page that does not exist | Pass | Home, Getting started, Lecture steps and Learning points are all listed; every link target exists. |
| 4 | A `**Related**` section follows the page list only when the wiki has related wikis (for example the checklists wiki for a framework wiki); each entry is a link to that wiki's Home. A wiki with nothing related has no such section | N-A | No related wikis, and the sidebar has no Related section. |
| 5 | A `**Languages**` section is the last section of the sidebar. It has one line per language, the language written in that language, linking to that language's `Home` page | Pass | **Languages** is last, with English, Dansk and Bahasa Malaysia lines linking to each Home page. |
| 6 | The sidebar does not repeat the page list per language | Pass | The page list appears once. |
| 7 | A sidebar produced by a generator carries a comment that says so and names the generator; the generator is changed, not the page | N-A | The sidebar is written by hand, not generated. |
| 8 | The wiki has a `Languages` line on each page (criterion 11), so the sidebar is not the only way to switch language | Pass | Each page has the language line. |
| 9 | Every wiki exists in English and, as a minimum, in the language the project's registry names as the PO language; further languages are added on top, never instead of English | Pass | English and Danish (the PO-language minimum is English); Bahasa Malaysia added on top. |
| 10 | Every English page has a page in each other language of the wiki: the page sets are identical | Pass | Four pages in each of en, da and ms (12 pages). |
| 11 | Every page starts with the language line, with the current language in bold and a link to the same page in each other language | Pass | Every page starts with the language line, current language in bold. |
| 12 | A page in a language other than English is named `<Page>-<code>.md`, with a BCP 47 code; English has no suffix | Pass | Pages are named Page-da.md and Page-ms.md; English has no suffix. |
| 13 | Code blocks, commands, file names and IDs stay in English in every language | Pass | Code blocks, commands and file names are English in every language. |
| 14 | The sidebar, every page and every link were checked on the published wiki after the change, not only in the repository | Pass | After the merge the host listed all 13 pages (12 pages and the sidebar); a script read every page through the host API and found no dead link; the step images load. |
| 15 | A change to the layout rules (sections, order, naming) is made in the generator or template and in this checklist's source rules together | N-A | No layout rule was changed. |
| 16 | The wiki folder (`docs/wiki/`) is flat: every page, `Home.md` and `_Sidebar.md` included, is directly in it, and languages are told apart by file name, never by a subfolder | Pass | docs/wiki/ is flat; languages are told apart by file name. |

## Overall Verdict

Go — no Mandatory criterion fails; criterion 14 was checked on the published wiki. The stand-in review is not independent and stays open to challenge by S01.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| none | - | - |

---

[WIKI-001]: ../../wiki
[QC-WIKI-001]: ../../../framework/qc/artifacts/qc-wiki.md
[e6dff98]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/072-data-exploration-with-pandas/commit/e6dff989dc1db537606da1e3dc3af7814043e032
