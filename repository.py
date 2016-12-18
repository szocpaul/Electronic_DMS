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

# from datetime import datetime
import os
import shutil


def get_instance(configuration):
    return Repository(configuration)


class Repository(object):
    """Represents the document management system as a repository"""

    def __init__(self, configuration):
        if "repository" not in configuration:
            raise KeyError("repository not found in configuration")
        if "location" not in configuration['repository']:
            raise KeyError("repository.location is not configured")
        self.base = configuration['repository']['location']

    def get_dir(self, uuid, documents="documents"):
        return self.base + "/" + str(uuid) + "/" + documents + "/"

    def load(self, uuid, file_path):
        """Try to load an existing repository"""
        directory = self.get_dir(uuid, documents="documents")
        if not os.path.exists(directory):
            os.makedirs(directory)
        shutil.copy2(file_path, directory)

    def save(self, uuid, _file, file_name):
        directory = self.get_dir(uuid, documents="documents")
        if not os.path.exists(directory):
            os.makedirs(directory)
        target = os.path.join(directory, file_name)
        _file.save(target)

    def get(self, uuid, file=None, basename_only=False):
        result = []
        directory = self.get_dir(uuid, documents="documents")
        for (dir_path, dir_names, file_names) in os.walk(directory):
            result = file_names
            break
        if basename_only:
            prefix = ""
        else:
            prefix = directory
        if file is not None:
            if file in result:
                return prefix + file
            return None
        return [prefix + r for r in result]

    def remove(self, uuid):
        full = self.get_dir(uuid)
        try:
            os.remove(full)
        except OSError:
            return False
        return True

    def remove_dir(self, uuid):
        directory = self.get_dir(uuid)
        try:
            shutil.rmtree(directory)
        except OSError:
            pass
