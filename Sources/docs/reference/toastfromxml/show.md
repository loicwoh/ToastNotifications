## Connector

![Native LabVIEW Show icon and ToastFromXML and error terminals.](show.png)

## Inputs and outputs

| Input | Type | Default | Use |
|---|---|---|---|
| `ToastFromXML in` | ToastFromXML | Uninitialized | Created source with a live XML Document. |
| `error in` | Error cluster | No error | Incoming error chain. |

| Output | Type | Use |
|---|---|---|
| `ToastFromXML out` | ToastFromXML | Same source with document retained. |
| `error out` | Error cluster | Display/temporary cleanup result or incoming error. |

## Typical call sequence

```mermaid
flowchart LR
    accTitle: Display XML through the common source contract
    accDescr: Prepare the service and receiver, then give the XML source to ToastService.Show. It dispatches to this override, which creates a notification and notifier, shows the toast and releases those temporaries.
    P[Prepare service and receiver] --> S[ToastService.Show with XML source]
    S --> D[ToastFromXML.Show]
    D --> N[Create notification and notifier]
    N --> W[Show through Windows]
    W --> R[Release temporary references]
```

## Usage notes

- Use ToastService.Show in the application. It dynamically invokes this source
  override and borrows the source without closing it.
- Keeps the stored document alive. The caller closes the source after its last
  use. This method attempts to release the notification and notifier even after
  a display error.
- Callback registration and the receiving event loop are separate. Showing a
  notification does not guarantee it is visible under the current Windows settings.
- No XML loading or content composition occurs here.

## Related reading

[ToastService.Show](/reference/toastservice/show.md) ·
[XML example](/guides/xml.md) · [Close](/reference/toastfromxml/close.md)
