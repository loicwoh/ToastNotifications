## Connector

![Native LabVIEW Initialize icon with ActivationHandler in and error in inputs, ToastService out, ActivationHandler out and error out outputs.](initialize.png)

## Inputs and outputs

| Input | Type | Default | Use |
|---|---|---|---|
| `ActivationHandler in` | ActivationHandler | Base handler | **Required.** Supply the child class that will process activations. |
| `error in (no error)` | Error cluster | No error | Incoming error chain. |

| Output | Type | Use |
|---|---|---|
| `ToastService out` | ToastService | New service storing the native reference and initialized handler on success. |
| `ActivationHandler out` | ActivationHandler | Value returned by the handler Initialize hook; retains its runtime child type. |
| `error out` | Error cluster | Native initialization, handler initialization or storage error; incoming error otherwise. |

## Typical call sequence

```mermaid
flowchart LR
    accTitle: Initialize the service and prepare the reply receiver
    accDescr: Inject a configured handler into Initialize, use its returned initialized value to prepare the receiver, register the native callback and then show a builder.
    H[Configured handler] --> I[ToastService.Initialize]
    I -->|Service| R[Register For Events]
    I -->|Initialized handler| E[Prepare application receiver]
    R --> S[ToastService.Show]
    E --> S
```

For the User Event plugin, cast the returned handler to
[UserEventActivationHandler](/api/usereventactivationhandler.md), read Event Ref
and register the application's Event Structure before showing the toast.

## Usage notes

- This VI requires `ActivationHandler in`, calls its Initialize hook and
  stores/returns the initialized value. Callback registration remains a
  separate step.
- Native initialization calls `WasCurrentProcessToastActivated`. Its Boolean
  result is not exposed; it is not an activation payload or a waiting operation.
- The input handler's runtime child class selects the Initialize override and,
  later, Handle Activation. The base handler owns no delivery mechanism.
  Configure a child before this call; do not separately initialize the same
  owned handler lifecycle a second time.
- On incoming error, native and handler initialization are skipped:
  `ToastService out` is a default service and `ActivationHandler out` is the
  unchanged input handler. Check `error out` before using either output.
- Use the initialized output, or [Read ActivationHandler](/reference/toastservice/read-activationhandler.md),
  to obtain references created by the hook. The original class value does not
  gain fields written into a later value.
- A failure after resource acquisition has no rollback path here. The native
  handle or initialized handler may not be stored in the returned service if
  a later step fails. Partial-initialization cleanup remains covered by
  [issue #16](https://github.com/loicwoh/ToastNotifications/issues/16).

## Related reading

[ToastService](/api/toastservice.md) · [Register For Events](/reference/toastservice/register-for-events.md) ·
[Callbacks and ownership](/callbacks.md) · [Handle multiple actions](/guides/multiple-actions.md)
