# ToastBuilder

Compose a notification by calling the native builder through a LabVIEW class.
Start with Create, add the required content and inspect Get XML when useful.
Display through the application's [ToastService](/api/toastservice.md) workflow.

## Boundary and dependencies

This class uses [Toast Native](/api/toast-native.md). Its methods change the native
builder directly; there is no separate LabVIEW content engine. The class exposes
composition methods for displayed text, text input, application buttons, protocol
buttons and body arguments. Loading saved XML remains planned.

One caller owns Close. Copies of the class share a handle, so closing an alias
affects the other copies. See [resource ownership](/callbacks.md).

The native reference accessor and its data type are listed for completeness.
Ordinary application examples use the class methods instead of manipulating
the underlying .NET handle.

<!-- API-MEMBERS -->
