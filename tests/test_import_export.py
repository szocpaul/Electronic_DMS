from datetime import date
import os
import shutil
import unittest

from documents import Document
from repository import Repository
from users import User

SAMPLE_DIR_PATH = '/tmp/samples'


class TestImportExport(unittest.TestCase):
    """Test the import and export functionality."""

    def test_import_without_users(self):
        repository = Repository('Empty', '/tmp/test_repo')
        with self.assertRaises(ValueError):
            repository.import_documents('{}/importable'.format(SAMPLE_DIR_PATH))
        shutil.rmtree('/tmp/test_repo')

    def test_import_with_users(self):
        if os.path.exists('/tmp/test_repo2'):
            shutil.rmtree('/tmp/test_repo2')
        repository = Repository('Empty', '/tmp/test_repo2')
        alice = User('Alice', 'Smith', date(1980, 10, 10), 'alice@mail.org', '****')
        bob = User('Bob', 'Marker', date(1970, 11, 11), 'bob@mail.org', '****')
        alice_id = repository._user_manager.add_user(alice)
        bob_id = repository._user_manager.add_user(bob)
        self.assertEqual(repository._user_manager.count_users(), 2)
        repository.import_documents('{}/importable'.format(SAMPLE_DIR_PATH))

        self.assertEqual(repository._document_manager.count_documents(), 2)
        
        results = repository._document_manager.find_documents_by_author(alice_id)
        self.assertEqual(len(results), 1)
        first_document = results[0]
        self.assertEqual(first_document.author, alice_id)
        self.assertEqual(first_document.title, 'Some important doc')
        self.assertEqual(first_document.description, 'Contains various documentations')
        self.assertEqual(first_document.files, ['part1.pdf', 'part2.pdf'])
        self.assertEqual(first_document.doc_format, 'pdf')

        results = repository._document_manager.find_documents_by_author(bob_id)
        self.assertEqual(len(results), 1)
        second_document = results[0]
        self.assertEqual(second_document.author, bob_id)
        self.assertEqual(second_document.title, 'Data report')
        self.assertEqual(second_document.description, 'Figures and graphs mainly')
        self.assertEqual(second_document.files, ['data.doc'])
        self.assertEqual(second_document.doc_format, 'doc')

        shutil.rmtree('/tmp/test_repo2')

    def test_export_documents(self):
        try:
            shutil.rmtree('/tmp/test_repo3')
            shutil.rmtree('/tmp/exported_documents')
        except OSError as error:
            pass
        repository = Repository('Empty', '/tmp/test_repo3')
        alice = User('Alice', 'Smith', date(1980, 10, 10), 'alice@mail.org', '****')
        bob = User('Bob', 'Marker', date(1970, 11, 11), 'bob@mail.org', '****')
        alice_id = repository._user_manager.add_user(alice)
        bob_id = repository._user_manager.add_user(bob)
        first_document = Document(
            'Some important doc',
            'Contains various documentations',
            alice_id,
            [SAMPLE_DIR_PATH + '/importable/part1.pdf', SAMPLE_DIR_PATH + '/importable/part2.pdf'],
            'pdf'
        )
        first_document.make_public()
        first_document.change_state('pending')
        first_document.change_state('accepted')
        second_document = Document(
            'Data report',
            'Figures and graphs mainly',
            bob_id,
            [SAMPLE_DIR_PATH + '/importable/data.doc'],
            'doc'
        )
        second_document.make_public()
        second_document.change_state('pending')
        second_document.change_state('accepted')
        first_id = repository._document_manager.add_document(first_document)
        second_id = repository._document_manager.add_document(second_document)
        repository.export_documents([first_id, second_id], '/tmp/exported_documents')

        self.assertTrue(os.path.exists('/tmp/exported_documents/part1.pdf'))
        self.assertTrue(os.path.exists('/tmp/exported_documents/part2.pdf'))
        self.assertTrue(os.path.exists('/tmp/exported_documents/data.doc'))
        self.assertTrue(os.path.exists('/tmp/exported_documents/1.edd'))
        self.assertTrue(os.path.exists('/tmp/exported_documents/2.edd'))

        with open('/tmp/exported_documents/1.edd') as edd_file:
            lines = edd_file.readlines()
            self.assertIn('[document]\n', lines)
            self.assertIn('title=Some important doc\n', lines)
            self.assertIn('description=Contains various documentations\n', lines)
            self.assertIn('author=Alice Smith\n', lines)
            self.assertIn('files=part1.pdf part2.pdf\n', lines)
            self.assertIn('type=pdf\n', lines)

        with open('/tmp/exported_documents/2.edd') as edd_file:
            lines = edd_file.readlines()
            self.assertIn('[document]\n', lines)
            self.assertIn('title=Data report\n', lines)
            self.assertIn('description=Figures and graphs mainly\n', lines)
            self.assertIn('author=Bob Marker\n', lines)
            self.assertIn('files=data.doc\n', lines)
            self.assertIn('type=doc\n', lines)

        shutil.rmtree('/tmp/exported_documents')
        shutil.rmtree('/tmp/test_repo3')
