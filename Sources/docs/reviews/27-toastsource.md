# ToastSource migration review

Date: 2026-11-02. Work branch: `codex/27-toastsource`, based on develop `c789f38`.

## Maintainer implementation

- ToastSource is a base class, explicitly retained by the maintainer instead of
  the interface originally proposed in #27. It has no native resource to own.
- ToastBuilder derives from it. Show, Get XML and Close are dynamic methods.
- The maintainer aligned `GetXML.vi` to `Get XML.vi` during this review so XML
  export has the same method name in the base class and concrete class.
- ToastService.Show accepts ToastSource and calls its Show method dynamically.
  There is no concrete-type switch or cast to ToastBuilder in that VI.
- Create was renamed Create ToastBuilder. Create ToastSource (Poly) currently
  has this one creation instance, confirmed from the saved polymorphic VI links
  and the four example call sites. The output remains a concrete ToastBuilder.
- Four examples use the creation polymorph and the adapted service input.

## Documentation edits

VI Server updated only VI descriptions on the three base methods, the four
affected builder methods, Service.Show and four examples. Each of these 12 saved
descriptions was read back offline from STRG, with unchanged icon resources.
No unrelated files were changed by that description batch. The polymorphic VI
was refused by the helper because its opened path was empty; its description
was entered and saved manually by the maintainer, then verified offline.

Class/library descriptions were updated through VI Server and verified from the
saved XML for ToastSource, ToastBuilder and ToastNotification. The repository
script synchronized class-method online help URLs with backups. The renamed
constructor has a new canonical route and an explicit old-route landing page.

The three new source method pages use the approved detailed-help model. The four
changed builder pages and Service.Show were reviewed and their native connector
illustrations recaptured with Print.VI To HTML over ActiveX. All eight PNGs were
visually inspected. No connector has been redrawn. Review records fingerprint
the inspected saved files, including dispatch dependencies for Service.Show.

## Checks and limits

- Native gRPC exports inspected: connectors, dynamic terminals, source method
  bodies, builder overrides, service dispatch and four example call chains.
- The eight inspected methods and four class examples report `eIdle`, executable,
  with empty execution error lists. The initially unavailable base Show error
  list was read successfully by a follow-up probe.
- Strict documentation generation checks all current class-method descriptions,
  saved detailed-help URLs, authored review fingerprints and local routes/assets.
- All 39 existing documentation CI regression checks pass (8 inventory, 16
  detailed help, 3 legal assets and 12 version-catalogue checks). No LabVIEW
  unit-test framework was introduced and no product VI was executed by the reviewer.

After description edits, the eight native AIXML exports match their pre-edit
snapshots when description attributes are excluded and the maintainer's Get XML
rename is accounted for. This checks that the review did not change their exported
wiring or connectors; it is not a full binary equivalence claim.

The base methods are currently no-ops, not failure-reporting abstract bodies:
base Show displays nothing; base Get XML yields an empty String; base Close only
propagates its error. Concrete source overrides must supply the work. Show/Get XML
skip on incoming error, while concrete cleanup must attempt release even on error.
Service.Show borrows the source and discards its returned class value; the caller
retains the original source for closure. No new concurrency or leak-free guarantee
is established by this migration. Existing #16/#22 limitations remain.

A second concrete implementation, ToastFromXML (#28), and disk templates (#29)
are not implemented in this commit. The second-implementation acceptance check
from #27 remains to be demonstrated with #28; existing examples do not prove XML
loading. No issue is closed by this checkpoint commit.
