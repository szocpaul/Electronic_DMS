import unittest

from projects import Project


class TestProject(unittest.TestCase):
    """Test the project class"""

    def test_creation(self):
        project = Project('project_1', 'The first project')

    def test_creation_with_members(self):
        members = [1, 2, 3]
        project = Project('project_1', 'The first project', members=members)

    def test_creation_with_documents(self):
        documents = [1, 2, 3]
        project = Project('project_1', 'The first project', documents=documents)

    def test_properties(self):
        members = [1, 2, 3]
        documents = [4, 5, 6]
        project = Project('project_1', 'The first project', members=members, documents=documents)
        self.assertEqual(project.name, 'project_1')
        self.assertEqual(project.description, 'The first project')
        self.assertEqual(project.members, [1, 2, 3])
        self.assertEqual(project.documents, [4, 5, 6])
