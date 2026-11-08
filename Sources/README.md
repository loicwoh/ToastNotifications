# Toast Notifications source project

Open `Toast Notifications.lvproj` to work on the toolkit. Open `Toast Notification Examples.lvproj`
to run the examples listed in the [example guides](docs/example-guides/README.md).

Use LabVIEW 2026 as the development IDE. Both projects use **Save Version 2020**
so the same source tree can be opened in LabVIEW 2020.

## Build the VIPM package

From the repository root, build from the commit selected for release. The first
release uses LabVIEW 2026 64-bit on Windows and VIPM 26.3.2.

```powershell
$env:VIPM_DESKTOP_LIVELINESS_TIMEOUT = '120'
vipm build "Sources/Toast Notifications for LabVIEW.vipb" --labview-version 2026 --labview-bitness 64 --timeout 240
```

VIPM writes the `.vip` to `Builds/VIPM`. Install it in the target LabVIEW version
and open the installed examples project to verify the package before publishing.

## Documentation entry points

- [Published documentation](https://loicwoh.github.io/ToastNotifications/)
- [Project motivation and background](docs/site/background.md)
- [Getting started source](docs/site/getting-started.md)
- [API overview source](docs/site/api.md)
- [Concept map source](docs/site/concepts.md)
- [Callback and ownership contract](docs/site/callbacks.md)
- [Native integration and reflection notes](docs/maintenance/)
- [Coverage and known limits](docs/site/coverage.md)
- [Documentation maintenance and preview](docs/README.md)
- [Canonical content map](docs/CONTENT-MAP.md)

Each class/library and its members occupy one flat physical folder; virtual scope
folders are independent of that layout. Native dependencies are in `bins`.
The original prototype is retained under `Archive`.
