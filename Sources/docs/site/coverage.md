# Coverage & known limits

This matrix separates implemented workflows from planned features. Manual success
on the development workstation is not a claim of full compatibility or leak-free operation.

## Feature map

| Capability | Public entry point | Example / follow-up | Status |
|---|---|---|---|
| Displayed text | Add Text | All focused examples | Available |
| Application-action buttons | Add Bouton | Multiple actions | Manually validated |
| Body activation arguments | Set Activation Arguments | Multiple actions | Manually validated |
| Protocol button | Add Link Button | Link button | Manually validated |
| Text input | Add Text Input | Reply | Manually validated, including empty text and special characters |
| User Event delivery | UserEventActivationHandler | Reply / Multiple actions; #22 | Nominal path works; errors still need hardening |
| Common source contract | ToastSource base class; ToastBuilder implementation | #27 | Implemented by ToastBuilder and ToastFromXML |
| XML string display | ToastFromXML | [XML example](guides/xml.md); #28 | Nominal display manually validated |
| XML files and templates | Methods to define | #29 | Planned |
| Images | Methods to define | #5 | Planned |
| Selection input | Methods to define | #8 | Planned |
| Progress and updates | Methods to define | #9 | Planned |
| Reminder and audio | Methods to define | #10 | Planned |
| Queue delivery | Planned QueueActivationHandler | #23 | Not implemented |
| Button icons, styles, tooltips, context menus | Methods / XML path to define | #31–#34 | Planned |

Numbers refer to [GitHub issues](https://github.com/loicwoh/ToastNotifications/issues).
ToastFromXML parses XML text into a retained document. File I/O and parameterized
templates remain application work. Constructor failure cleanup is not yet guaranteed
when parsing fails after document creation; resource hardening remains in #16.

## Compatibility

| Environment | Current statement |
|---|---|
| LabVIEW 2026 on the development Windows workstation | Working examples and execution-state checks |
| LabVIEW 2020 | Target under evaluation in #25; not verified |
| Other Windows versions, architectures and built-application deployments | Compatibility matrix still to establish in #17 |
| VIPM installation | Package planned in #14; not released |

The implementation currently relies on `Microsoft.Toolkit.Uwp.Notifications`.
The Windows App SDK notification API is a separate integration route. Do not copy
its method names into this wrapper and assume they are interchangeable.

## Release work

- **#16:** resource lifetime, duplicate registrations, partial failures and concurrent shutdown.
- **#22:** failed User Event generation and invalid references.
- **#15:** useful automated-test scope without assuming notification clicks can be automated.
- **#12–#14:** English documentation, the documentation site and distribution.
- **#18:** license, public API versioning and release process.

The example guides report observed behavior and remaining checks. If the guide and
a saved VI disagree, inspect the current VI and update the documentation before release.
