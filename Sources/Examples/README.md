# Examples

Open `../ToastAPI.lvproj` before opening the examples.

| VI | Purpose | How to try it |
|---|---|---|
| `Toast From XML.vi` | XML-string source displayed through the common service, with a text reply | Run, type a reason, click Send, inspect Activation, then press stop. See [the guide](Toast%20From%20XML.md). |
| `Toast With Reply.vi` | Text input submitted with application context and relayed through UserEventActivationHandler | Run, type a reason, click Send, inspect User Inputs under Key Reason, then press stop. See [the guide](Reply%20Input.md). |
| `Build Toast With Classes.vi` | Public class workflow with text input and an application-action button | Run, enter a reply, click the button, then press Stop. The current base handler does nothing; inject a derived handler to consume the activation data. |
| `Toast With Link Button.vi` | Public class workflow with a protocol-activation button | Run, click Open project on GitHub, then press stop in LabVIEW. See [the guide](Protocol%20Activation.md). |
| `Toast With Multiple Actions.vi` | Accept/Reject buttons and body arguments relayed through UserEventActivationHandler | Run, click a button or the body, inspect Activation.Arguments, then press stop. User Inputs is empty because there are no input controls. See [the guide](Multiple%20Actions.md). |
| `Native Toast Example.vi` | Lower-level toolkit calls | Inspect the diagram before running. Prefer the class examples for application code. |

Running an example can display a Windows notification. The class examples remain
active until their Stop event, then close the service and concrete source and perform the
existing final .NET collection workaround. A protocol button opens its URI through
Windows; it does not send that button action to the application's activation handler.

The historical prototype remains in `../Archive/SandBox`.
