# Multiple actions with a User Event

Open `ToastAPI.lvproj`, then `Examples/Toast With Multiple Actions.vi`.
The example and User Event handler have been implemented manually. This guide describes
the current code, tracked in [#6](https://github.com/loicwoh/ToastNotifications/issues/6)
and [#22](https://github.com/loicwoh/ToastNotifications/issues/22).

The example creates its concrete ToastBuilder through `Create ToastSource (Poly)`
(Create ToastBuilder instance). Composition and XML export use the builder;
`ToastService.Show` accepts it as a ToastSource and dynamically calls the
builder Show override. The example retains ownership and closes the builder
after the service. This does not load an external XML file.

## Trying the example

1. Run the VI. The toast displays **Request #42**, **Do you accept this request?**,
   and the **Accept** and **Reject** buttons.
2. Click one target and inspect `Activation.Arguments` on the example's front panel.

| Click target | Configured raw arguments |
|---|---|
| Notification body | `action=open&requestId=42` |
| Accept button | `action=accept&requestId=42` |
| Reject button | `action=reject&requestId=42` |

3. The User Event updates the `Activation` and `error` indicators without stopping
   the loop. These indicators show the most recently received payload, not a history.
4. Press **stop** to leave the receiving loop and allow cleanup.
5. Run again to try another target if Windows has removed the notification.

The example uses fixed diagram constants and displays raw strings. It does not
implement the typed argument API planned in #4 or parse arbitrary key/value data.
`Toast XML` contains the serialized toast before display: inspect its `launch`
attribute for the body and the action arguments for the buttons.

## Arguments versus User Inputs

`action` and `requestId` are application-provided activation arguments. They are
returned in `Activation.Arguments`, not as entries in `Activation.User Inputs`.

This example has no text input or selection control, so an empty `User Inputs`
array is expected. To receive input values, add an input control with a stable ID
and submit it through an appropriate application-action button. Input IDs and
submitted values then appear as Key/Value pairs. Displayed text is not input data.

## Construction and body activation

The builder sequence is Create, two Add Text calls, two Add Bouton calls,
Set Activation Arguments and Get XML. The old introductory text calls were removed:
adding them as well exceeded the toolkit's text capacity; the question mark is valid.

`ToastBuilder.Set Activation Arguments` takes the raw string `launchArgs` and fixes
body activation to Foreground. Its native helper, `Toast Native.Add ToastActivation Info`,
calls `AddToastActivationInfo(launchArgs, activationType)` on the borrowed builder.
This replaces the body's launch string; it does not append or parse arguments.
Each button keeps the arguments configured through Add Bouton.

These are application activations, unlike Add Link Button, whose Protocol action
is handled by Windows rather than the LabVIEW handler.

## Handler and receiving loop

| Component | Current responsibility |
|---|---|
| `ActivationHandler` | Base dynamic-dispatch Initialize, Handle Activation and Close hooks |
| `UserEventActivationHandler.Initialize` | Creates a typed User Event and stores its reference |
| `Activation Event Data.ctl` | Delivery cluster with `Activation` and `error` |
| `UserEventActivationHandler.Handle Activation` | Bundles the activation and conversion error, then generates the User Event |
| `UserEventActivationHandler.Close` | Destroys the owned User Event and merges cleanup errors with its incoming error |
| Main example | Borrows the event reference, owns its event registration, receives data and controls shutdown |

The reusable handler is in `Sources/PlugIns/UserEventActivationHandler`; it is not
an example-only class. No .NET reference crosses the User Event payload.

Initialize ToastService **with** the handler instance. The service calls the
handler's Initialize hook, stores the returned initialized instance, and also
returns it to the caller. The example casts that result to UserEventActivationHandler
and reads its Event Ref property. Using the original pre-initialization class value
would not retrieve the reference created by Initialize.

The example registers the User Event with the application's Event Structure, then
registers the native callback through ToastService.Register For Events and shows
the toast. The receiving loop starts only if setup and Show succeed. Its Stop case
ends the loop; its User Event case displays the received activation and conversion error.

## Errors and resource ownership

The conversion error is bundled into the User Event payload. It is not wired into
Generate User Event's error input, so an incoming conversion error does not itself
suppress the send. The `error` indicator displays that delivered conversion error;
the example's `error out` is its final setup/cleanup result.

The current handler does not expose the error output of Generate User Event.
Invalid references and delivery failures therefore still need an explicit diagnostic
contract and validation before #22 is considered complete. An unchanged display
does not prove that a new event was delivered.

The handler owns the User Event; the application borrows its reference for registration
and must not destroy it independently. The application owns and unregisters its
Event Registration Ref. Copies of the handler share the same underlying event.

After the loop, the example attempts to unregister its event registration, close
the service (including the handler Close hook), close the builder and perform the
existing final System.GC.Collect workaround. The setup-error path skips the wait
and proceeds to cleanup. This sequence does not establish that concurrent callbacks
have drained: callbacks in progress, repeated initialization/closure and partial
failures remain part of [#16](https://github.com/loicwoh/ToastNotifications/issues/16).
Do not destroy a resource while a callback may still use it, wait for application
work inside the callback, or close the service from Handle Activation.

## Validation status

The user confirmed the nominal User Event reception path, the button actions,
Stop/restart without quitting LabVIEW, and body activation returning
`action=open&requestId=42`. The three configured targets are covered by this manual
validation for #6. No additional notification was emitted during documentation or delivery.

The native body-activation helper, the public method and the example have been
checked executable, with saved context-help text and icons verified. Conversion-error
delivery, invalid event references, event-generation failures and shutdown during
an active callback still require dedicated validation for #22/#16. No unit-test
framework has been added.
