# ToastAPI source project

Open `ToastAPI.lvproj` to work on the toolkit. Open `Toast Notification Examples.lvproj`
to run the examples listed in the [example guides](docs/example-guides/README.md).

## Documentation entry points

- [Published documentation](https://loicwoh.github.io/ToastNotifications/)
- [Project motivation and background](docs/site/background.md)
- [Getting started source](docs/site/getting-started.md)
- [API overview source](docs/site/api.md)
- [Concept map source](docs/site/concepts.md)
- [Callback and ownership contract](docs/site/callbacks.md)
- [Coverage and known limits](docs/site/coverage.md)
- [Documentation maintenance and preview](docs/README.md)
- [Canonical content map](docs/CONTENT-MAP.md)

Each class/library and its members occupy one flat physical folder; virtual scope
folders are independent of that layout. Native dependencies are in `bins`.
The original prototype is retained under `Archive`.

[ARCHITECTURE.md](ARCHITECTURE.md) and [CALLBACK-LIFETIME.md](CALLBACK-LIFETIME.md)
contain maintainer implementation notes and historical observations.
[HANDOFF.md](HANDOFF.md) is a handover log. These files are not alternative
end-user tutorials or evidence of a fresh regression run.
