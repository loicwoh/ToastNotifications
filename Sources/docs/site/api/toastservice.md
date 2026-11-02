# ToastService

Initialize the notification integration, register the activation callback, display
a borrowed [ToastBuilder](/api/toastbuilder.md) and close the service.

## Boundary and dependencies

Initialize accepts an [ActivationHandler](/api/activationhandler.md), calls its
Initialize hook, stores the initialized value and returns it. Register For Events
uses that stored handler. For the supplied plugin, retrieve Event Ref from the
returned [UserEventActivationHandler](/api/usereventactivationhandler.md).

The callback uses [Reflection DotNet](/api/reflection-dotnet.md) helpers to convert
native activation data before invoking the handler. The builder remains owned by
the caller; the service does not give it an independent lifetime.

The service owns its native reference and callback registration. Its Close path
also calls the handler Close hook. Concurrent callbacks, repeated registration
and partial failure remain [known limits](/callbacks.md?id=shutdown-is-still-being-hardened).

The native reference accessor is implementation-level access, not the recommended
entry point for application code.

<!-- API-MEMBERS -->
