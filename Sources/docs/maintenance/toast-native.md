# Toast Native

Repository-only implementation notes; this library is outside the published
application API. Membership and scopes are defined by the saved
[library file](../../Toast%20Native/Toast%20Native.lvlib).

Direct wrappers around Microsoft.Toolkit.Uwp.Notifications calls. This library is
the low-level implementation layer used by [ToastBuilder](../../ToastBuilder/ToastBuilder.lvclass).

## Boundary and dependencies

Members operate on native .NET references. Their saved descriptions define the
specific inputs, borrowed aliases and acquired results. Technical Public scope
does not make every helper an independent application-level API.

For example, the native Add Link Button fixes
protocol activation and passes the URI through the toolkit overload. The
[application method](../reference/toastbuilder/add-link-button.md) hides that native
configuration. Other helpers support builder or button construction, arguments,
content serialization and display.

Prefer the class workflow in application code. When maintaining this library,
trace acquisition and release through the caller and consult
[reflection helpers](reflection-dotnet.md) where applicable.

