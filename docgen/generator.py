#
# Generate random document metadata and content.
#

import random
import string


document_types = ['general', 'office', 'image']

extensions = {
    'general': ['txt', 'html', 'pdf'],
    'office': ['odt', 'ods', 'odp', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx'],
    'image': ['bmp', 'gif', 'jpg', 'jpeg', 'png']
}

topics = ['project', 'programming', 'python', 'management', 'coding', 'admin', 'scheduling', 'interview']

filename_parts = {
    'general': ['overview', 'introduction', 'tutorial', 'book', 'reference'],
    'office': ['summary', 'report', 'notes', 'meeting'],
    'image': ['photo', 'img', 'image', 'scan', 'picture', 'graph', 'copy']
}


class DocumentGenerator(object):
    """Generate various types of documents."""

    def select_document_type(self):
        return random.choice(document_types)

    def generate_filename(self, keyword):
        transform_id = random.randint(0, 2)
        filename = keyword
        if transform_id == 1:
            filename = filename.capitalize()
        elif transform_id == 2:
            filename = filename.upper()
        if random.choice([True, False]):
            filename = filename + random.choice(['', '-', '_', '.'])
            filename = filename + str(random.randint(1, 10000))
        return filename

    def generate_title(self, keyword, topic):
        return '{} {}'.format(topic.capitalize(), keyword)

    def generate_description(self, keyword):
        version = random.randint(1, 3)
        if version == 1:
            return 'The description of {}'.format(keyword)
        elif version == 2:
            return '{} details'.format(keyword.capitalize())
        else:
            return 'Some information about {}'.format(keyword)

    def generate_metadata(self, document_type):
        keyword = random.choice(filename_parts[document_type])
        filename = self.generate_filename(keyword)
        if document_type in ['general', 'office']:
            topic = random.choice(topics)
        else:
            topic = ''
        filename = random.choice(['', '-', '_', '.']) + filename
        transform_id = random.randint(0, 2)
        if transform_id == 1:
            topic = topic.capitalize()
        elif transform_id == 2:
            topic = topic.upper()
        extension = random.choice(extensions[document_type])
        transform_id = random.randint(0, 2)
        if transform_id == 1:
            extension = extension.capitalize()
        elif transform_id == 2:
            extension = extension.upper()
        filename = topic + filename + '.' + extension
        title = self.generate_title(keyword, topic)
        description = self.generate_description(keyword)
        return {
            'filename': filename,
            'title': title,
            'description': description
        }

    def generate_random_file(self, path):
        with open(path, 'w') as random_file:
            random_file.write('The file has created by the document generator.\n\n')
            n_lines = random.randint(5, 100)
            for i in range(n_lines):
                row_length = random.randint(3, 70)
                row = ''.join([random.choice(string.ascii_letters) for i in range(row_length)])
                random_file.write(row + '\n')
