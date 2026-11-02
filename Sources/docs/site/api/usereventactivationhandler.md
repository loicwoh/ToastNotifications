# UserEventActivationHandler

A supplied [ActivationHandler](/api/activationhandler.md) implementation that
forwards activations to a typed LabVIEW User Event.

## Boundary and dependencies

Initialize creates and owns the event. The caller retrieves the initialized
handler returned by [ToastService](/api/toastservice.md), reads Event Ref and owns
its receiving event registration. The handler destroys the event in Close.

The delivery data type wraps Activation and its conversion error. The application
can process the payload in its own Event Structure instead of inside the native
callback. Read Event Ref is a communication property for this workflow, unlike
the native reference accessors in the builder and service.

The nominal path has been exercised in the reply and multiple-actions examples.
Event-generation diagnostics and shutdown during a callback are still tracked in
[#22](https://github.com/loicwoh/ToastNotifications/issues/22) and
[#16](https://github.com/loicwoh/ToastNotifications/issues/16).

<!-- API-MEMBERS -->
