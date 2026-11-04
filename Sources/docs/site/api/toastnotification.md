# ToastNotification

The toolkit's root library groups the application classes, handler implementations,
native wrappers and shared activation data types.

## Choose a layer

- **Application:** compose with [ToastBuilder](/api/toastbuilder.md) and manage the
  callback registration with [ToastService](/api/toastservice.md).
  [ToastSource](/api/toastsource.md) carries the common source contract.
- **Extension:** use the [ActivationHandler](/api/activationhandler.md) contract and
  the supplied [User Event implementation](/api/usereventactivationhandler.md).

These categories describe the current workflows. They do not change LabVIEW
access scope or establish a stable release API; that policy remains in
[#18](https://github.com/loicwoh/ToastNotifications/issues/18).

The root library includes `Activation.ctl` (raw Arguments and User Inputs) and
`Argument.ctl` (a Key/Value pair). The User Event delivery wrapper belongs to the
plugin, rather than adding an error field to Activation itself.

`Create ToastSource (Poly).vi` groups Create ToastBuilder for composition and
Create ToastFromXML for XML text. Each returns its concrete class type.
The caller closes the created source; this selector neither
initializes ToastService nor registers a callback.

<!-- API-MEMBERS -->
