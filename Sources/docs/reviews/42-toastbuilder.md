# ToastBuilder detailed help — first delivery for #42

Reviewed 2026-11-02 against committed develop revision
`c8560442a9ac71e3bec81900c8cd18cff38635ce`, in an isolated worktree.
The user's uncommitted LabVIEW edits were not used, saved or changed.

## Coverage and evidence

All nine application methods now follow the approved Add Text model: Create,
Add Text, Add Text Input, Add Bouton, Add Link Button, Set Activation Arguments,
Get XML, Show and Close. Short descriptions come directly from saved VIs.
Native LabVIEW icon/terminal exports are preserved as PNGs; connector panes are
not redrawn. Each authored JSON record captures source/helper hashes, image
hash, review method and incoming-error behavior.

Inspection used native gRPC AIXML exports and LabVIEW Print.VI To HTML through
ActiveX for the new images. No product VI was executed or saved. Hash comparison
of all 82 versioned LabVIEW source files before and after inspection found no change.

Close releases its handle even on incoming error and merges the primary error
first. The other eight methods skip work on incoming error. Get XML closes its
temporary content reference. Add Bouton still acquires a temporary native button
without an explicit release in the wrapper: the help records this existing
lifetime limitation and points to #16; this documentation change does not fix it.

## Application boundary

The public site covers ToastBuilder, ToastService, ActivationHandler and its
UserEventActivationHandler plugin, plus their root library and public payloads.
Reflection DotNet and Toast Native notes live under `maintenance/` in the repo.
Their pages are excluded from current navigation, generated routes and inventory.
Raw .NET reference accessors and Builder Reference storage are implementation
details even while their saved scope is Public. No scope was changed in LabVIEW.

The current generated inventory has five owners and 24 entries (21 application
VIs and three payload types). All 23 saved class-VI Help URLs remain mapped;
internal accessor URLs resolve to small redirects-by-link to their class methods,
without advertising the accessor in navigation/search routes. Historical versions
without these audience flags retain their own boundary.

## Validation

- Strict build and local Markdown/asset link checks pass.
- Twelve detailed-help and eight inventory regression checks pass, including
  internal accessor exclusion and owners later moved to Community scope.
- Two consecutive strict builds produce identical files and preserve authored
  Markdown, JSON and native images.
- The current builder can still build the historical #39 source tree.
- All nine help routes render in Chromium, including their native images,
  Mermaid diagrams and exact skip/always error cues. Representative connector,
  Get XML sequence and Close pages were visually inspected.
- At a 390 px emulated viewport, the native image fits and wide tables scroll
  horizontally. Table wrapping was adjusted to prevent single-letter type names.
  This is browser emulation, not a physical-device test.

## Remaining work

Issue #42 stays open. Subsequent deliveries cover ToastService, then
ActivationHandler and UserEventActivationHandler with the same evidence model.
This first delivery neither extends toolkit behavior nor changes LabVIEW scopes.
