# Documentation as code

Documentation lives under `Sources/docs` and is reviewed with the implementation.
No global npm installation or LabVIEW licence is needed to build the website.

## Project and third-party licences

The root `LICENSE` covers original ToastAPI code and authored documentation.
`THIRD-PARTY-NOTICES.md` distinguishes redistributed components, development
tools and proprietary prerequisites. `Sources/third-party-licenses` preserves
the upstream texts; existing vendor licences and bundle notices remain intact.

The build copies these files unchanged into `legal/` for versions that contain
`site/licenses.md`. The branch/release archive includes its own root licence
and notices when present. Historical refs without the page receive no new
licence or retroactive claim of rights. Review notices whenever DLLs or website
bundles change, and include the relevant files in any future VIPM package.

## Sources of truth

See [CONTENT-MAP.md](CONTENT-MAP.md) for the canonical source of each topic,
owner inventory, route compatibility and generated/manual boundaries.

- `api-map.json`: owner IDs, documented layers and related workflows. Membership
  and public scope are discovered from the root library and actual owner XML.
  `audience: internal` and `internal_members` exclude implementation details from
  the application reference without changing access scope. Repository-only support
  notes live in `maintenance/`. See CONTENT-MAP.md for compatibility help URLs.
- `site/api/*.md`: authored role/dependency pages. The API-MEMBERS marker receives
  the generated member list in staging only.
- `VISUAL-IDENTITY.md` and `site/assets/identity.css`: toolkit/class palette and
  usage rules. The maintainer reference stays outside the published site.
  `api-map.json` assigns each owner a
  `visual_family`; the User Event plugin uses the handler family.
- `site/`: authored English guides, navigation, API overview and Microsoft directory.
- `Sources/Examples/*.md`: canonical scenario guides, copied into the generated site.
- Saved application VI/payload descriptions: generated reference. Class methods
  keep existing help routes without changing VIs. Raw-handle accessor Help URLs
  retain a short class-directed compatibility page, outside indexes and search.
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

## Hybrid detailed help

`reference/toastbuilder/add-text.md` is the authored enrichment for the existing
`/reference/toastbuilder/add-text` route. The generator keeps the title, owner,
scope, source path and **Short description** from the versioned files, then appends
this Markdown. It never writes back to the authored directory or saved VIs.
The short description reproduces the saved LabVIEW Context Help text exactly;
it is read again on each build. The nine ToastBuilder and five ToastService
application methods, the three ActivationHandler hooks and four User Event
plugin methods now use this model: 21 application VIs across the four classes.
Payload types retain their generated summaries and are explained at method
terminals. Other entries explicitly say **Short description only**. Automated
export remains tracked in #46.

To author another page using the approved model:

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
   to `Sources/docs/reference`), `visual_sha256` and `error_behavior` (`skip`,
   `always`, or `noop` for an empty base hook). Use `review_fingerprint` from
   `tools/detailed_help.py`: XML owner files (.lvclass/.lvlib/.lvproj) normalize
   CRLF to LF for cross-platform checkouts when the record sets
   `fingerprint_format: sha256-lf-xml`; VIs, typedefs and images remain
   byte-exact. Historical records without this field keep their raw hashes.
   Include helper files whose behavior the page
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
also publish the selected catalogue. It contains only versions with documentation:

- `main` and `develop`;
- same-repository branches with an **open PR**, including draft PRs;
- tags attached to **published GitHub releases**, including prereleases.

Branches without an open PR, closed/merged PR branches, draft releases and bare
tags are omitted even if their Git refs remain. A branch preview starts when its
PR is opened; a Git branch has no independent open/closed state.

`.github/workflows/documentation-catalogue.yml` is a small orchestration workflow
installed on the default branch `main` as well as retained in `develop`. It
refreshes Pages on PR opening/reopening/closure and release changes, including
closure without merging. It explicitly checks out trusted `develop` scripts,
never a PR head. The public catalogue excludes fork PRs; their ordinary checks
remain read-only and do not publish. This main-branch workflow is infrastructure,
not a toolkit release. A merge onto develop/main also refreshes through its push.

Each version is built from its own saved VIs and Markdown. The current workflow's
builder treats other refs as data, never executing their scripts. Every deployment
contains the full version catalogue, so publishing a work branch preserves the
integration and release documentation. The selector preserves the requested page;
an absent page shows that version's 404 rather than silently switching content.
Each publication is a fresh complete artifact: excluded previews disappear from
the selector, every version manifest and the deployed directories. Their old
URLs cease to be published; Git branches and commit history are unchanged.
The event payload overrides briefly stale PR/release API results. API failures
fail the build instead of silently retaining an unfiltered catalogue.

The catalogue builder reads GitHub's paginated PR/release endpoints with a
read-only token in CI. For deterministic offline review, pass a JSON snapshot:

```powershell
python Sources/docs/tools/build_versions.py --output _review/pages --github-state _review/github-state.json
python Sources/docs/tools/test_build_versions.py
```

The snapshot has `pulls` and `releases` arrays using GitHub API field names.

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
