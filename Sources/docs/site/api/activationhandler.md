# ActivationHandler

The dynamic-dispatch extension point for deciding what happens after an application
activation. The base class performs no application action.

## Boundary and dependencies

The service invokes Initialize, Handle Activation and Close. Configure a handler
before passing it to [ToastService.Initialize](/reference/toastservice/initialize.md);
the service retains the initialized instance.

Handle Activation receives LabVIEW activation values and the conversion error.
Keep the callback short and forward work to an application loop. Do not wait for
that loop or close the service from inside the callback.

The supplied [User Event plugin](/api/usereventactivationhandler.md) demonstrates
the current relay. A FIFO handler and a complete custom-handler tutorial remain
tracked separately. See [activation](/concepts.md?id=activation) and
[ownership](/callbacks.md) before implementing another destination.

<!-- API-MEMBERS -->
