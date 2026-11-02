# Licenses & third-party notices

## ToastAPI: MIT

Copyright © 2026 loicwoh. ToastAPI's original source code and authored
documentation are available under the **MIT License**. Commercial use,
modification and redistribution, including in proprietary applications, are
permitted provided the copyright and licence notice are retained.

The software is provided **as is, without warranty**. The MIT licence includes
an exclusion of authors' and copyright holders' liability. It does not promise
support, maintenance or updates. The enforceability of exclusions remains
subject to applicable law.

[Read the full MIT License](legal/toastapi-license.txt ':ignore') ·
[Read all third-party notices](legal/third-party-notices.txt ':ignore')

## Components distributed with the project

Third-party software retains its own terms; ToastAPI's MIT licence does not
replace them. Keep these notices when redistributing the relevant components.

| Component | Used for | Licence |
|---|---|---|
| Microsoft.Toolkit.Uwp.Notifications 7.1.3 | Notification builder and activation integration | [MIT](legal/third-party/Microsoft.Toolkit.Uwp.Notifications-7.1.3-MIT.txt ':ignore') |
| Docsify 4.13.1 | Documentation site, search and theme | [MIT](legal/third-party/Docsify-4.13.1-MIT.txt ':ignore') |
| Mermaid Tiny 12.2.0 | Documentation diagrams | [MIT](legal/third-party/Mermaid-Tiny-12.2.0-MIT.txt ':ignore') |
| DOMPurify 3.4.12, embedded in Mermaid | Sanitize rendered diagram content | [Apache-2.0 option](legal/third-party/DOMPurify-3.4.12-LICENSE.txt ':ignore') |
| Lodash / Underscore notices retained in Mermaid | Browser utility code | [MIT](legal/third-party/Lodash-4.18.1-LICENSE.txt ':ignore') |

The notification DLL is the net461 binary from the official NuGet package.
Its file version is 7.1.3.1 and its assembly version is 7.1.0.0; these are not
different package versions. The same DLL is retained for the archived prototype.

An unrelated `ToastNotifications.dll` 2.5.1 used during earlier exploration has
been removed from the current tree. Historical copies retain their LGPL v3
terms and corresponding-source obligations; see the full third-party notices
before redistributing older commits. It is not a dependency to include in a
new ToastAPI application or package.

## Tools and prerequisites

Python builds the documentation; LabVIEW MCP and Codex assist development.
They are not shipped runtime dependencies and are not required by applications
using ToastAPI. Their licences/service terms remain separate. The Python
description reader also credits the MIT-licensed pylabview format reference.

LabVIEW is proprietary NI software and requires an appropriate NI licence.
Windows, .NET and WinRT are separate platform prerequisites. ToastAPI's MIT
licence grants no rights to their IDEs, runtimes or installers. Runtime/driver
redistribution must follow the relevant vendor agreement.

Copyright © 2026 National Instruments Corporation. All rights reserved.
LabVIEW and NI are trademarks of National Instruments Corporation. Names are
used to identify interoperability; this independent project is not endorsed
or supported by NI, Microsoft, OpenAI or the other named providers.

[NI distribution requirements](https://www.ni.com/en/about-ni/legal/distribution-requirements-for-applications-developed-using-ni-so.html) ·
[Python licences](https://docs.python.org/3/license.html) ·
[LabVIEW MCP licence](https://github.com/Zuehlke/labview-mcp/blob/main/LICENSE) ·
[OpenAI terms](https://openai.com/policies/eu-terms-of-use/)
