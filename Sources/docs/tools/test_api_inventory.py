"""Regression checks for owner URL, scope and route discovery. No LabVIEW needed."""
from pathlib import Path
import json
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from api_inventory import inventory


class InventoryChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.owner = self.root / 'Sources/ToastBuilder/ToastBuilder.lvclass'
        self.write('Sources/ToastNotification/ToastNotification.lvlib',
                   '<Library><Item Name="ToastBuilder.lvclass" Type="LVClass" URL="../../ToastBuilder/ToastBuilder.lvclass"/></Library>')

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return path

    def test_item_url_is_used_instead_of_display_name(self):
        self.write('Sources/ToastBuilder/Actual.vi', '')
        self.owner.write_text('<LVClass><Item Name="Display.vi" Type="VI" URL="../Actual.vi"/></LVClass>')
        owner = inventory(self.root)[1]
        self.assertEqual(owner.id, 'toastbuilder')  # Existing detailed-help prefix.
        self.assertEqual([m.path.name for m in owner.members], ['Actual.vi'])

    def test_scope_inheritance_properties_and_private_data(self):
        for name in ['Public.vi', 'Hidden.vi', 'Read.vi', 'Data.ctl']:
            self.write('Sources/ToastBuilder/' + name, '')
        self.owner.write_text('''<LVClass>
          <Item Name="Data.ctl" Type="Class Private Data" URL="Data.ctl"/>
          <Item Name="Private" Type="Folder"><Property Name="NI.LibItem.Scope">2</Property>
            <Item Name="Hidden.vi" Type="VI" URL="../Hidden.vi"/></Item>
          <Item Name="Public.vi" Type="VI" URL="../Public.vi"><Property Name="NI.ClassItem.MethodScope">1</Property></Item>
          <Item Name="Value" Type="Property Definition"><Item Name="Read.vi" Type="VI" URL="../Read.vi"/></Item>
          </LVClass>''')
        members = inventory(self.root)[1].members
        self.assertEqual([m.path.name for m in members], ['Public.vi', 'Read.vi'])
        self.assertTrue(members[1].property)

    def test_private_owner_is_not_published(self):
        self.write('Sources/ToastNotification/ToastNotification.lvlib',
                   '<Library><Item Type="LVClass" URL="../../ToastBuilder/ToastBuilder.lvclass"><Property Name="NI.LibItem.Scope">2</Property></Item></Library>')
        self.write('Sources/ToastBuilder/ToastBuilder.lvclass', '<LVClass/>')
        self.assertEqual(len(inventory(self.root)), 1)

    def test_slug_collision_fails_instead_of_overwriting_a_page(self):
        for name in ['Add Text.vi', 'Add-Text.vi']:
            self.write('Sources/ToastBuilder/' + name, '')
        self.owner.write_text('<LVClass><Item Type="VI" URL="../Add Text.vi"/><Item Type="VI" URL="../Add-Text.vi"/></LVClass>')
        with self.assertRaisesRegex(ValueError, 'Duplicate documentation route'):
            inventory(self.root)

    def test_ambiguous_url_is_rejected(self):
        self.write('Sources/ToastBuilder/Actual.vi', '')
        self.write('Sources/Actual.vi', '')
        self.owner.write_text('<LVClass><Item Type="VI" URL="../Actual.vi"/></LVClass>')
        with self.assertRaisesRegex(ValueError, 'ambiguous'):
            inventory(self.root)

    def test_new_owner_requires_classification_when_map_exists(self):
        self.write('Sources/ToastBuilder/ToastBuilder.lvclass', '<LVClass/>')
        self.write('Sources/docs/api-map.json', json.dumps({'owners': {
            'Sources/ToastNotification/ToastNotification.lvlib': {'id': 'toastnotification'}}}))
        with self.assertRaisesRegex(ValueError, 'Classify the new documentation owner'):
            inventory(self.root)

    def test_route_ids_cannot_escape_the_output_directory(self):
        self.write('Sources/docs/api-map.json', json.dumps({'owners': {
            'Sources/ToastNotification/ToastNotification.lvlib': {'id': '../escape'}}}))
        with self.assertRaisesRegex(ValueError, 'Invalid documentation route ID'):
            inventory(self.root)


if __name__ == '__main__':
    unittest.main()
