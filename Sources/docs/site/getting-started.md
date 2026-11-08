# Getting started

Start with an example before composing your own notification.

## Current environment

The project is developed in **LabVIEW 2026 on Windows**, with
`Microsoft.Toolkit.Uwp.Notifications`. Required DLLs are kept in `Sources/bins`.
The wrapper currently uses the Windows Community Toolkit notification APIs;
examples written for `Microsoft.Windows.AppNotifications` are a different API.

The development sources and examples are saved in LabVIEW 2020 format. The
published v1.0.0 VIPM package targets LabVIEW 2026 64-bit. See the
[compatibility status](coverage.md) for the tested configurations.

## Open the examples project

For a VIPM installation, download the `.vip` from the
[GitHub release](https://github.com/loicwoh/ToastNotifications/releases) and install
it with VIPM for LabVIEW 2026 64-bit on Windows.

1. Open [the examples project](examples.md) from a source checkout or a VIPM installation.
2. Select `Toast With Reply.vi` in the project.
3. Run it, enter a reason in the Windows notification, and click **Send**.
4. Look at the example's `Activation` indicator. `User Inputs` should contain the
   key `Reason` and the submitted value.
5. Press **stop** in LabVIEW to leave the event loop and allow cleanup.

Running an example displays a real Windows notification. Its presentation and
visibility also depend on the user's Windows notification settings.

The [reply guide](guides/reply.md) includes the full configured values, observed
results and a distinction between callback errors and the final example error.

## Build your own application flow

1. [Create a builder](/reference/toastbuilder/create-toastbuilder.md) directly or through Create ToastSource (Poly), then add texts, inputs and application buttons as required.
2. [Initialize ToastService](/reference/toastservice/initialize.md) with a handler instance.
3. If using [UserEventActivationHandler](/api/usereventactivationhandler.md), retrieve the initialized handler and read
   its `Event Ref`. Register that event with your application's Event Structure.
4. Register the native callback with [ToastService.Register For Events](/reference/toastservice/register-for-events.md).
5. [Show the toast](/reference/toastservice/show.md) and process delivered values in your receiving loop.
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
| Display a toast from XML | `Toast From XML.vi` |

These four VIs are in `Sources/Examples`. The two development VIs are available
in the **Development Examples** folder of `Toast Notifications.lvproj`.
