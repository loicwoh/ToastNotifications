# Offer a choice in a toast

Let an operator accept or reject a request without switching back to LabVIEW. Application-action buttons carry distinct arguments, and a User Event delivers the selection.

## Try it

Open `ToastAPI.lvproj` and run `Examples/Toast With Multiple Actions.vi`. Click **Accept**, **Reject**, or the toast body and inspect `Activation.Arguments`. Run again to try another choice. Press **stop** after each run.

## What to look for

The buttons return `action=accept` and `action=reject`. Clicking the body returns `action=open`. All three carry `requestId=42`. Use the action to decide what to do and the request ID to find the affected item.

[Set Activation Arguments](/reference/toastbuilder/set-activation-arguments.md)
