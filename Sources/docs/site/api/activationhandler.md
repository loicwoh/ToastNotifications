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

## Choose a hook

- [Initialize](/reference/activationhandler/initialize.md): return the initialized
  child value with the resources it needs for callback delivery.
- [Handle Activation](/reference/activationhandler/handle-activation.md): receive
  Activation and its conversion error, with no connector outputs.
- [Close](/reference/activationhandler/close.md): release child-owned resources
  while preserving the primary error.

The three base implementations perform no action. Error handling and delivery
are child responsibilities; the [User Event implementation](/api/usereventactivationhandler.md)
shows one concrete policy. A minimal custom handler implements these hooks and
exposes only the communication references needed by its caller.

<!-- API-MEMBERS -->
