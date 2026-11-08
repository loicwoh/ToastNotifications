# Canonical content and routes

This map is the maintenance contract for issue #36. It identifies where to edit
information, rather than keeping another copy of each explanation.

## Sources of truth

| Information | Canonical source | Build / consumer |
|---|---|---|
| Project motivation, history and author's experience with AI assistance | site/background.md | Personal account based on the author's notes; home and repository pages link here |
| Physical ownership, item URL and technical scope | Saved root .lvlib and referenced .lvlib/.lvclass XML | api_inventory.py discovers owners and public members |
| Documented layer, owner ID, related workflows, native-accessor annotations | api-map.json | Human-reviewed classification; does not change access scope |
| Role, boundary and dependencies of each owner | site/api/*.md | API-MEMBERS marker is replaced only in the staged copy |
| Saved VI/data-type summary | STRG in the saved .vi/.ctl | Read-only vi_descriptions.py; no graph/terminal extraction |
| Current public callback and ownership contract | site/callbacks.md | Links from owner pages, concept map and guides |
| Concept entry points | site/concepts.md | Existing terms and destinations; expanded tutorials in #40 |
| Example parameters, instructions and observations | Sources/docs/example-guides/Reply Input.md, Multiple Actions.md, Protocol Activation.md | Copied once; build adds navigation to the staged guides |
| Feature maturity and compatibility statements | site/coverage.md | #15 and #17 supply validation evidence and environment details |
| Upstream Microsoft links and API families | site/microsoft.md | Shared destination for deeper reference |
| Site build/publication procedure | README.md in this directory | Maintainer instructions |
| Detailed VI explanations, Mermaid call sequence, native help image and terminal tables | reference/<owner-id>/<member-slug>.md and .png | Appended to generated summary in staging; no redrawn connector |
| Compact incoming-error behavior | Adjacent reference/*.json: error_behavior=skip/always/noop | Bold cue in detailed help; noop identifies an empty base hook; use the same wording in authorized context-help edits |
| Detailed-help review provenance and saved-file fingerprints | Adjacent reference/*.json | Build checks freshness; technical review evidence is not published in the help page |
| Detailed-help authoring structure | templates/detailed-help.md | Maintainer scaffold; never published as an API entry |
| Toolkit/class visual conventions | VISUAL-IDENTITY.md and site/assets/identity.css | Repository-only maintainer reference for the shared palette and future LabVIEW banners; not published as a website page |
| Owner to visual family | api-map.json: visual_family | Generated owner banners; plugin uses its base handler family |
| Application API documentation boundary | api-map.json: audience and internal_members | Excludes support libraries and raw-reference members independently of saved access rights |
| Internal library implementation notes | maintenance/*.md | Repository-only; never copied into the website |

## Existing repository documents

- The repository README and Sources/README.md are entry points, not parallel tutorials.
- Sources/docs/example-guides/README.md remains the local example-file index; site/examples.md
  is the website scenario selector. Scenario configuration and results belong in
  the scenario guides, not in either index. Toast From XML.md is the canonical
  XML-string guide, published at guides/xml.md.
- Sources/Archive preserves the original prototype and is not part of the
  generated API or package documentation.

The remaining French maintainer notes and any intentional archive exceptions are
tracked by #12. Do not translate an obsolete duplicate instead of updating its
canonical destination.

## Routes and linking rules

- Keep /api and /reference as entry points. Existing /api?id=toastbuilder,
  toastservice, activationhandler, activation-data and xml-support anchors remain.
- Owner pages use /api/{owner-id}. Methods and data types use
  /reference/{owner-id}/{member-slug}. Existing class owner IDs and saved
  VI help URLs (with a compatibility page for the renamed Create method) are retained.
  The generated api-links.json remains the input to
  Sync-DetailedHelp.ps1. Payload-type pages do not require saving VIs; internal
  support libraries are excluded from the current website.
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

The root is ToastNotification.lvlib, not a hard-coded list of classes.
Traverse library/class membership, resolve actual item URLs and retain Public
members. Explicit method/item scope takes precedence over inherited folder scope.
Private, Protected and Community members are excluded from the public lists.
Class private-data controls are excluded. Application payload .ctl files have their
own entries; internal storage types are excluded by internal_members.

Application and Extension define the user-facing classes. Support owners marked
audience=internal and members listed in internal_members are not promoted in
public lists, owner children, search routes or the published inventory. This does
not modify LabVIEW scopes. Existing saved Help URLs for the two raw-reference
accessors retain small compatibility pages pointing to their class; their full
descriptions are not published. The help-link maintenance map follows the current class inventory.
The low-level owner notes remain in maintenance/, outside site/. A mapped internal
owner can later become Community/Private without breaking documentation inventory
validation, provided its recorded source still exists.
The stable support boundary remains undecided in #18.

## Generated output and historical versions

All generated references, api-inventory.json, api-links.json, staged guide
navigation and assembled owner pages stay under the ignored output directory.
Breadcrumbs are rendered from navigation.js outside the Markdown source so the
search plugin does not index them as duplicate sections. Search caches identify
the generated revision.
Edit the sources above; never hand-edit the staged pages.

The current builder must still read published refs that predate api-map.json.
For those refs it discovers owners from their root library, preserves class
reference IDs and supplies minimal generated owner pages with an Unclassified
layer. It does not require new authored pages or execute old branch scripts.
This compatibility path does not make old release documentation immutable.
Audience exclusions come from each source version's map; historical versions
without the flags retain their earlier inventory and references.
