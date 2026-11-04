## Connector

![Native LabVIEW Show icon with ToastService in, ToastSource in and error in inputs, ToastService out and error out outputs.](show.png)

## Inputs and outputs

| Input | Type | Default | Use |
|---|---|---|---|
| `ToastService in` | ToastService | Uninitialized | Service from the setup chain, with callback registration if activations are needed. |
| `ToastSource in` | ToastSource | Default base class | **Required.** Created, configured concrete source. The base class performs no display. |
| `error in (no error)` | Error cluster | No error | Incoming error chain. |

| Output | Type | Use |
|---|---|---|
| `ToastService out` | ToastService | Same service value; no new service resource is acquired. |
| `error out` | Error cluster | Concrete source display result, or unchanged incoming error. |

## Typical call sequence

```mermaid
flowchart LR
    accTitle: Display composed content through the service
    accDescr: Service initialization and registration join the configured builder at Show. The application then waits for activations and closes its resources after stopping reception.
    I[Initialize / register service] --> S[ToastService.Show]
    B[Create / configure concrete source] --> S
    S --> W[Application receives activations]
    W --> C[Stop / close service and source]
```

## Usage notes

- This method dynamically invokes [ToastSource.Show](/reference/toastsource/show.md).
  ToastBuilder supplies builder display and ToastFromXML supplies XML display;
  the service has no concrete-type switch or cast to ToastBuilder.
  It does not inspect or validate service state, initialize the service or
  register a callback. Successful display alone does not prove reply delivery
  is configured.
- Show borrows the source and has **no source output**. Keep its existing
  class value for caller-owned cleanup; the service does not retain an
  independent copy of its resources or close it.
- On incoming error, the source Show call is skipped and the service/error
  pass through unchanged.
- `error out` reports the display call, not the user's later action or input.
  Those arrive asynchronously through the handler. Keep the receiving workflow
  alive after this VI returns.
- Use application actions for callback replies and protocol buttons for opening
  links. Clicking a protocol button does not invoke the app handler for that
  button; see [Open a link](/guides/protocol.md).

## Related reading

[ToastService](/api/toastservice.md) · [Register For Events](/reference/toastservice/register-for-events.md) ·
[ToastBuilder](/api/toastbuilder.md) · [Receive a text reply](/guides/reply.md) ·
[Close](/reference/toastservice/close.md)
