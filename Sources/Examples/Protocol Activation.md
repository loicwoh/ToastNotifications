# Toast with a link button

Tracked in [issue #11](https://github.com/loicwoh/ToastNotifications/issues/11).
Open `ToastAPI.lvproj`, then `Examples/Toast With Link Button.vi`.
The example was implemented manually and the user confirmed that the link button works.

## Public API

`ToastBuilder.Add Link Button` accepts two LabVIEW strings: `Content` and `URl`
(the current connector label), plus the builder and error inputs/outputs.
`Content` is the displayed button text; `URl` is the address Windows should open.
The example uses diagram constants:

| Input | Example value |
|---|---|
| Content | `Open project on GitHub` |
| URl | `https://github.com/loicwoh/ToastNotifications` |

Create the builder before adding the button. This method modifies the builder;
it does not display the toast. It skips work on an incoming error and passes
the class and error through. The builder owner closes it after the last use.

## Native implementation

`Toast Native.Add Link Button` calls the installed toolkit overload:

```text
ToastContentBuilder.AddButton(String content,
                             ToastActivationType activationType,
                             String arguments)
```

`activationType` is fixed to `Protocol`; the URI string is passed directly to
`arguments`. This implementation needs neither a `System.Uri` object nor a
separately acquired `ToastButton` handle. URI validation and errors are delegated
to the toolkit and Windows; the wrapper does not add its own validation policy.

The native input reference is borrowed. `reference out` aliases the same builder,
and neither is closed by this method. Public class methods keep these .NET details internal.
Protocol activation asks Windows to open the URI in its associated application;
it is distinct from invoking the application's activation handler.

Reference: [ToastContentBuilder API](https://learn.microsoft.com/en-us/dotnet/api/microsoft.toolkit.uwp.notifications.toastcontentbuilder?view=win-comm-toolkit-dotnet-7.1).

## Trying the example

1. Run the VI. It creates a builder, adds two text lines and the link button,
   reads `Toast XML`, initializes the service, registers the base handler and shows the toast.
2. Click **Open project on GitHub**. Windows opens the URL in the associated browser.
   This button action does not invoke the LabVIEW activation handler.
3. Clicking the notification body instead is a separate application activation.
   The current base `ActivationHandler.Handle Activation` performs no action and shows no dialog.
   Override it in a child class if the application should react to body activation.
4. Press **stop** in the example after trying the toast. The VI unregisters and closes
   the service, closes the builder, then performs the existing `System.GC.Collect()` call.
   Clicking the link alone does not stop the VI. It also waits for stop if setup reports an error;
   inspect `error out` after the VI finishes.

The final collection is the existing workaround for callback reservation observed
on this workstation. It is not evidence that every lifetime or concurrency case is resolved.

`Toast XML` allows inspection of the action: `activationType="protocol"`,
`content` containing the displayed text, and `arguments` containing the URI.

Validation: the user confirmed successful opening of the link. Documentation work
does not re-run the example or claim that body activation, invalid URLs or repeated
activation/closure have been tested. Remaining lifecycle hardening is tracked in issue #16.
