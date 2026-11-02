# ToastAPI for LabVIEW

Build interactive Windows notifications from LabVIEW, and receive activation
arguments and submitted text through a customizable handler.

- [Documentation and examples](https://loicwoh.github.io/ToastNotifications/)
- [Why this project](https://loicwoh.github.io/ToastNotifications/#/background)
- [Source project](Sources/ToastAPI.lvproj)
- [Documentation maintenance](Sources/docs/README.md)
- [Current coverage and limitations](Sources/docs/site/coverage.md)

Development currently uses LabVIEW 2026 on Windows and
Microsoft.Toolkit.Uwp.Notifications. `develop` is the integration branch; `main`
is reserved for releases. Documentation previews identify their branch and commit
in the version selector. Compatibility with LabVIEW 2020 remains planned.

## License

Original ToastAPI code and authored documentation are available under the
[MIT License](LICENSE), copyright (c) 2026 loicwoh, without warranty or an
obligation to provide support. Third-party components retain their own terms;
see [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md), including the legacy DLL
remaining in repository history. LabVIEW and platform prerequisites are
licensed separately.
