# Reply input — implementation guide

Status: preparation only for [issue #7](https://github.com/loicwoh/ToastNotifications/issues/7).
The owner will implement the VIs manually. Reuse the existing UserEventActivationHandler;
this scenario does not require the argument API redesign in #4 or ToastSource work.

## Scenario and configuration

Ask for a reason to reject request #42. Use only these two text elements, without
keeping extra introductory Add Text calls from the source example.

| Method/input | Value |
|---|---|
| First Add Text | `Request #42` |
| Second Add Text | `Why do you reject this request?` |
| Add Text Input: id | `Reason` |
| Add Text Input: Title | `Reason for rejection` |
| Add Text Input: Placeholder Text | `Enter your reason` |
| Application button: Content | `Send` |
| Application button: Arguments | `action=reject&requestId=42` |

The input ID is a stable key, not the visible title or placeholder. Use the exact
case `Reason` when looking up the submitted value. The button must use application
activation; Add Link Button uses Protocol and is not appropriate here.

## Starting point

Prefer evolving the existing `Build Toast With Classes.vi`, which already contains
a text input and a reply button, rather than keeping two equivalent reply demos.
Suggested final name: `Toast With Reply.vi`. If you rename it, do so through LabVIEW,
update project links and the examples index, and preserve its existing useful content.

Use `Toast With Multiple Actions.vi` as the reference for the working handler,
User Event registration, receiving loop and Stop sequence. Keep the multiple-action
example itself unchanged: it demonstrates a different scenario.

## First milestone: receive text

1. Configure the builder as in the table. A standard application button is sufficient
   for the first capture check; explicit input association is the next milestone.
2. Pass a UserEventActivationHandler instance to ToastService.Initialize.
3. Retrieve the initialized handler, cast to its concrete class and read Event Ref.
   Register that User Event with the receiving Event Structure before displaying the toast.
4. Call ToastService.Register For Events and Show using the existing pattern.
5. Keep the Event Structure in a While Loop. In its User Event case, display the
   delivered Activation and conversion error. Find the User Inputs entry by Key
   `Reason`, rather than assuming an array index. Distinguish a missing key from
   a present key with an empty value.
6. Stop exits the loop and follows the existing cleanup sequence. Receiving the
   reply updates the indicators and leaves the loop running.

For a reply such as `Missing information`, the expected payload is:

```text
Activation.Arguments = action=reject&requestId=42
Activation.User Inputs = [{Key: Reason, Value: Missing information}]
error.status = false
error.code = 0
```

The action and request ID are application context in Arguments. The user's text
is in User Inputs; it does not automatically become part of the Arguments string.
Displayed text, placeholder and input title are not submitted values.

## Second milestone: associate the reply button with the input

Inspect the installed native AddButton overloads accepting a textBoxId, or configure
a ToastButton through SetTextBoxId before adding it. In both cases the association
must name the existing input ID `Reason`.

Keep the .NET details inside Toast Native and ToastBuilder. A dedicated public
`Add Reply Button` is one possible interface to review; preserve existing callers
of Add Bouton if its interface is changed instead. Native button objects acquired
along this path need explicit ownership and cleanup.

The toolkit documents an image URI as required for a button displayed beside the
input. Include a redistributable local icon and correct deployment paths if choosing
that layout; do not promise inline rendering from TextBoxId alone. Verify the final
rendering and inspect Toast XML for the input ID, action arguments and association.

Reference: [ToastButton API, TextBoxId and ImageUri](https://learn.microsoft.com/en-us/dotnet/api/microsoft.toolkit.uwp.notifications.toastbutton?view=win-comm-toolkit-dotnet-7.0).

## Manual checks and completion

- Type a normal sentence, click Send and verify Arguments plus the Reason Key/Value.
- Try `Réponse : délai dépassé & pièce <manquante> "à fournir"` and verify the text
  survives unchanged. Encoding in Toast XML is distinct from the returned string.
- Submit an empty field. Record whether Windows delivers Reason with an empty value
  or omits it; handle that result explicitly without treating it as a conversion error.
- Repeat the run with a different reply and verify reception in the application loop.
  Re-show the toast if a click removes it.
- Press Stop and restart without quitting LabVIEW. The handler owns its User Event;
  the application owns only the event registration and must not destroy the event itself.
- Verify the explicit reply-button association and any icon path on the target machine.
- Update the VI/parameter context help, examples index and this guide to describe
  the actual implementation and observed results before delivery.

Do not extend lifecycle guarantees: delivery failures/invalid references remain
part of #22 and in-flight callback shutdown remains in #16. No framework installation
or unit-test suite is required. This preparation has not run or changed any VI.
