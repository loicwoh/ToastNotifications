# Canonical content and routes

This map is the maintenance contract for issue #36. It identifies where to edit
information, rather than keeping another copy of each explanation.

## Sources of truth

| Information | Canonical source | Build / consumer |
|---|---|---|
| Physical ownership, item URL and technical scope | Saved root .lvlib and referenced .lvlib/.lvclass XML | api_inventory.py discovers owners and public members |
| Documented layer, owner ID, related workflows, native-accessor annotations | api-map.json | Human-reviewed classification; does not change access scope |
| Role, boundary and dependencies of each owner | site/api/*.md | API-MEMBERS marker is replaced only in the staged copy |
| Saved VI/data-type summary | STRG in the saved .vi/.ctl | Read-only vi_descriptions.py; no graph/terminal extraction |
| Current public callback and ownership contract | site/callbacks.md | Links from owner pages, concept map and guides |
| Concept entry points | site/concepts.md | Existing terms and destinations; expanded tutorials in #40 |
| Example parameters, instructions and observations | Sources/Examples/Reply Input.md, Multiple Actions.md, Protocol Activation.md | Copied once; build adds navigation to the staged guides |
| Feature maturity and compatibility statements | site/coverage.md | #15 and #17 supply validation evidence and environment details |
| Upstream Microsoft links and API families | site/microsoft.md | Shared destination for deeper reference |
| Site build/publication procedure | README.md in this directory | Maintainer instructions |
| Future detailed VI explanations | To be defined by #37 | #36 does not introduce a second hand-maintained VI-summary snapshot |

## Existing repository documents

- The repository README and Sources/README.md are entry points, not parallel tutorials.
- Sources/ARCHITECTURE.md is a maintainer architecture note and link to the current
  owner/contract pages. Its implementation details are not independently copied
  into user documentation.
- Sources/CALLBACK-LIFETIME.md preserves helper-level implementation notes and
  historical validation observations. The current user contract is callbacks.md.
  Historical counts or probes do not describe a fresh regression run.
- Sources/HANDOFF.md is a handover log. It is not published as an API contract.
- Sources/Examples/README.md remains the local example-file index; site/examples.md
  is the website scenario selector. Scenario configuration and results belong in
  the three guides, not in either index.
- Sources/Archive preserves the original prototype and is not part of the
  generated API or package documentation.

The remaining French maintainer notes and any intentional archive exceptions are
tracked by #12. Do not translate an obsolete duplicate instead of updating its
canonical destination.

## Routes and linking rules

- Keep /api and /reference as entry points. Existing /api?id=toastbuilder,
  toastservice, activationhandler, activation-data and xml-support anchors remain.
- Owner pages use /api/{owner-id}. Methods and data types use
  /reference/{owner-id}/{member-slug}. Existing class owner IDs and all 23 saved
  VI help URLs are retained. The 23-entry api-links.json remains the input to
  Sync-DetailedHelp.ps1; new low-level/type pages do not require saving VIs.
- api-map.json fixes IDs independently of display labels. Inventory validates
  collisions and missing/ambiguous source URLs. A new owner must be classified.
- Breadcrumbs go API → root library → owner → member. Each member links back
  to its owner and to related owner workflows. Guides link to their owners.
- Owner pages link to existing concept sections and guides. Do not create links
  to empty pages for future tutorials; add the new destination when #40/#24 lands.
- On a rename in #12, preserve the old route or supply an explicit alias and
  check the saved help URL before changing callers. Release-specific URL policy
  and immutable publication remain #18/#14; no new policy is implied here.

## Inventory and scope

The root is ToastNotification.lvlib, not a hard-coded list of four classes.
Traverse library/class membership, resolve actual item URLs and retain Public
members. Explicit method/item scope takes precedence over inherited folder scope.
Private, Protected and Community members are excluded from the public lists.
Class private-data controls are excluded. Public .ctl files have their own entries.

Application, Extension and Low-level are documentation categories describing the
existing examples. Public native-reference accessors stay listed in a separate
section; they do not become a recommended application API through documentation.
The stable support boundary remains undecided in #18.

## Generated output and historical versions

All generated references, api-inventory.json, api-links.json, staged guide
navigation and assembled owner pages stay under the ignored output directory.
Edit the sources above; never hand-edit the staged pages.

The current builder must still read published refs that predate api-map.json.
For those refs it discovers owners from their root library, preserves class
reference IDs and supplies minimal generated owner pages with an Unclassified
layer. It does not require new authored pages or execute old branch scripts.
This compatibility path does not make old release documentation immutable.
