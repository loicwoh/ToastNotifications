# MIT licence and third-party notices

Reviewed 2026-11-02 against develop `8e04d00`. The maintainer accepted MIT for
original code/documentation, with the explicit clarification that its warranty
and liability exclusions remain subject to applicable law. The licence grants
reuse rights; it promises no support, maintenance or updates. Copyright holder
is identified by the repository owner's public handle, `loicwoh`.

## Delivery

- Standard root MIT licence, without custom clauses changing its meaning.
- Third-party notices and retained licence texts, clearly outside the project's
  ownership claim. No NI, Microsoft or OpenAI software is relicensed as ToastAPI.
- Website legal page linked from navigation, search and footer. Exact source
  texts are published with each adopting branch/version, not copied into old
  branches as if they had adopted MIT. Archive extraction includes root notices.
- Microsoft notification DLL matched byte-for-byte to official NuGet 7.1.3,
  lib/net461; duplicate archival DLL is identical.
- Existing Docsify/Mermaid licence files and bundle comments remain unchanged;
  DOMPurify Apache licence, Lodash/Underscore attribution and pylabview format
  reference text are added. No runtime upgrade or asset minification is performed.

## Authorized removal of unused LGPL DLL

The maintainer selected removal if unused. All 73 saved .vi/.ctl files, including
archived prototype files, were extracted read-only with the bundled pylabview
reader. Extraction succeeded for all files. Neither the DLL filename, assembly
identity prefix nor public-key token `e89d9d7314a7c797` occurred in extracted
metadata/sidecars. Text projects/C# references also did not name this library.
Actual notification references point to Microsoft.Toolkit.Uwp.Notifications.
No VI was run, saved, or loaded into LabVIEW for this inspection.

The two `ToastNotifications.dll` files are identical to official NuGet 2.5.1,
lib/net40. They are removed from current Sources/bins and Sources/Archive/bins.
The archived project, VIs and C# sources are retained. The main workspace and its
nine uncommitted LabVIEW files are untouched. Dependency evidence is retained in
the ignored worktree `_review/license-evidence/dependency-scan.json`.

## Scope and remaining release work

This is not a claim of exhaustive legal clearance. Removal does not erase
historical Git copies. LGPL/GPL texts and the original upstream source link are
retained, but exact corresponding-source matching for historical binaries still
needs a release decision; notices alone are not asserted to fulfil all LGPL
obligations. No history rewrite or promise of future source provision was made.
The two DLLs were never a reason to relicense original ToastAPI code as LGPL.

A complete transitive licence inventory for the browser bundles is still a
release follow-up beyond the package licences and embedded notices checked here.
The maintainer's actual NI edition/contract and entitlement have not been
inspected. Future Runtime/driver bundling and VIPM packaging need their own
redistribution review. Normal source/site publication does not bundle Python,
LabVIEW, MCP, Codex, Windows or .NET runtimes.

## Verification

Strict documentation build and link checks, licence-asset publication tests,
existing inventory/detailed-help regressions and historical source build pass
for this change (27 automated checks). Publication tests verify exact licence
bytes and refuse a new legal page lacking its root notices; they also ensure
older documentation does not receive a new licence. These are documentation
checks, not legal adjudication or LabVIEW application execution tests.

Visual browser review remains unperformed: the automatic browser-origin approval
gate denied access to the local preview, first due to an account usage limit and
again on resumption because that origin remained blocked. No alternate browser
surface or indirect browser access was used. Maintainer visual review is required
before merge; automated local file/link checks do not substitute for it.
