# ToastBuilder

Compose a notification by calling the native builder through a LabVIEW class.
Start with Create ToastBuilder, add the required content and inspect Get XML when useful.
Display through the application's [ToastService](/api/toastservice.md) workflow.

## Boundary and dependencies

This class derives from [ToastSource](/api/toastsource.md) and delegates composition
to the native toolkit. Its methods change the native
builder directly; there is no separate LabVIEW content engine. The class exposes
composition methods for displayed text, text input, application buttons, protocol
buttons, hero images and body arguments. Show, Get XML and Close override the source operations.
To reuse exported XML text, create a [ToastFromXML](/api/toastfromxml.md) source.

One caller owns Close. Copies of the class share a handle, so closing an alias
affects the other copies. See [resource ownership](/callbacks.md).

The application uses these methods without manipulating the underlying .NET handle.
Native reference accessors and storage types are implementation details.

## Choose a method

- [Create](/reference/toastbuilder/create-toastbuilder.md), then compose [text](/reference/toastbuilder/add-text.md),
  [text input](/reference/toastbuilder/add-text-input.md), [application actions](/reference/toastbuilder/add-bouton.md)
  or [a link button](/reference/toastbuilder/add-link-button.md).
- Add a [hero image](/reference/toastbuilder/add-hero-image.md) to preview a result.
- Set [body activation arguments](/reference/toastbuilder/set-activation-arguments.md)
  separately from button arguments and submitted values.
- [Inspect XML](/reference/toastbuilder/get-xml.md), then display through
  [ToastService.Show](/reference/toastservice/show.md). The builder's
  [Show](/reference/toastbuilder/show.md) is the delegated display call.
- [Close](/reference/toastbuilder/close.md) the builder after its last use, including
  after a failure. Class copies alias one handle; keep one explicit owner.

<!-- API-MEMBERS -->
