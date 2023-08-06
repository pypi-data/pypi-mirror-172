

from generalpackager import Packager

from generalfile.test.test_path import PathTest

class TestPackager(PathTest):
    def test_badges_dict(self):
        self.assertLess(2, len(Packager().get_badges_dict()))

    def test_get_todos(self):
        Packager().get_todos()

    def test_get_todos_markdown(self):
        Packager().get_todos_markdown()

    def test_get_description_markdown(self):
        self.assertEqual(True, len(str(Packager().get_description_markdown())) > 3)

    def test_get_org_description_markdown(self):
        self.assertEqual(True, len(str(Packager().get_org_description_markdown())) > 3)

    def test_get_information_markdown(self):
        self.assertIn("generalpackager", Packager().get_information_markdown())

    def test_get_installation_markdown(self):
        self.assertIn("pip install", Packager().get_installation_markdown())

    def test_github_link(self):
        self.assertIn("generalpackager", Packager().github_link("foo", "bar"))

    def test_github_link_path_line(self):
        self.assertIn("generalpackager", Packager().github_link_path_line("foo", "bar"))

    def test_get_attributes_markdown(self):
        self.assertIn("generalpackager", Packager().get_attributes_markdown())

    def test_get_footnote_markdown(self):
        self.assertIn("generalpackager", Packager().get_footnote_markdown())


