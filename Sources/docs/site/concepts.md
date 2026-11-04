# Concepts

Use this map to move between the toolkit's layers and its working examples.
Expanded explanations belong to
[#40](https://github.com/loicwoh/ToastNotifications/issues/40); the links below
already lead to the current API and contracts.

## Toast source

[ToastSource](/api/toastsource.md) is the base class for Show, Get XML and Close.
The application creates a concrete source and retains responsibility for its
cleanup. ToastService borrows it and invokes its Show override.

The creation polymorph groups concrete constructors; it currently offers
ToastBuilder and ToastFromXML. Compose with the builder or provide XML text to
ToastFromXML; both use the same ToastService and activation handlers.

## Builder

Microsoft's ToastContentBuilder is the native composition object.
[ToastBuilder](/api/toastbuilder.md) is the LabVIEW wrapper around that object.
Its methods change the native content directly.

Continue with the [builder methods](/api/toastbuilder.md), the
[reply example](/guides/reply.md) or the [link example](/guides/protocol.md).

## Activation

Arguments are supplied by the application; User Inputs are submitted field values.
Protocol activation opens the associated Windows application rather than invoking
the LabVIEW handler for that button.

Continue with [ActivationHandler](/api/activationhandler.md),
[shared data types](/api/toastnotification.md?id=public-members),
[multiple actions](/guides/multiple-actions.md) or [text input](/guides/reply.md).

## Ownership

A copied class can still refer to the same underlying resource. Creation,
borrowing, receiving-event registration and closure each need an explicit owner.

Continue with the [callback ownership contract](/callbacks.md),
[ToastService](/api/toastservice.md) and
[UserEventActivationHandler](/api/usereventactivationhandler.md).

## Reflection

The integration obtains native type/member information to reach operations that
are awkward to call directly from LabVIEW. Conversion helpers keep those details
outside the application's activation payload.

Continue with [ToastService](/api/toastservice.md), the [ownership contract](/callbacks.md)
and the [Microsoft directory](/microsoft.md).
