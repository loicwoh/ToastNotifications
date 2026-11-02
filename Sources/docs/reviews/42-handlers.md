# Activation handler detailed help — final class lot for #42

Reviewed 2026-11-02 against committed develop `dd2e5ec`, after merging approved
ToastBuilder PR #52 and ToastService PR #53. The main workspace's nine
uncommitted LabVIEW files, including the plugin Handle Activation, were not
used or changed. This delivery documents committed sources only.

## Scope and evidence

Seven detailed pages cover the three ActivationHandler hooks and four
UserEventActivationHandler application methods (including Read Event Ref).
The private event-reference writer remains outside the application reference.
Public payload types are explained at their method terminals; their generated
reference summaries remain available. All 21 application VIs across the four
classes now have authored detailed help.

Review used native gRPC AIXML for eight methods/accessors, and native LabVIEW
Print.VI To HTML over ActiveX (pylabview rendering backend). The seven published
icon/terminal PNGs are unchanged copies of those exports. Their hashes and
reviewed method/helper/class hashes are retained in adjacent JSON records.
Images and the base/plugin delivery and plugin cleanup diagrams were visually
inspected. No product VI was executed or saved, and all 82 LabVIEW source hashes
remain unchanged in this worktree.

## Important distinctions

- All three base hooks are empty. Initialize and Close preserve their existing
  error output; Handle Activation has no outputs and forwards nothing. A new
  `noop` metadata cue makes the empty implementation visible without incorrectly
  implying an error-gated action or cleanup acquisition.
- The saved base Handle Activation description says it propagates the error,
  despite the absent output. The plugin Handle Activation saved description
  repeats that base text. The detailed pages preserve those exact summaries but
  explicitly clarify the real connector and implementation. No description was
  rewritten here, especially not the user's locally edited plugin VI.
- Plugin Initialize and Read Event Ref skip work on incoming error. Initialize
  returns the new class value; the original pre-initialized value gains no event.
- Plugin Handle Activation attempts event generation even on conversion error:
  Activation and error are bundled as payload. Generate User Event's error input
  is not wired to the conversion error; its error output is not surfaced.
  Event-ref read errors are also not exposed in this method. Diagnostics remain
  tracked in #22, without claiming verified delivery in this review.
- The handler owns the typed User Event. The application borrows it and owns
  its separate receiving Event Registration Ref. Plugin Close attempts event
  destruction even on incoming error, merging the primary error first.
- No repeated-initialization/closure guard, field clearing, partial-setup
  rollback or callback drain is added. Shutdown diagrams follow the maintainer's
  approved target from the ToastService lot. The current service still requires
  the sequencing adjustment documented in [42-toastservice.md](42-toastservice.md)
  and #16; this delivery does not implement or validate that future sequence.

## Validation

- Strict build and local Markdown/asset link checks pass.
- Thirteen detailed-help checks (including the new no-op cue) and eight inventory
  regressions pass. These are documentation-pipeline tests, not LabVIEW tests.
- Two consecutive final builds are byte-identical and preserve authored sources.
- Chromium renders all seven routes, native images, Mermaid diagrams and exact
  no-op/skip/always cues. Delivery scenario and connector layout were inspected.
- Existing saved VI Help URLs and the application/internal API boundary remain
  unchanged. No new public support-library pages are introduced.

PR review completes this documentation lot; the functional gaps above remain
separate work. The remaining inherited-summary corrections can be made alongside
the maintainer's pending local code changes, then their fingerprints re-reviewed.
