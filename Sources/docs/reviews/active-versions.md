# Active documentation catalogue

The maintainer requested main/develop, active work and releases, excluding
previews of closed PRs even when the remote branches remain. The catalogue now
uses GitHub PR/release metadata instead of considering every existing ref active.

## Policy

- Keep main/develop when they contain documentation.
- Keep same-repository branches with an open PR, including draft PRs. Exclude
  fork PRs and branches without an open PR.
- Keep tags attached to published releases, including prereleases. Exclude draft
  releases and tags without a published release.
- Rebuild every manifest and the complete Pages artifact from that selection.
  Closing a PR removes its directory as well as its selector entry. Git branches
  and commit history are not deleted.
- Paginate the API, fail on API errors, and apply the triggering PR/release state
  so a briefly stale list response does not retain the just-closed preview.

The source extraction, current-builder-only execution and safe archive path
checks remain in place. Source refs are data; their scripts are not executed.
Stable help URLs still prefer main documentation, falling back to develop until
main contains the docs. This change does not add main documentation prematurely.

## Default-branch orchestration

GitHub now resolves pull_request_target from the repository's default branch,
which is main here. Main has no documentation workflow yet. The maintainer
explicitly approved installing only a small orchestration workflow there, without
shipping toolkit code or treating this as a release.

`documentation-catalogue.yml` must be identical in develop and main. It reacts
to PR opening/reopening/closure and release changes and explicitly checks out
trusted develop, never a PR head. Fork PRs do not enter its publish job. The
build uses contents/PR read permissions; only the separate Pages deployment job
has pages/id-token write permissions. No secrets are embedded in catalogue data.
Its concurrency group is shared with the push workflow's Pages publication.

Merge the develop catalogue implementation first, then the main-only workflow
installation. Until both are merged, the new main-triggered cleanup is not
installed. The regular push workflow already publishes the filtered catalogue.

References reviewed:
- https://github.blog/changelog/2025-11-07-actions-pull_request_target-and-environment-branch-protections-changes/
- https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target
- https://docs.github.com/en/rest/pulls/pulls#list-pull-requests
- https://docs.github.com/en/rest/releases/releases#list-releases

## Verification

Twelve catalogue regressions cover permanent refs, closed/merged and reopened
PRs, drafts, forks/deleted head repositories, missing refs, published/prerelease
versus draft/bare tags, stale event overrides, API pagination and API failure.

An offline integration fixture using real existing Git refs built develop and
a sample open work branch. Marking that PR closed produced only develop; the
closed branch's directory and entries were absent from the new artifact, without
deleting its Git ref. Evidence is under ignored `_review/version-policy`.
The existing 27 documentation regressions and strict local-link build also pass
(39 automated checks total). No LabVIEW files or website layout/runtime assets
are changed.
