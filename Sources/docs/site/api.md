# Public API

This is a practical map of the current classes. The saved VIs and their context
help define the actual connector labels and behavior; this page is not an exhaustive
generated VI reference.

## ToastBuilder

| Method | Purpose | Main values |
|---|---|---|
| `Create` | Acquire the native builder | Builder output |
| `Add Text` | Append displayed text | `text` |
| `Add Text Input` | Define a submitted input field | `id`, `Title`, `Placeholder Text` |
| `Add Bouton` | Add an application-action button | `Content`, `Arguments` |
| `Add Link Button` | Add a protocol-activation button | `Content`, `URl` |
| `Set Activation Arguments` | Replace the body launch string with Foreground activation | `launchArgs` |
| `Get XML` | Serialize the current content | XML string |
| `Show` | Display using the native builder | Current builder |
| `Close` | Release the owned builder reference | Builder input |

`Add Bouton` and `URl` retain their current spelling in the project. A broader
English naming pass is planned. Displayed text is not automatically an activation argument.

The current input API does not add a default text value. The reply example uses a
standard button beneath the field; it does not claim an inline reply-button layout.

## ToastService

| Method | Responsibility |
|---|---|
| `Initialize` | Initialize the native service and supplied handler; store and return the initialized handler |
| `Register For Events` | Subscribe to native activation using the stored handler |
| `Show` | Display a borrowed builder |
| `Close` | Run the service cleanup path, including the handler Close hook |

The caller remains responsible for closing the builder. The service does not create
an independent builder reference merely because it receives a class input.

## ActivationHandler

Implement a child class when the application needs a custom activation destination.

| Hook | Responsibility |
|---|---|
| `Initialize` | Prepare handler-owned resources |
| `Handle Activation` | Process or forward Activation and its incoming conversion error |
| `Close` | Release handler-owned resources |

The base handler performs no application action. The supplied User Event handler
provides the working relay used in the examples. Its exceptional-path hardening is
still [in progress](coverage.md).

## Activation data

| Field | Meaning |
|---|---|
| `Activation.Arguments` | Raw application-defined activation string |
| `Activation.User Inputs` | Array of submitted `Key` / `Value` pairs |
| Delivery payload `error` | Conversion error forwarded beside Activation by the User Event handler |

For a request reply, `Arguments` can be `action=reject&requestId=42` while
`User Inputs` contains `Reason` → the typed text. Look up inputs by key, rather than
assuming a fixed array position. Empty submitted text and an absent key are different cases.

## XML support

`Get XML` is available. Loading and displaying a saved XML model is **planned** through
`ToastSource` and `XmlToast`; it is not implemented by the current builder.
