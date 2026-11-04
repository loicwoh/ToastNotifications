# Reuse a toast definition from XML

Once you have a notification design you like, you can reuse its XML in another application. `ToastFromXML` displays that definition through the same service and User Event handler used with `ToastBuilder`.

## Try it

Open `ToastAPI.lvproj` and run `Examples/Toast From XML.vi`. Enter a reason and click **Send**. Look for `action=reject&requestId=42` in `Activation.Arguments` and your text under `Reason` in `Activation.User Inputs`. Press **stop** after each run.

## What to look for

The XML defines the action arguments and the field ID. The submitted text arrives separately at runtime. To try your own design, replace the example’s XML string with the output of `ToastBuilder.Get XML`.

[ToastFromXML](/api/toastfromxml.md)
