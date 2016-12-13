import unittest

from documents import Document


class TestDocument(unittest.TestCase):
    """Test the document class"""

    def test_creation(self):
        document = Document('title1', 'desc1', 'author1', ['1.pdf', '2.pdf'], 'pdf')

    def test_properties(self):
        document = Document('title1', 'desc1', 'author1', ['1.pdf', '2.pdf'], 'pdf')
        self.assertEqual(document.title, 'title1')
        self.assertEqual(document.description, 'desc1')
        self.assertEqual(document.author, 'author1')
        self.assertEqual(document.files, ['1.pdf', '2.pdf'])
        self.assertEqual(document.doc_format, 'pdf')

    def test_visibility(self):
        document = Document('title1', 'desc1', 'author1', ['1.pdf', '2.pdf'], 'pdf')
        self.assertFalse(document.is_public())
        document.make_public()
        self.assertTrue(document.is_public())
        document.make_private()
        self.assertFalse(document.is_public())
