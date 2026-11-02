# Third-party notices

ToastAPI's original LabVIEW code, Python/site code and authored documentation
are licensed under the root [MIT License](LICENSE), copyright (c) 2026 loicwoh.
Third-party components and material retain their respective licences and
copyrights. The project licence does not relicense NI, Microsoft or other
third-party software, trademarks or linked documentation.

## Redistributed notification library

**Microsoft.Toolkit.Uwp.Notifications 7.1.3** — MIT.

Copyright (c) .NET Foundation and Contributors. All rights reserved.

The copies under `Sources/bins/` and `Sources/Archive/bins/` are identical to
`lib/net461/Microsoft.Toolkit.Uwp.Notifications.dll` from the official NuGet
7.1.3 package. File version: 7.1.3.1; assembly version: 7.1.0.0.

SHA-256: `a0b5be9580bf6548f685d79e5439f6d946ef57e013d201f946b2a894e7441804`.

- [Package](https://www.nuget.org/packages/Microsoft.Toolkit.Uwp.Notifications/7.1.3)
- [Upstream licence](https://github.com/CommunityToolkit/WindowsCommunityToolkit/blob/v7.1.3/License.md)
- [Included licence text](Sources/third-party-licenses/Microsoft.Toolkit.Uwp.Notifications-7.1.3-MIT.txt)

Preserve this attribution and the included licence when redistributing the DLL,
including in a future VIPM package or application installer.

## Documentation website

The build redistributes these unchanged browser assets under
`Sources/docs/vendor/`, together with their existing licence files:

| Component | Licence | Copyright / source |
|---|---|---|
| Docsify 4.13.1, search plugin and Vue-style CSS theme | MIT | 2016–present Docsify Contributors; [licence](Sources/docs/vendor/docsify-4.13.1/LICENSE) |
| Mermaid Tiny 12.2.0 | MIT | 2014–2022 Knut Sveidqvist; [licence](Sources/docs/vendor/mermaid-tiny-12.2.0/LICENSE) |

The Mermaid bundle's own retained notices identify these embedded components:

- **DOMPurify 3.4.12**, copyright Cure53 and other contributors. Upstream offers
  Apache-2.0 or MPL-2.0; this distribution uses the Apache-2.0 option and retains
  the original dual-licence header. [Included Apache licence](Sources/third-party-licenses/DOMPurify-3.4.12-LICENSE.txt).
- **Lodash modular build 4.18.1**, copyright OpenJS Foundation and other
  contributors, based on Underscore.js 1.8.3, copyright Jeremy Ashkenas,
  DocumentCloud and Investigative Reporters & Editors. MIT.
  [Included upstream licence](Sources/third-party-licenses/Lodash-4.18.1-LICENSE.txt).

Keep the bundled copyright/licence comments when copying or minifying assets.
These entries identify verified packages and retained bundle notices; a complete
transitive bundle inventory is a release-maintenance follow-up, not a warranty
of exhaustive legal clearance.

## Legacy library in repository history

**ToastNotifications 2.5.1**, by DevCrew.pl / Rafał Łopatka, is a separate WPF
library, not Microsoft.Toolkit.Uwp.Notifications. Its NuGet package points to
the GNU LGPL version 3. Historical copies have this SHA-256:

`ed1297117c8dba2b3880246721af5b74c6ae16d745bea176adbeefc1ee75f2fb`.

- [Package](https://www.nuget.org/packages/ToastNotifications/2.5.1)
- [Upstream source and licence](https://github.com/rafallopatka/ToastNotifications/tree/master-v2)
- [LGPL v3 text](Sources/third-party-licenses/ToastNotifications-2.5.1-LGPL-3.0.txt)
- [GPL v3 text incorporated by LGPL v3](Sources/third-party-licenses/GPL-3.0.txt)

This unused DLL is removed from the current source tree; the archived prototype
and Git history are retained. Earlier commits may still contain the binary.
Its licence is not replaced by ToastAPI's MIT licence. Anyone redistributing
those older copies must satisfy their LGPL/GPL obligations, including the
applicable corresponding-source requirements. A link to upstream or retention
of licence text alone is not asserted to fulfil all those obligations. Matching
the historical binary to corresponding buildable source remains a release
follow-up; do not include this legacy DLL in a new package.

## Format reference and development tools

**pylabview** — MIT, copyright (C) 2013 Jessica Creighton and (C) 2019–2020
Mefistotelis. The documentation reader credits its LabVIEW RSRC format work;
the module is not bundled with the site's Python scripts. The upstream licence
is retained as attribution for that reference and any incorporated adaptations:
[licence text](Sources/third-party-licenses/pylabview-MIT.txt),
[project](https://github.com/mefistotelis/pylabview).

Python, LabVIEW MCP and Codex are development/documentation tools, not runtime
dependencies shipped with ToastAPI. Merely using them does not assign their
licences to the toolkit's original code. Copied or embedded tool code would
require its own licence review.

- [Python licences](https://docs.python.org/3/license.html): the scripts use the
  standard library; no Python interpreter is included in this repository.
- [LabVIEW MCP](https://github.com/Zuehlke/labview-mcp/blob/main/LICENSE): MIT,
  copyright (c) 2026 Zühlke. Neither the server nor its skills are distributed here.
  The server's MIT licence does not cover NI's IDE or NI's services.
- [Codex/OpenAI terms for individuals in Europe](https://openai.com/policies/eu-terms-of-use/)
  and [business services agreement](https://openai.com/policies/services-agreement/):
  the applicable service contract depends on the account. Contractual allocation
  of output rights does not waive third-party rights or guarantee unique output.

## LabVIEW and platform prerequisites

LabVIEW, its Runtime and NI components remain subject to the applicable NI
agreement. Windows, .NET and WinRT components remain subject to their own terms.
Their installers/runtimes are not bundled here. Installing or using ToastAPI
does not grant a licence to those products. No external LabVIEW toolkit has
been identified in the saved-source inspection; package dependency resolution
must still be checked before a VIPM release.

NI's published distribution guidance requires an NI copyright notice in
distributed application documentation/About information and additional terms
when shipping NI runtime/driver software. Include the applicable version-year
notice when preparing such an application; this is separate from ownership of
ToastAPI's source. For the current LabVIEW 2026 development prerequisite:

Copyright © 2026 National Instruments Corporation. All rights reserved.

LabVIEW and NI are trademarks of National Instruments Corporation. Product names
identify interoperability; ToastAPI is an independent project and is not endorsed
or supported by NI, Microsoft, OpenAI or the other named tool providers.

- [NI software agreement](https://www.ni.com/en/about-ni/legal/software-license-agreement.html)
- [NI distribution requirements](https://www.ni.com/en/about-ni/legal/distribution-requirements-for-applications-developed-using-ni-so.html)

This notice does not modify or replace any upstream licence or service contract.
