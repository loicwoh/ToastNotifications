# LabVIEW theme and diagram cleanup delivery

Reviewed 2026-11-02 against develop `c8656c6`. The maintainer applied the theme
and explicitly authorized delivery of the previously modified diagram cleanup
alongside it. The 56 saved LabVIEW files are supplied by the maintainer: 50 VIs,
two controls and four class XML files. The reviewer did not rewrite or save any
of these files. Hashes taken before inspection still match after it.

## Theme and documentation

Native class/method icon exports use the approved visual families: Builder blue,
Service teal and Handler violet, with the User Event plugin in the handler
family. Support helpers and the example cleanup are included as provided.
The shared convention remains in [VISUAL-IDENTITY.md](../VISUAL-IDENTITY.md).

All 21 detailed-help native icon/terminal illustrations have been refreshed from
LabVIEW's Print.VI To HTML over ActiveX (pylabview render backend), without image
redrawing or recoloring. Each illustration was visually inspected. Adjacent JSON
records retain their original review history and record the new source/image
hashes and this maintenance review. Authored usage contracts and error cues are
unchanged. The website theme itself is unchanged.

## Verification

- Native gRPC AIXML exports succeeded for all 50 changed VIs.
- Public connector names, slot indexes, types, defaults and connection settings
  match the prior reviewed native exports for all 21 application VIs. Saved
  short descriptions match the develop baseline for all 21 as well.
- All 50 changed VIs report `eIdle`, with error lists read successfully and no
  errors. No product VI was executed: there was no toast, interactive test,
  notification delivery test or LabVIEW unit-test run.
- No active LabVIEW project and no unsaved main-instance VI changes were
  reported before inspection. No project was closed or saved by the reviewer.
- Class-member inventory/scope checks found no member or scope changes. The
  service class serialization changes Register For Events' InvokeUsage from 3
  to 0; its public connector and executable state remain intact. Native icon
  editor serialization also changes and includes generated whitespace; it was
  preserved rather than rewritten solely to satisfy a text whitespace check.
- The strict documentation build, saved help-link checks and 27 Python
  documentation regressions pass. Staged Git blobs also match every refreshed
  review fingerprint, including normalized XML owner hashes. Source snapshots and native exports
  are retained in the ignored `_review/theme-delivery` directory.

The maintainer describes the diagram changes as cosmetic. Interface and
executability checks support this delivery, but do not establish functional
equivalence of every rewritten wire. Existing #16/#22 lifetime/delivery limits
and the pending service shutdown sequencing are not claimed resolved by a theme
change. No API expansion or new runtime dependency is introduced.
