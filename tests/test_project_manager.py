import os
import shutil
import unittest

from projects import Project
from projects import ProjectManager
from users import UserManager
from users import RoleManager


class TestProjectManager(unittest.TestCase):
    """Test the project manager class"""

    def setUp(self):
        os.makedirs('/tmp/edms/projects')
        self._user_manager = UserManager('/tmp/edms/users')
        self._project_manager = ProjectManager('/tmp/edms/projects', self._user_manager)

    def tearDown(self):
        shutil.rmtree('/tmp/edms')

    def test_empty_project_storage(self):
        project_count = self._project_manager.count_projects()
        self.assertEqual(project_count, 0)

    def test_add_project(self):
        project = Project('My Project', 'A very difficult project')
        self._project_manager.add_project(project)
        self.assertEqual(self._project_manager.count_projects(), 1)

    def test_multiple_project_addition(self):
        for i in range(100):
            project = Project('Project {}'.format(i), 'Common project')
            self._project_manager.add_project(project)
        self.assertEqual(self._project_manager.count_projects(), 100)

    def test_find_project_by_id(self):
        a = Project('Project A', 'Work on A')
        b = Project('Project B', 'Work on B')
        a_id = self._project_manager.add_project(a)
        b_id = self._project_manager.add_project(b)
        project = self._project_manager.find_project_by_id(a_id)
        self.assertEqual(project.name, 'Project A')
        self.assertEqual(project.description, 'Work on A')
        project = self._project_manager.find_project_by_id(b_id)
        self.assertEqual(project.name, 'Project B')
        self.assertEqual(project.description, 'Work on B')

    def test_invalid_id_in_empty(self):
        with self.assertRaises(ValueError):
            self._project_manager.find_project_by_id(4321)

    def test_invalid_id(self):
        a = Project('Project A', 'Work on A')
        a_id = self._project_manager.add_project(a)
        with self.assertRaises(ValueError):
            self._project_manager.find_project_by_id(a_id + 1)

    def test_project_update(self):
        a = Project('Project A', 'Work on A')
        project_id = self._project_manager.add_project(a)
        b = Project('Project B', 'Work on B')
        self._project_manager.update_project(project_id, b)
        updated_project = self._project_manager.find_project_by_id(project_id)
        self.assertEqual(updated_project.name, b.name)
        self.assertEqual(updated_project.description, b.description)

    def test_project_update_with_invalid_id(self):
        with self.assertRaises(ValueError):
            a = Project('Project A', 'Work on A')
            project_id = self._project_manager.add_project(a)
            b = Project('Project B', 'Work on B')
            self._project_manager.update_project(project_id + 1, b)

    def test_project_remove(self):
        a = Project('Project A', 'Work on A')
        a_id = self._project_manager.add_project(a)
        b = Project('Project B', 'Work on B')
        b_id = self._project_manager.add_project(b)
        self.assertEqual(self._project_manager.count_projects(), 2)
        self._project_manager.remove_project(a_id)
        project = self._project_manager.find_project_by_id(b_id)
        self.assertEqual(project.name, 'Project B')
        self.assertEqual(self._project_manager.count_projects(), 1)

    def test_project_remove_with_invalid_id(self):
        a = Project('Project A', 'Work on A')
        a_id = self._project_manager.add_project(a)
        with self.assertRaises(ValueError):
            self._project_manager.remove_project(a_id + 1)

    def test_find_projects_by_name(self):
        a = Project('Initialization', 'Work on A')
        b = Project('Progress', 'Work on B')
        c = Project('Final steps', 'Work on C')
        self._project_manager.add_project(a)
        self._project_manager.add_project(b)
        self._project_manager.add_project(c)
        result = self._project_manager.find_projects_by_name('in')
        self.assertEqual(len(result), 2)
        result = self._project_manager.find_projects_by_name('in progress')
        self.assertEqual(len(result), 0)
        result = self._project_manager.find_projects_by_name('PROGRESS')
        self.assertEqual(len(result), 1)
