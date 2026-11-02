"""Documentation pipeline regressions; no LabVIEW execution or VI writes."""
from pathlib import Path
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from detailed_help import load_help
from reference_docs import generate_reference
import reference_docs


class DetailedHelpChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.addCleanup(setattr, reference_docs, 'description', reference_docs.description)
        self.site = self.root / 'output'
        self.site.mkdir()
        self.source = 'Sources/ToastBuilder/Add Text.vi'
        self.route = 'reference/toastbuilder/add-text'
        self.write('Sources/ToastNotification/ToastNotification.lvlib',
                   '<Library><Item Type="LVClass" URL="../../ToastBuilder/ToastBuilder.lvclass"/></Library>')
        self.write('Sources/ToastBuilder/ToastBuilder.lvclass',
                   '<LVClass><Item Type="VI" URL="../Add Text.vi"/></LVClass>')
        self.write(self.source, 'saved file fixture; not a real VI')
        self.markdown = self.write('Sources/docs/' + self.route + '.md',
                                   '## Purpose\n\nAuthored explanation.\n\n![Connector](add-text.svg)\n')
        self.visual = self.write('Sources/docs/' + self.route + '.svg', '<svg xmlns="http://www.w3.org/2000/svg"/>')
        self.record_path = self.root / ('Sources/docs/' + self.route + '.json')
        self.record = dict(schema_version=1, source=self.source, reviewed_on='2026-11-02',
                           method='Fixture review, no runtime validation.',
                           error_behavior='skip',
                           reviewed_files={self.source: hashlib.sha256((self.root / self.source).read_bytes()).hexdigest()},
                           visual='toastbuilder/add-text.svg')
        self.save_record()

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        return path

    def save_record(self):
        self.record_path.write_text(json.dumps(self.record), encoding='utf-8')

    def load(self):
        return load_help(self.root, self.site, {self.route: self.source})

    def test_two_generations_preserve_authored_sources_and_refresh_saved_summary(self):
        authored = {p: p.read_bytes() for p in [self.markdown, self.record_path, self.visual]}
        for summary in ['First saved summary', 'Updated saved summary']:
            # docs_preview.build starts from a clean staging tree each time.
            shutil.rmtree(self.site)
            self.site.mkdir()
            # Stub only the binary-description reader: this fixture never edits a real VI.
            reference_docs.description = lambda path: summary
            generate_reference(self.root, self.site, False)
            page = (self.site / (self.route + '.md')).read_text(encoding='utf-8')
            self.assertIn('## Short description\n\n*From LabVIEW Context Help.*\n\n' + summary, page)
            self.assertEqual(page.count('Authored explanation.'), 1)
            self.assertNotIn('## Review provenance', page)
            self.assertNotIn('Fixture review', page)
            self.assertIn('Error behavior: Skipped on incoming error.', page)
            self.assertNotIn('Detailed help pilot', page)
            self.assertEqual((self.site / (self.route + '.svg')).read_bytes(), self.visual.read_bytes())
            for path, original in authored.items():
                self.assertEqual(path.read_bytes(), original)
        self.assertNotIn('First saved summary', page)

    def test_changed_reviewed_file_requires_review(self):
        self.write(self.source, 'changed fixture')
        with self.assertRaisesRegex(ValueError, 'Stale detailed help'):
            self.load()

    def test_orphaned_or_wrong_member_is_rejected(self):
        self.record['source'] = 'Sources/ToastBuilder/Wrong.vi'
        self.save_record()
        with self.assertRaisesRegex(ValueError, 'Orphaned or mismatched'):
            self.load()

    def test_missing_record_is_rejected(self):
        self.record_path.unlink()
        with self.assertRaisesRegex(ValueError, 'matching .md and .json'):
            self.load()

    def test_missing_or_escaping_visual_is_rejected(self):
        for visual in ['toastbuilder/missing.svg', '../../../outside.svg']:
            self.record['visual'] = visual
            self.save_record()
            with self.assertRaisesRegex(ValueError, 'Missing or invalid.*visual'):
                self.load()

    def test_visual_must_be_used_by_the_page(self):
        self.markdown.write_text('## No visual\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'link its reviewed visual'):
            self.load()

    def test_cleanup_error_behavior_is_prominent_and_explicit(self):
        self.record['error_behavior'] = 'always'
        self.save_record()
        page = self.load()[self.route]
        self.assertTrue(page.startswith('**Error behavior: Executes even on incoming error.**'))
        self.assertNotIn('Fixture review', page)

    def test_unknown_error_behavior_is_rejected(self):
        self.record['error_behavior'] = 'guessed'
        self.save_record()
        with self.assertRaisesRegex(ValueError, 'Choose skip or always'):
            self.load()

    def test_changed_captured_visual_is_rejected(self):
        self.record['visual_sha256'] = hashlib.sha256(self.visual.read_bytes()).hexdigest()
        self.save_record()
        self.visual.write_text('<svg>changed capture</svg>', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Changed detailed help visual'):
            self.load()

    def test_historical_ref_without_authored_directory_still_generates_summaries(self):
        shutil.rmtree(self.root / 'Sources/docs/reference')
        reference_docs.description = lambda path: 'Historical saved summary'
        routes = generate_reference(self.root, self.site, False)
        self.assertIn('/' + self.route, routes)
        page = (self.site / (self.route + '.md')).read_text(encoding='utf-8')
        self.assertIn('Short description only', page)
        self.assertNotIn('Detailed help pilot', page)
        self.assertIn('Historical saved summary', page)


if __name__ == '__main__':
    unittest.main()
