# Ask for a text reply

Ask someone why they rejected a request while they work outside your application. A **Send** button submits the reply, and a User Event brings it into the LabVIEW event loop.

## Try it

Open `Toast Notification Examples.lvproj` and run `Toast With Reply.vi`. Type a reason, click **Send**, and look for `Reason` in `Activation.User Inputs`. Press **stop** after each run.

## Using this in your application

Look up the reply by its field ID (`Reason`) so the lookup still works if you add other fields. A present entry with an empty value means the field was submitted blank. A missing entry means the activation did not carry that field.

[Add Text Input](/reference/toastbuilder/add-text-input.md)
