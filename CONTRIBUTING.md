# Contributing to ToastAPI

## Development environment

The current development IDE is **LabVIEW 2026 Q3 (64-bit) on Windows**.
On `develop`, open `Sources/ToastAPI.lvproj` and run the example closest to your change.
The project keeps its notification toolkit DLLs in `Sources/bins`.
LabVIEW 2020 compatibility is under evaluation. See the current [compatibility and coverage](https://loicwoh.github.io/ToastNotifications/#/coverage).

## Git and issue workflow

1. Pick or open an issue and describe the change you want to make. The maintainer tracks active work as **In Progress** on the project board.
2. Start a topic branch from the current `develop`. For example, `git fetch origin` followed by `git switch -c feature/short-topic origin/develop`.
3. Verify the change in the relevant example. In your PR, describe what changed, what you verified, and any remaining limitations.
4. Open the PR against `develop` and link the issue. Once the work is integrated and the issue's scope is complete, the maintainer closes it as **Completed** and moves it to **Done**. Issues closed without implementation use **Not planned** or **Duplicate**, as appropriate.

`develop` is the integration branch. Releases land on `main`.

## Documentation and examples

Keep public guides and VI help in English. An example guide should explain why to try the VI, what to do, and what the reader can reuse in their application. Update the relevant guide or API page when you change a public behavior.

To check the site from the repository root on `develop`, use Python 3.12 or later.

```powershell
python Sources/docs/tools/docs_preview.py build --require-help-links
```

[Local preview and documentation conventions](https://github.com/loicwoh/ToastNotifications/blob/develop/Sources/docs/README.md)

## Reporting a problem

Include your LabVIEW version and bitness, Windows version, the VI or example you ran, and the steps to reproduce the problem. Include the expected result, what happened, and any LabVIEW error code and source. [Open an issue](https://github.com/loicwoh/ToastNotifications/issues/new)
