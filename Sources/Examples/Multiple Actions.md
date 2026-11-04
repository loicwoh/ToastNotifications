# Offer a choice in a toast

Let an operator accept or reject a request without switching back to LabVIEW. Application-action buttons carry distinct arguments, and a User Event delivers the selection.

## Try it

Open `ToastAPI.lvproj` and run `Examples/Toast With Multiple Actions.vi`. Click **Accept**, **Reject**, or the toast body and inspect `Activation.Arguments`. Run again to try another choice. Press **stop** after each run.

## Using this in your application

Give each action a stable ID so you can change or translate the button labels independently. Use `action` to choose what happens next and `requestId` to find the affected item, even if the operator has since selected another request in LabVIEW.

[Set Activation Arguments](/reference/toastbuilder/set-activation-arguments.md)
