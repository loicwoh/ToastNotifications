# Documentation as code

Documentation lives under `Sources/docs` and is reviewed with the implementation.
No global npm installation or LabVIEW licence is needed to build the website.

## Sources of truth

See [CONTENT-MAP.md](CONTENT-MAP.md) for the canonical source of each topic,
owner inventory, route compatibility and generated/manual boundaries.

- `api-map.json`: owner IDs, documented layers and related workflows. Membership
  and public scope are discovered from the root library and actual owner XML.
- `site/api/*.md`: authored role/dependency pages. The API-MEMBERS marker receives
  the generated member list in staging only.
- `site/visual-identity.md` and `site/assets/identity.css`: toolkit/class visual
  proposal, palette and usage rules. `api-map.json` assigns each owner a
  `visual_family`; the User Event plugin uses the handler family.
- `site/`: authored English guides, navigation, API overview and Microsoft directory.
- `Sources/Examples/*.md`: canonical scenario guides, copied into the generated site.
- Saved public VI/data-type descriptions in all discovered owners: generated reference.
  Class methods keep their existing help routes; libraries and types gain reference
  entries without changing the saved VIs or adding help URLs to them.
- `vendor/docsify-4.13.1/`: pinned runtime, search plugin, theme and MIT licence.
- `vendor/mermaid-tiny-12.2.0/`: pinned local renderer for authored Mermaid flowcharts.

Edit VI context help in LabVIEW and save before building. There is no manually
maintained description snapshot. The reader handles the uncompressed ANSI STRG
resource in the current VIs, is read-only, and refuses unsupported encodings or
layouts. It does not inspect wiring or infer behavior. Missing non-class descriptions
produce visible placeholders; strict CI rejects missing class-method descriptions.
Connector terminal descriptions and
diagrams are not automatically extracted yet. Authored walkthroughs still require human review
when behavior changes; a generated description cannot verify that it is correct.

## Hybrid detailed help (pilot)

`reference/toastbuilder/add-text.md` is the authored enrichment for the existing
`/reference/toastbuilder/add-text` route. The generator keeps the title, owner,
scope, source path and **Short description** from the versioned files, then appends
this Markdown. It never writes back to the authored directory or saved VIs.
The short description reproduces the saved LabVIEW Context Help text exactly;
it is read again on each build. Other entries explicitly say **Short description only**. Review the pilot before
expanding coverage in #42; automated terminal/diagram export is tracked in #46.

To author a page after the pilot is approved:

1. Copy `templates/detailed-help.md` to `reference/<owner-id>/<member-slug>.md`.
   Start at H2. Do not copy the VI summary or add another page title.
2. Inspect the saved VI and actual connector in LabVIEW, including slot positions,
   types, defaults and connection settings. Inspect its error branches and called
   helpers. Do not infer behavior from a majority-orientation offline estimate.
3. Export LabVIEW's native help illustration: the actual VI icon with its named
   terminals. The pilot uses `Print.VI To HTML` over ActiveX through
   `lvai_render_diagrams` with backend `pylabview`, taking the generated `*c.png`
   unchanged. This does not run or save the product VI. Keep the PNG next to the
   Markdown and link it by filename (`add-text.png`) with meaningful alt text.
   Do not redraw connector grids. If native capture is unavailable, report it
   rather than replacing it with an imitation.
4. Add an adjacent `.json` using the pilot record's schema: `schema_version: 1`,
   `source` (repository-relative saved VI), `reviewed_on` (ISO date), `method`
   (tools, LabVIEW version, evidence and visual revision), `reviewed_files`
   (repository-relative source paths to lowercase SHA-256), `visual` (relative
   to `Sources/docs/reference`), `visual_sha256` and `error_behavior` (`skip` or
   `always`). Include helper files whose behavior the page
   relies on. `Get-FileHash -Algorithm SHA256` or Python hashlib can calculate hashes.
5. Build twice, check routes, compare the terminals with Context Help and inspect
   the rendered page, search and links. Record separately any actual runtime test.

The published page uses a compact, bold error cue: **Skipped on incoming error.**
or **Executes even on incoming error.** Use the same wording in context-help
summaries when editing them in LabVIEW is authorized. Always-executing cleanup
must be visible; do not bury it in an internal error-case walkthrough. The Add Text
saved summary already states that it skips on incoming error; no VI is changed here.

Use a Mermaid flowchart for call sequences, with an accessible `accTitle` and
`accDescr`. Keep prose for wiring constraints or caveats that the diagram does
not explain. The pinned Tiny renderer works offline with strict security mode.
Review provenance, LabVIEW inspection versions and fingerprints stay in the JSON
and PR, not in the reader-facing page. User-facing compatibility information
belongs in the canonical coverage page.

Any byte change in a reviewed file makes the detailed-help build fail, including
a summary-only edit or a LabVIEW resave. Review the impact, update the Markdown/
visual if needed, then update the date, method and hashes. Never refresh hashes
blindly: a matching hash confirms the inspected snapshot, not correctness.
The saved summary is re-read on every build; no Markdown copy is maintained.
Historical refs without this authored directory still build with summaries only.

## Local preview

From the repository root with Python 3.12 or later:

```powershell
python Sources/docs/tools/docs_preview.py serve --port 8766
```

This workstation can use `C:/Tools/bin/pylabview/python.exe` instead of `python`.
Open `http://127.0.0.1:8766/ToastNotifications/`. Stop with Ctrl+C.

```powershell
python Sources/docs/tools/docs_preview.py build
python Sources/docs/tools/docs_preview.py check
python Sources/docs/tools/test_api_inventory.py
python Sources/docs/tools/test_detailed_help.py
```

The ignored `_review/docsify-preview/ToastNotifications` directory holds generated
files. The preview uses the repository subpath to catch relative-path mistakes.
Checks validate internal Markdown routes and HTML entry assets, not external-site
availability. Vendor files are local so navigation and search work without a CDN.

## Publication and versions

`.github/workflows/documentation.yml` checks every push and pull request. Pushes
also build and publish the available remote branches and tags containing this docs
layout. A merge onto `develop` or `main` is a push and follows the same path.
Pull requests validate without publishing; no fork credentials are exposed.

Each version is built from its own saved VIs and Markdown. The current workflow's
builder treats other refs as data, never executing their scripts. Every deployment
contains the full version catalogue, so publishing a work branch preserves the
integration and release documentation. The selector preserves the requested page;
an absent page shows that version's 404 rather than silently switching content.
Deleted branches disappear at the next publication; release tags remain selectable.

The root URL redirects to `main` once main contains documentation. Until then it
opens `develop`, or the first available work branch. The version selector always
identifies the actual branch; this fallback is not a released version. Public VI detailed-help links use:

```text
https://loicwoh.github.io/ToastNotifications/#/reference/<class-slug>/<vi-slug>
```

For example: `#/reference/toastbuilder/add-text`. These stable URLs resolve to the
released documentation. During development, open the work branch using the selector.
The 23 current public VIs have their online detailed-help URL saved. After adding
or renaming a public method, close the LabVIEW project and build locally, then run:

```powershell
./Sources/docs/tools/Sync-DetailedHelp.ps1
./Sources/docs/tools/Sync-DetailedHelp.ps1 -Apply
python Sources/docs/tools/docs_preview.py build --require-help-links
```

The first command inspects the target URLs. `-Apply` backs up the VIs under
`_review/detailed-help-backup`, refuses unsaved changes, sets only HelpDocumentUrl
and HelpUseOnline through LabVIEW's ActiveX server and saves using SaveInstrument.
Run on Windows with LabVIEW installed, from the repository root, with projects
closed. It never runs product VIs or cleans diagrams. LabVIEW may update compiled
or serialized resources when saving. CI checks descriptions and saved help URLs
for the pushed source without needing LabVIEW; historical versions are still
buildable without imposing that new check on their metadata.

Repository setup: make the repository public and set Settings → Pages → Source to
GitHub Actions. The `github-pages` environment must allow repository work branches,
`develop`, `main` and release tags to deploy. GitHub's environment protections can
otherwise reject a branch even when the workflow itself is correct.

GitHub Pages uses GitHub Actions. The environment allows `main`, `develop`,
`codex/*` work branches and `v*` release tags. For another branch naming convention,
add its deployment rule before pushing. Keep `main` reserved for releases; review
this branch into `develop`.

Docsify 4.13.1 is the explicit initial baseline. A runtime update should be reviewed
separately. Upstream assets came from the npm 4.13.1 jsDelivr `lib` paths and matching
GitHub tag licence. The small VI resource reader follows the format documented by
the MIT-licensed [pylabview project](https://github.com/mefistotelis/pylabview).
