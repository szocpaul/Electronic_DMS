"""Repository

The repository is in a dedicated directory. This directory contains the following subdirectories by default:

    documents/  - document data and metadata files
    logs/       - logs of the repository events
    projects/   - project files
    users/      - user metadata files
    paths.ini   - the path of the main parts of the repository
    roles.txt   - user roles

The documents directory contains subdirectories which name is the document identifier.

For document metadata we save them to text files with the same name and .info extension next to the directories.

The paths.ini file contains the (relative or absolute) paths of mentioned subdirectories.

The roles.txt contains the user names and the list of assigned roles.
"""

from datetime import datetime
import os

from iniformat.writer import write_ini_file


class Repository(object):
    """Represents the document management system as a repository"""

    def __init__(self, name, location):
        self._name = name
        self._location = location
        self.load()

    def load(self):
        """Try to load an existing repository"""
        if os.path.exists(self._location):
            if os.path.isdir(self._location):
                pass
            else:
                raise ValueError('The repository should be a directory!')
        else:
            self.initialize()

    def initialize(self):
        """Initialize a new repository"""
        os.makedirs(self._location)
        for dir_name in ['documents', 'logs', 'projects', 'users']:
            os.makedirs('{}/{}'.format(self._location, dir_name))
        role_file_path = '{}/roles.txt'.format(self._location)
        with open(role_file_path, 'w') as role_file:
            os.utime(role_file_path, None)
        self.create_default_path_file()
        self._creation_date = datetime.now()

    def create_default_path_file(self):
        data = {
            'directories': {
                'documents': 'documents',
                'logs': 'logs',
                'projects': 'projects',
                'users': 'users'
            }
        }
        write_ini_file('{}/paths.ini'.format(self._location), data)
