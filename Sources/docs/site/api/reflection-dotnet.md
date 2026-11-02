# Reflection DotNet

Reusable low-level helpers for inspecting .NET objects, reading properties,
invoking interface methods and releasing acquired references.

## Boundary and dependencies

[ToastService](/api/toastservice.md) uses these operations while converting native
activation data. Application handlers receive copied LabVIEW values and do not
need to repeat the reflection work.

Helpers use native objects and reflection metadata. A returned object value and
an alias of an input reference have different ownership; consult each saved
description. Closing a LabVIEW handle, disposing an enumerator and collecting
.NET objects are distinct operations.

This is an implementation layer. See [reflection](/concepts.md?id=reflection),
[callback ownership](/callbacks.md) and the
[Microsoft directory](/microsoft.md) for context.

<!-- API-MEMBERS -->
