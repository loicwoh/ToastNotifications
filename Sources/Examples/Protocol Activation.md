# Protocol activation example — implementation plan

Tracked in [issue #11](https://github.com/loicwoh/ToastNotifications/issues/11).
This example is not implemented yet. The LabVIEW implementation will be authored manually.

## Intended public API

Proposed method: `ToastBuilder.Add Link Button`, with `Content` and `URL` string inputs,
the builder class input/output and the usual error input/output.
Keep .NET references internal and follow the existing Error/No Error convention.
Confirm the connector and naming while implementing the method.

## Native sequence to explore

1. Create a `ToastButton` and set its display text.
2. Construct a `System.Uri` from an HTTPS URL.
3. Configure the button with `SetProtocolActivation`, using the overload available in the installed toolkit.
4. Add the configured button to the toast builder and show the toast.

Review temporary reference ownership and cleanup on both success and error paths.
Do not close the builder borrowed from the class in this method.
Protocol activation asks Windows to open the URI in its associated application;
it is distinct from invoking the application's activation handler.

Reference: [ToastButton API](https://learn.microsoft.com/en-us/dotnet/api/microsoft.toolkit.uwp.notifications.toastbutton?view=win-comm-toolkit-dotnet-7.0).

## Manual acceptance checks

- Use a public HTTPS URL, such as the project's GitHub page.
- Clicking the link button opens the intended page in the associated browser.
- Document the separate behavior of clicking the notification body.
- Verify the example's stop and cleanup path, including temporary .NET references.
- Add context help and usage instructions once the VI is implemented.

No implementation or functional validation has been performed as part of this preparation.
