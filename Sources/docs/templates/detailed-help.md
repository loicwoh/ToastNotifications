<!-- Maintainer template: copy to reference/<owner-id>/<member-slug>.md,
     add the matching .json record and reviewed SVG as described in ../README.md.
     Replace every placeholder; do not publish this template itself.
     No H1 or saved-summary copy: those come from the generator. -->

## Purpose and when to call

Explain the developer's goal, the place in the workflow and nearby alternatives.

## Connector and terminals

Add an accessible SVG connector schematic or controlled equivalent. Record its
source, revision and review method in the JSON record. Identify pattern, slots,
unused positions and Required/Recommended/Optional settings from the saved VI.

### Inputs

| Terminal (slot) | LabVIEW type | Saved default | Meaning and precondition |
|---|---|---|---|
| Replace | Replace | Distinguish saved default from a valid runtime value | Replace |

### Outputs

| Terminal (slot) | LabVIEW type | Meaning |
|---|---|---|
| Replace | Replace | State ownership, aliases and returned-error meaning |

## Behavior and errors

Describe the actual error/no-error branches, validation, side effects, failure
propagation and any lack of rollback. Link upstream constraints with API version.
Do not invent custom codes or infer behavior from names alone.

## Minimal calling scenario

Show before/call/after, class and error wiring, expected result, prerequisites,
handler setup if relevant, and a link to an existing executable example.
Label a schematic sequence as such.

### Ownership and cleanup

State who creates/closes each reference, whether outputs alias inputs, lifetime
through asynchronous callbacks and the cleanup path on success and failure.
Link the canonical ownership contract rather than duplicate its internals.

## Pitfalls and variants

Explain likely misuse and how to select the related operation.

## Maturity and validation

Separate inspection, observed execution, supported environments and untested
cases. Link evidence; an export or successful docs build is not a runtime test.

## Related reading

Link the owner, concepts, neighboring VIs, example guide and Microsoft reference.

<!-- The builder adds provenance (date, review method, reviewed SHA-256 values)
     from JSON. Do not keep another copy here. -->
