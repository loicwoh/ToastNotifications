# Multiple actions with a User Event — implementation guide

Status: preparation only. No VI or handler has been implemented for this scenario.
Tracked in [#6](https://github.com/loicwoh/ToastNotifications/issues/6) and
[#22](https://github.com/loicwoh/ToastNotifications/issues/22).

## Scenario

Suggested main VI: `Toast With Multiple Actions.vi` in this folder.
Show a request with two application-activation buttons, **Accept** and **Reject**.
Display received activation data in the main VI through a LabVIEW User Event.
Use the existing raw argument interface for now; this work does not implement #4.

| Click target | Proposed activation arguments |
|---|---|
| Notification body | `action=open&requestId=42` |
| Accept button | `action=accept&requestId=42` |
| Reject button | `action=reject&requestId=42` |

These are fixed demonstration strings, not a general-purpose encoding contract.
Initially display and compare the complete strings; do not introduce a partial
URL parser or concatenate arbitrary user input. Repeat the example to click each
target: clicking a button may consume the notification.

Use `ToastBuilder.Add Bouton` for application buttons, not `Add Link Button`:
Protocol activation is handled by Windows and does not relay this action to the handler.
Body launch arguments need their own builder configuration. Inspect the existing
native Add Argument helpers and toolkit behavior, then expose the smallest class
method necessary. Verify whether builder arguments are also inherited by buttons;
record the actual payload and adjust the fixed-string checks accordingly.

## Suggested components

| Component | Responsibility |
|---|---|
| `UserEventActivationHandler.lvclass` | Concrete child of ActivationHandler that forwards activations through a borrowed User Event reference |
| Handler configuration method | Stores the event reference before injection into Register For Events |
| `Handle Activation.vi` override | Copies activation and conversion error into an event payload, generates the event and returns promptly |
| Shared delivery typedef | Cluster containing `Activation` (existing Activation.ctl) and `Error` (standard error cluster) |
| Main example VI | Owns the User Event and its registration, handles incoming data and Stop, and closes resources |

Names are proposals to confirm while authoring. Keep each class/library in its
own flat folder; the reusable handler belongs to the toolkit, not inside the example.
Choose one owner for the delivery typedef so the future FIFO handler can reuse it.
Do not add .NET references to the event payload or modify Activation.ctl solely
to add an error field: the delivery wrapper carries the error separately.

## Authoring order

1. Define the delivery typedef and create the User Event in the example.
2. Create the handler child class and its event-reference data member. Use the
   native accessor/property conventions, class banner and virtual scope folders.
   Override Handle Activation with the native override facility, retaining its connector.
3. Implement only the relay. The handler borrows the configured event reference;
   it must not create/destroy the application's event or registration.
4. Register the User Event with an Event Structure inside the application's loop.
   Display the received Arguments, User Inputs and conversion error. Add a Stop event.
5. Configure the handler, initialize the service and inject the handler with
   Register For Events. Have the event registration ready before showing the toast.
6. Add text, the Accept and Reject buttons and body arguments, then show the toast.
7. Complete shutdown and documentation after the delivery path works.

First milestone: one application button reaches the main VI through the User Event.
Then add the second button and the distinct notification-body action.

## Errors and lifetime

- A conversion error arriving at Handle Activation is data to deliver, not a reason
  to silently suppress the event. Keep it in the payload. Ensure it does not cause
  Generate User Event to skip the send through its error input.
- Report an invalid event reference or generation failure through the handler's
  error output; define error precedence without losing the original conversion error.
  Do not claim a failed event was delivered.
- The callback must not wait for a response, show a dialog or close the service.
  Application work belongs in the receiving loop.
- Keep the event and its registration alive while a callback can use them.
  Stop notification production, unregister the callback and resolve callbacks
  already in progress before destroying communication resources. Decide how to
  handle already-delivered events and avoid waiting on the loop doing shutdown.
- The current service does not yet guarantee draining callbacks in progress.
  Coordinate with #16; a simple Close call or GC.Collect is not proof that event
  destruction is safe. Do not silently extend the concurrency guarantees.
- The application owns service closure, builder closure, event unregistration and
  event destruction. Copies of the handler share the borrowed event reference.

## Manual verification before review

- A first button activation reaches the receiving loop without blocking the callback.
- Accept, Reject and body clicks can be distinguished and retain request context.
- Received data matches what the toolkit actually emits; record body/button inheritance.
- Conversion errors remain observable; invalid event references fail visibly.
- Repeated activations do not require restarting LabVIEW.
- Stop closes resources under the documented supported conditions; pending callback
  limitations are explicit and not advertised as solved without verification.
- Context help, parameter descriptions and this guide match the final implementation.

No framework installation or unit-test suite is part of this preparation.
