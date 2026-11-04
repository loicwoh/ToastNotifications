# Ask for a text reply

Ask someone why they rejected a request while they work outside your application. A **Send** button submits the reply, and a User Event brings it into the LabVIEW event loop.

## Try it

Open `ToastAPI.lvproj` and run `Examples/Toast With Reply.vi`. Type a reason, click **Send**, and look for `Reason` in `Activation.User Inputs`. Press **stop** after each run.

## What to look for

`Activation.Arguments` identifies the action and request (`action=reject&requestId=42`). The submitted text arrives under the field ID `Reason`. Look it up by key and distinguish an empty value from a missing entry.

[Add Text Input](/reference/toastbuilder/add-text-input.md)
