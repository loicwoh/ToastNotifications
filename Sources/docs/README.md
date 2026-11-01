# Documentation as code

Documentation lives under `Sources/docs` and is reviewed with the implementation.
No global npm installation or LabVIEW licence is needed to build the website.

## Sources of truth

- `site/`: authored English guides, navigation, API overview and Microsoft directory.
- `Sources/Examples/*.md`: canonical scenario guides, copied into the generated site.
- Saved public VI descriptions in ToastBuilder, ToastService, ActivationHandler and
  UserEventActivationHandler: generated detailed reference. Class membership and
  public scope are read from `.lvclass` XML on each build.
- `vendor/docsify-4.13.1/`: pinned runtime, search plugin, theme and MIT licence.

Edit VI context help in LabVIEW and save before building. There is no manually
maintained description snapshot. The reader handles the uncompressed ANSI STRG
resource in the current VIs, is read-only, and refuses unsupported encodings or
layouts. It does not inspect wiring or infer behavior. Missing descriptions produce
explicit warnings and visible placeholders. Connector terminal descriptions and
diagrams are not extracted yet. Authored walkthroughs still require human review
when behavior changes; a generated description cannot verify that it is correct.

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
lists development versions explicitly. Public VI detailed-help links should use:

```text
https://loicwoh.github.io/ToastNotifications/#/reference/<class-slug>/<vi-slug>
```

For example: `#/reference/toastbuilder/add-text`. These stable URLs resolve to the
released documentation. During development, open the work branch using the selector.
Setting these URLs in saved VI metadata is a separate integration step; it is not
performed by the build and cannot happen on a Linux GitHub runner.

Repository setup: make the repository public and set Settings → Pages → Source to
GitHub Actions. The `github-pages` environment must allow repository work branches,
`develop`, `main` and release tags to deploy. GitHub's environment protections can
otherwise reject a branch even when the workflow itself is correct.

Publication is not active until these files are committed/pushed and Pages setup
is complete. Keep `main` reserved for releases; review this branch into `develop`.

Docsify 4.13.1 is the explicit initial baseline. A runtime update should be reviewed
separately. Upstream assets came from the npm 4.13.1 jsDelivr `lib` paths and matching
GitHub tag licence. The small VI resource reader follows the format documented by
the MIT-licensed [pylabview project](https://github.com/mefistotelis/pylabview).
