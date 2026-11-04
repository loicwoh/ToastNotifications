# Reuse a toast definition from XML

Once you have a notification design you like, you can reuse its XML in another application. `ToastFromXML` displays that definition through the same service and User Event handler used with `ToastBuilder`.

## Try it

Open `ToastAPI.lvproj` and run `Examples/Toast From XML.vi`. Enter a reason and click **Send**. Look for `action=reject&requestId=42` in `Activation.Arguments` and your text under `Reason` in `Activation.User Inputs`. Press **stop** after each run.

## Using this in your application

Export a design with `ToastBuilder.Get XML` and use it to create a `ToastFromXML` source. You can keep the same `ToastService` and activation handler. Preserve the action arguments and field IDs that your application reads when you edit the XML.

[ToastFromXML](/api/toastfromxml.md)
