# Getting started

Start with an example before composing your own notification.

## Current environment

The project is developed in **LabVIEW 2026 on Windows**, with
`Microsoft.Toolkit.Uwp.Notifications`. Required DLLs are kept in `Sources/bins`.
The wrapper currently uses the Windows Community Toolkit notification APIs;
examples written for `Microsoft.Windows.AppNotifications` are a different API.

LabVIEW 2020 distribution is planned for evaluation, not currently verified.
There is no released VIPM package yet. See the [compatibility status](coverage.md).

## Open the project

1. Open `Sources/ToastAPI.lvproj` in LabVIEW.
2. Open `Sources/Examples/Toast With Reply.vi`.
3. Run it, enter a reason in the Windows notification, and click **Send**.
4. Look at the example's `Activation` indicator. `User Inputs` should contain the
   key `Reason` and the submitted value.
5. Press **stop** in LabVIEW to leave the event loop and allow cleanup.

Running an example displays a real Windows notification. Its presentation and
visibility also depend on the user's Windows notification settings.

The [reply guide](guides/reply.md) includes the full configured values, observed
results and a distinction between callback errors and the final example error.

## Build your own application flow

1. Create a builder and add texts, inputs and application buttons as required.
2. Initialize `ToastService` with a handler instance.
3. If using `UserEventActivationHandler`, retrieve the initialized handler and read
   its `Event Ref`. Register that event with your application's Event Structure.
4. Register the native callback with `ToastService.Register For Events`.
5. Show the toast and process delivered values in your receiving loop.
6. Stop the receiving flow and release resources according to the
   [ownership contracts](callbacks.md).

Use the **initialized handler returned by the service**, rather than the original
class value, when retrieving references created by its Initialize hook.

## Which example should I open?

| Goal | VI |
|---|---|
| Receive entered text | `Toast With Reply.vi` |
| Distinguish several actions | `Toast With Multiple Actions.vi` |
| Open a URL | `Toast With Link Button.vi` |

These files are in `Sources/Examples`. The older `Build Toast With Classes.vi`
and `Native Toast Example.vi` remain in the project; use the focused examples above
for the current documented application workflow.
