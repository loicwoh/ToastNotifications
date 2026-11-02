# Public API

[Toolkit library](/api/toastnotification.md) · [VI and data type reference](/reference.md) · [Concepts](/concepts.md)

Choose a layer before choosing a VI. The categories below describe how the current
examples use the toolkit; they do not change LabVIEW scopes or promise release
compatibility. The supported API and versioning policy remain tracked in
[#18](https://github.com/loicwoh/ToastNotifications/issues/18).

## ToastBuilder

[ToastBuilder: role, dependencies and members](/api/toastbuilder.md) — construct
content through LabVIEW methods.

## ToastService

[ToastService: role, dependencies and members](/api/toastservice.md) — initialize,
register, display with a borrowed builder and close.

## ActivationHandler

[ActivationHandler: hooks and members](/api/activationhandler.md) — the extension
contract. [UserEventActivationHandler](/api/usereventactivationhandler.md) is the
supplied implementation used by the reply and multiple-actions examples.

## Activation data

The root [ToastNotification library](/api/toastnotification.md) owns Activation
and Argument. The [User Event plugin](/api/usereventactivationhandler.md) owns the
delivery wrapper that adds the conversion error beside Activation.

## Implementation boundary

Native .NET calls and reflection helpers are internal implementation details.
The application API is carried by the classes above and their activation data.
This documentation boundary does not itself change the saved LabVIEW scopes.

## XML support

[Get XML](/reference/toastbuilder/get-xml.md) is available. Loading saved XML through
ToastSource/XmlToast remains planned in #27–#29; those classes are not implemented.

## Continue with an example

[Reply](/guides/reply.md) · [Multiple actions](/guides/multiple-actions.md) ·
[Open a link](/guides/protocol.md) · [Coverage and limits](/coverage.md)
