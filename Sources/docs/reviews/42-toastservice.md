# ToastService detailed help — second delivery for #42

Reviewed 2026-11-02, based on ToastBuilder documentation commit `ae1661f` and
LabVIEW code from develop `c856044`. This branch is stacked on PR #52 until
that first documentation lot is merged. The main workspace's nine uncommitted
LabVIEW edits are preserved.

## Coverage

Five application methods follow the accepted Add Text model: Initialize,
Register For Events, Show, Read ActivationHandler and Close. The raw .NET
reference getter remains internal to the documentation boundary. The initialized
handler getter is application-facing, unlike that raw-handle accessor.

Each page preserves the exact saved short description and includes a native
icon/terminal PNG, terminal types/defaults and required inputs, error cue,
Mermaid scenario and ownership notes. JSON records fingerprint the method,
reviewed helpers/class and native image. Evidence came from native gRPC AIXML
exports and Print.VI To HTML over ActiveX with the pylabview render backend.
No product VI was executed.

## Authorized description correction

The initial Initialize description incorrectly said the VI accepted no handler.
The maintainer explicitly authorized its correction during this delivery.
`lvai_set_vi_descriptions` used native VI Server, with unsaved-change protection;
the saved STRG text matched the requested text, icon resources were unchanged,
and the tool reported no other file changes. Before/after native AIXML is
identical after excluding only the top-level description attribute. The native
connector image remains valid. No connector, panel, diagram or scope was edited.
Of the 82 LabVIEW source files, only `Sources/ToastService/Initialize.vi` changed.
Backup and comparison exports are retained in the ignored worktree review folder.

## Shutdown sequence: maintainer follow-up

At the maintainer's explicit request, the public Close help presents the target
order, with the code adjustment to be made by the maintainer afterward:

1. Stop/unregister the application's receiver.
2. Unregister the native callback.
3. Close handler resources, then release the service native reference.
4. Preserve/merge errors; the caller separately closes the builder.

**This delivery does not implement that sequencing.** Inspection of the current
Close diagram found independent native-unregistration and handler-close branches.
Close Reference receives the unregistration error and can be suppressed by it.
There is no callback drain or repeated-close guard. This handoff and #16 retain
the implementation gap; the public target must not be cited as tested behavior.
The incoming error is currently merged first without gating branch entry.

Other reviewed limits: Initialize has no rollback after partial acquisition;
Register For Events has no duplicate-registration guard; Show delegates to the
builder without checking service state; Read ActivationHandler returns a default
base value when the incoming error bypasses its read. The docs distinguish native
callback registration from the application's separate User Event registration.

## Validation

- Strict build and local Markdown/asset links pass.
- Twelve detailed-help and eight inventory regression checks pass.
- Repeated strict builds produce identical output and preserve authored files.
- All five routes render native images, Mermaid diagrams and the expected error
  cue in Chromium; Close says it executes even on incoming error.
- Native terminal images for all five methods and Initialize/Close block
  diagrams were visually inspected. Browser checks cover the corrected saved
  summary and the shutdown diagram. No application execution test is claimed.

Issue #42 remains open for ActivationHandler and UserEventActivationHandler.
