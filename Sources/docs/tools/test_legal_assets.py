"""Licence assets must accompany their version without relicensing old refs."""
from pathlib import Path
import tempfile
import unittest
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from docs_preview import stage_legal


class LegalPublicationChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.site = self.root / 'output'
        self.site.mkdir()

    def fixtures(self):
        (self.root / 'LICENSE').write_bytes(b'This version MIT\r\n')
        (self.root / 'THIRD-PARTY-NOTICES.md').write_bytes(b'Third-party notices\n')
        directory = self.root / 'Sources/third-party-licenses'
        directory.mkdir(parents=True)
        (directory / 'example.txt').write_bytes(b'Upstream licence text\r\n')

    def test_published_texts_are_byte_exact_copies_of_this_version(self):
        self.fixtures()
        (self.site / 'licenses.md').write_text('# Licenses')
        stage_legal(self.root, self.site)
        for source, target in [('LICENSE', 'toastapi-license.txt'),
                               ('THIRD-PARTY-NOTICES.md', 'third-party-notices.txt'),
                               ('Sources/third-party-licenses/example.txt', 'third-party/example.txt')]:
            self.assertEqual((self.root / source).read_bytes(),
                             (self.site / 'legal' / target).read_bytes())

    def test_historical_site_without_licence_page_gets_no_new_licence(self):
        self.fixtures()
        stage_legal(self.root, self.site)
        self.assertFalse((self.site / 'legal').exists())

    def test_new_page_cannot_publish_without_required_versioned_notices(self):
        self.fixtures()
        (self.site / 'licenses.md').write_text('# Licenses')
        for name in ['LICENSE', 'THIRD-PARTY-NOTICES.md']:
            path = self.root / name
            original = path.read_bytes()
            path.unlink()
            with self.assertRaisesRegex(ValueError, 'requires the versioned'):
                stage_legal(self.root, self.site)
            path.write_bytes(original)


if __name__ == '__main__':
    unittest.main()
