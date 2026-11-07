# Reflection DotNet

Repository-only implementation notes; this library is outside the published
application API. Membership and scopes are defined by the saved
[library file](../../Reflection%20DotNet/Reflection%20DotNet.lvlib).

Reusable low-level helpers for inspecting .NET objects, reading properties,
invoking interface methods and releasing acquired references.

## Boundary and dependencies

[ToastService](../../ToastService/ToastService.lvclass) uses these operations while converting native
activation data. Application handlers receive copied LabVIEW values and do not
need to repeat the reflection work.

Helpers use native objects and reflection metadata. A returned object value and
an alias of an input reference have different ownership; consult each saved
description. Closing a LabVIEW handle, disposing an enumerator and collecting
.NET objects are distinct operations.

This is an implementation layer. See [reflection concepts](../site/concepts.md),
[callback ownership](../site/callbacks.md) and the
[Microsoft directory](../site/microsoft.md) for context.
