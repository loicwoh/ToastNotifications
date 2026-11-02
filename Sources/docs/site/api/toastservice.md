# ToastService

Initialize the notification integration, register the activation callback, display
a borrowed [ToastSource](/api/toastsource.md) and close the service.

## Boundary and dependencies

Initialize accepts an [ActivationHandler](/api/activationhandler.md), calls its
Initialize hook, stores the initialized value and returns it. Register For Events
uses that stored handler. For the supplied plugin, retrieve Event Ref from the
returned [UserEventActivationHandler](/api/usereventactivationhandler.md).

**Call the service methods; let the service orchestrate the handler hooks.**
The application supplies a handler but does not separately call its Initialize,
Handle Activation or Close. See the
[handler lifecycle sequence](/api/activationhandler.md?id=hooks-orchestrated-by-toastservice)
for the boundary between application calls, dynamic hooks and callback delivery.

The callback uses internal reflection helpers to convert
native activation data before invoking the handler. Show calls ToastSource.Show
through dynamic dispatch; the concrete source remains owned by the caller.
The service does not give it an independent lifetime or close it.

The service owns its native reference and callback registration. Its Close path
also calls the handler Close hook. Concurrent callbacks, repeated registration
and partial failure remain [known limits](/callbacks.md?id=shutdown-is-still-being-hardened).

Native reference access is an implementation detail, outside the application API.

## Choose a method

- [Initialize](/reference/toastservice/initialize.md): inject the handler and
  initialize the service and handler resources.
- [Read ActivationHandler](/reference/toastservice/read-activationhandler.md):
  obtain the stored initialized handler through its read-only property.
- [Register For Events](/reference/toastservice/register-for-events.md): connect
  the native activation callback to that handler.
- [Show](/reference/toastservice/show.md): display caller-owned source content.
- [Close](/reference/toastservice/close.md): attempt service/handler cleanup,
  including when an earlier operation failed.

The detailed Close page shows the shutdown order and the lifetime guarantees
still tracked in [issue #16](https://github.com/loicwoh/ToastNotifications/issues/16).

<!-- API-MEMBERS -->
