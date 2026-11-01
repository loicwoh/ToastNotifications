# Choose an example

Each focused example shows a complete application path: configure, display,
receive when applicable, and close.

| Example | What you learn | Validation |
|---|---|---|
| [Text reply](guides/reply.md) | Separate application arguments from user-entered text | Manual input capture, empty value, special characters and notification-history interaction |
| [Multiple actions](guides/multiple-actions.md) | Distinguish two buttons and body activation | Accept, Reject, body arguments and nominal Stop/restart |
| [Link button](guides/protocol.md) | Open a URI through Windows protocol activation | Manual opening of the configured link |

## Text reply

Open `Sources/Examples/Toast With Reply.vi`.

```text
Button arguments  → action=reject&requestId=42
Submitted input   → Reason = the text the user typed
```

This is the best place to start if you want a result in your LabVIEW event loop.
The [guide](guides/reply.md) includes the exact configuration and observed cases.

## Multiple actions

Open `Sources/Examples/Toast With Multiple Actions.vi`. The same User Event relay
receives `action=accept`, `action=reject` or `action=open`, each with request context.
There are no input controls, so an empty User Inputs array is expected.

## Link button

Open `Sources/Examples/Toast With Link Button.vi`. The button opens the configured
URL through Windows. Its Protocol action is distinct from an application callback.

## Coming next

Selection input, images, progression updates, sounds, button icons and context menus
are planned examples. They are not part of the implemented surface shown above.
See the [coverage matrix](coverage.md) for the corresponding issues.
