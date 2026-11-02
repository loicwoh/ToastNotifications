# Toast with a reply input

Open `ToastAPI.lvproj`, then `Examples/Toast With Reply.vi`.
This example implements the text-input scenario tracked in
[#7](https://github.com/loicwoh/ToastNotifications/issues/7), using the existing
UserEventActivationHandler to forward the submitted value to a LabVIEW event loop.

The example creates its concrete ToastBuilder through `Create ToastSource (Poly)`
(Create ToastBuilder instance). Composition and XML export use the builder;
`ToastService.Show` accepts it as a ToastSource and dynamically calls the
builder Show override. The example retains ownership and closes the builder
after the service. This does not load an external XML file.

## Try it

1. Run the VI. Windows displays the notification described below.
2. Enter a reason in the text field and click **Send**.
3. Inspect `Activation.Arguments` and `Activation.User Inputs` on the front panel.
4. Press **stop** after trying the notification. Receiving a reply does not stop the VI.
5. Run again to submit a different value if Windows has removed the notification.

| Element | Value configured in the example |
|---|---|
| First text | `Request #42` |
| Second text | `Why do you reject this request?` |
| Input ID | `Reason` |
| Input title | `Reason for rejection` |
| Input placeholder | `Enter your reason` |
| Button content | `Send` |
| Button arguments | `action=reject&requestId=42` |

These values are diagram constants. The example uses two Add Text calls,
Add Text Input and the existing Add Bouton method. It does not use Protocol activation
or configure a separate body action. Clicking Send is the intended submission path.

## Reading the result

With the text `too bussy` shown in the user's validation capture, the expected result is:

```text
Activation.Arguments = action=reject&requestId=42
Activation.User Inputs = [{Key: Reason, Value: too bussy}]
```

Arguments carries application context supplied before display. User Inputs carries
the submitted field value. The ID `Reason` is the returned Key; neither the visible
input title nor the placeholder becomes the key. Look up entries by Key, not by
array index. A missing entry and an entry whose Value is empty are different cases.
The current example displays the complete cluster rather than implementing that lookup.

`Toast XML` is the notification serialized before display. The `input` element uses
`id="Reason"`; the `action` contains the Send arguments. The XML represents `&` as
`&amp;`, while the activation string returned to the application uses the raw character.
Text typed after display is returned through the callback, not inserted into this
pre-display XML indicator.

## Callback and receiving loop

The example passes a UserEventActivationHandler instance to ToastService.Initialize.
The service initializes and retains that handler. The example retrieves the returned
initialized instance, casts it to the concrete handler and reads Event Ref. It creates
its own event registration before registering the native callback and showing the toast.

The While Loop contains a User Event case that updates `Activation` and `error`,
and a Stop case that ends the loop. The indicators show the most recent payload;
they do not retain a history. The `error` indicator contains the conversion error
delivered alongside Activation. The separate `error out` is the final example result.

The handler owns its User Event and destroys it from its Close hook. The application
borrows the event reference and owns the event registration. After Stop, the example
attempts to unregister that registration, close the service and handler, close the
builder and perform the existing final System.GC.Collect workaround. Setup/Show
errors skip the wait and proceed to cleanup. This does not establish a guarantee
that callbacks in progress have drained; see #16. Event-generation error reporting
and invalid-reference handling remain part of #22.

## Button layout

The implemented Send button is a standard application-action button below the input.
The submitted XML does not contain an explicit `hint-inputId` association or a button
icon. This is sufficient for the demonstrated input capture; an inline quick-reply
button beside the field is a separate presentation enhancement, not a feature claimed
by this example.

If that layout is implemented later, inspect the toolkit's TextBoxId/SetTextBoxId and
ImageUri requirements, keep native references encapsulated, and validate the rendered
result and resource deployment paths.
[ToastButton API](https://learn.microsoft.com/en-us/dotnet/api/microsoft.toolkit.uwp.notifications.toastbutton?view=win-comm-toolkit-dotnet-7.0).

## Validation

The user's captures show the displayed Reason field, the entered text `too bussy`,
and the received User Inputs pair `Reason` / `too bussy`. The saved diagram configures
the complete action/context string shown above. The VI is executable and its help
describes the current implementation. The documentation update does not emit another toast.

The user also confirmed the expected behavior when clicking outside the toast,
closing the notification and interacting with it from Windows notification history.
These observations do not claim that dismissal generates an activation callback;
the exact callback payload for each interaction has not been separately recorded.

The user additionally confirmed these submissions:

- Empty submission: User Inputs contains Key `Reason` with an empty Value; the key is not omitted.
- Special characters: `Réponse & pièce <manquante> "à fournir"` is returned unchanged,
  including accents, ampersand, angle brackets and quotation marks.
- Several submissions with different values were received during these checks.

These results were reported explicitly by the user, rather than inferred from the captures.
Broader lifecycle guarantees and handler delivery failures remain tracked separately
in #16/#22. No unit-test framework has been added. The older Build Toast With Classes
example is still present; it has not been deleted or renamed as part of this work.
