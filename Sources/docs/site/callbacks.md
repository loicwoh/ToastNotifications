# Callbacks & ownership

[Concepts](/concepts.md) · [ToastService](/api/toastservice.md) ·
[ActivationHandler](/api/activationhandler.md) ·
[User Event plugin](/api/usereventactivationhandler.md)

Keep the native callback short. Transfer data to the application's loop before
performing long-running work or interacting with the UI.

## User Event flow

Initialize, Handle Activation and Close on the handler are hooks invoked by
the service and its callback. The application calls the service and prepares
its own receiver. See the
[lifecycle sequence](/api/activationhandler.md?id=hooks-orchestrated-by-toastservice).

Read the reference from the initialized handler. A copy of the original pre-initialized
class value does not acquire references that were subsequently created on another value.

## Resource owners

| Resource | Owner | Application rule |
|---|---|---|
| Builder native handle | Builder's owner | Close after its last use; class copies share the handle |
| Service callback registration and native reference | ToastService | Use the service Close path |
| User Event | UserEventActivationHandler | Borrow it for registration; do not destroy it independently |
| Event Registration Ref for the receiving loop | Application | Unregister when reception is finished |
| Native arguments handed to the callback | Callback mechanism | Borrowed; do not close them as acquired references |
| Converted Activation payload | LabVIEW values | No native ownership crosses the delivery boundary |

## Errors are two separate observations

The example's `error` indicator is the conversion error carried in its most recently
delivered User Event. Its final `error out` is the setup/cleanup result available when
the example finishes. Neither is an event history.

The User Event handler bundles the conversion error as data so that it does not
automatically suppress the event. It does not yet expose the failure result of
`Generate User Event`. Invalid-reference and failed-delivery diagnostics remain in
[issue #22](https://github.com/loicwoh/ToastNotifications/issues/22).

## Shutdown is still being hardened

The examples stop receiving, attempt event unregistration and service/handler closure,
then close the builder. They retain a final .NET collection workaround observed to
release a reserved callback on the development workstation.

This is not a guarantee that all callbacks in progress have drained. A complete
shutdown contract must prevent new work, unsubscribe, resolve callbacks already
engaged and only then release resources they can still access. Repeated closure,
partial initialization and concurrency are tracked in
[issue #16](https://github.com/loicwoh/ToastNotifications/issues/16).

Do not close the service from inside its callback, wait for a response from the
receiving loop, or treat `GC.Collect` as a substitute for resource ownership.
