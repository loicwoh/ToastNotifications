## Connector

![Native LabVIEW Add Hero Image icon and terminals.](add-hero-image.png)

## Inputs and outputs

| Input | Type | Use |
|---|---|---|
| `ToastBuilder in` | ToastBuilder | A created, live builder. |
| `Image` | Path | Absolute path to a local image file. |
| `alternateText` | String | Optional description for assistive technology. |
| `error in (no error)` | Error cluster | Incoming error chain. |

| Output | Type | Use |
|---|---|---|
| `ToastBuilder out` | ToastBuilder | The same builder, modified on success. |
| `error out` | Error cluster | Result of the operation or the incoming error. |

## Typical call sequence

```mermaid
flowchart LR
    accTitle: Show a toast with a hero image
    accDescr: Create a builder, add text and a local image, show the toast, then close the builder.
    A[Create ToastBuilder] --> B[Add Text] --> C[Add Hero Image] --> D[ToastService.Show] --> E[Close builder]
```

## Usage notes

- The wrapper converts the local path to a file URI. Windows reads the file when rendering the notification, so keep it available while the toast can be displayed.
- Check the path and file if the toast displays without its image. A successful `Show` does not confirm that Windows rendered the image.

[Result preview example](/guides/images.md)
