# XML source delivery review — 4 November 2026

The maintainer implemented ToastFromXML, the XML native wrappers and the example,
then confirmed the example worked after fixing Invoke Object Method's target.
That helper now invokes Get Object Type.Object out, rather than the declaring
System.Type. The reflection helpers have also lost their redundant name prefix.

The documentation pass updates the six ToastFromXML member descriptions, five
native XML wrappers, Find Method By Signature and the XML example. It adds four
detailed application method pages with actual LabVIEW icon/terminal images,
the class overview and canonical example guide. Public indexes, source contracts
and coverage now distinguish XML strings from planned file/template features.
The repository README has a direct documentation badge.

## Review evidence

- Native gRPC exports cover 88 VIs, including the retained archive. Product VIs
  were not executed by the reviewer.
- 38 existing class VI connector contracts and summaries match earlier native
  exports. Current public call chains and error cases were inspected to assess
  documentation impact; this is not an exhaustive functional-equivalence proof.
- 28 native icon/terminal images were exported through Print.VI To HTML over
  ActiveX and visually inspected as a contact sheet. The XML constructor and Show
  diagrams were also inspected. Published images are the unchanged native images.
- Description updates use VI Server only, with saved STRG read-back and unchanged
  icon resources. Detailed-help URLs use the repository synchronization script.
- Application source code, connector names and manual layout are preserved. The
  constructor terminal currently reads `XML Stirng`; documentation uses its actual
  spelling rather than silently renaming a connector.

The strict documentation build and all 39 existing Python checks pass. The current
builder also generates the previous develop documentation successfully without
requiring the new XML guide. Headless Chrome loads the class page, constructor
page and XML guide with their Mermaid diagrams, no broken images or JavaScript
errors; the XML navigation entry is available in the mobile drawer.

The six ToastFromXML methods, Invoke Object Method, Load XML and all six examples
report eIdle. XML methods/example have empty execution-error lists. Four existing
class examples also report a data-type diagnostic despite eIdle and empty linker
errors; this contradictory diagnostic is retained as an unresolved observation,
not presented as a clean runtime validation. No example was run by the reviewer.

The creation polymorph's description still mentions only the builder. The server
refuses to edit that VI because LabVIEW returns an empty path. A manual update
has been requested from the maintainer; its existing detailed-help URL is retained.

## Remaining limits

The constructor creates a document before loading XML but has no guaranteed
release path if Load XML or the property write fails. This remains resource
hardening work under #16. The nominal example success does not establish memory
stability, concurrent shutdown safety, malformed XML cleanup or built-executable
compatibility. The example retains the existing final .NET collection workaround.

XML parsing is not full toast-schema validation. Disk loading, saving and template
substitution remain #29. Reply edge cases already observed in the builder example
have not been revalidated by the reviewer on the new XML path.
