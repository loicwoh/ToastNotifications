"""Catalogue policy regressions without network calls or LabVIEW execution."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_versions import select_refs, api_pages, event_state

REPO = 'loicwoh/ToastNotifications'


def pull(number=1, state='open', branch='codex/work', repository=REPO):
    return dict(number=number, state=state, head=dict(ref=branch, repo=dict(full_name=repository)))


class CatalogueChecks(unittest.TestCase):
    def test_permanent_branches_survive_without_pull_requests(self):
        refs = ['refs/remotes/origin/main', 'refs/remotes/origin/develop',
                'refs/remotes/origin/HEAD', 'refs/remotes/origin/abandoned']
        self.assertEqual(select_refs(refs, REPO, [], []), refs[:2])

    def test_closed_and_merged_pr_branches_disappear_even_if_ref_remains(self):
        refs = ['refs/remotes/origin/codex/work']
        closed = pull(state='closed')
        closed['merged_at'] = '2026-11-02T12:00:00Z'
        self.assertEqual(select_refs(refs, REPO, [closed], []), [])
        closed['merged_at'] = None
        self.assertEqual(select_refs(refs, REPO, [closed], []), [])

    def test_open_and_draft_pr_branches_are_available(self):
        refs = ['refs/remotes/origin/codex/work']
        opened = pull()
        opened['draft'] = True
        self.assertEqual(select_refs(refs, REPO, [opened], []), refs)

    def test_fork_pr_does_not_publish_matching_local_branch(self):
        refs = ['refs/remotes/origin/codex/work']
        self.assertEqual(select_refs(refs, REPO, [pull(repository='someone/fork')], []), [])

    def test_deleted_head_repository_is_ignored(self):
        opened = pull()
        opened['head']['repo'] = None
        self.assertEqual(select_refs(['refs/remotes/origin/codex/work'], REPO, [opened], []), [])

    def test_missing_remote_branch_does_not_create_a_version(self):
        self.assertEqual(select_refs([], REPO, [pull()], []), [])

    def test_only_published_releases_include_tags(self):
        refs = ['refs/tags/v1', 'refs/tags/v2-beta', 'refs/tags/draft', 'refs/tags/bare']
        releases = [dict(tag_name='v1', draft=False, published_at='today'),
                    dict(tag_name='v2-beta', draft=False, prerelease=True, published_at='today'),
                    dict(tag_name='draft', draft=True, published_at=None)]
        self.assertEqual(select_refs(refs, REPO, [], releases), refs[:2])

    def test_close_event_overrides_temporarily_stale_open_list(self):
        state = dict(pulls=[pull()], releases=[])
        result = event_state(state, dict(pull_request=pull(state='closed')))
        self.assertEqual(result['pulls'], [])
        self.assertEqual(len(state['pulls']), 1)

    def test_reopen_event_restores_branch_and_other_open_pr_can_keep_it(self):
        state = event_state(dict(pulls=[], releases=[]), dict(pull_request=pull()))
        refs = ['refs/remotes/origin/codex/work']
        self.assertEqual(select_refs(refs, REPO, state['pulls'], []), refs)
        state['pulls'].append(pull(number=2))
        state = event_state(state, dict(pull_request=pull(state='closed')))
        self.assertEqual(select_refs(refs, REPO, state['pulls'], []), refs)

    def test_api_pagination_keeps_more_than_one_hundred_items(self):
        seen = []
        def fetch(path):
            seen.append(path)
            return list(range(100)) if path.endswith('page=1') else [100]
        self.assertEqual(len(api_pages(REPO, 'pulls?state=open', fetch)), 101)
        self.assertIn('&per_page=100&page=2', seen[-1])

    def test_release_removal_event_overrides_stale_api_result(self):
        release = dict(id=7, tag_name='v1', draft=False, published_at='today')
        for action in ['deleted', 'unpublished']:
            state = event_state(dict(pulls=[], releases=[release]),
                                dict(action=action, release=release))
            self.assertEqual(state['releases'], [])

    def test_api_failure_is_not_silently_treated_as_an_empty_catalogue(self):
        def fetch(path):
            return {'message': 'API unavailable'}
        with self.assertRaisesRegex(ValueError, 'did not return a list'):
            api_pages(REPO, 'releases', fetch)


if __name__ == '__main__':
    unittest.main()
