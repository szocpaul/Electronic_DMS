from datetime import date
import os
import shutil
import unittest

from documents import Document
from documents import DocumentManager
from users import User
from users import UserManager
from reviews import ReviewManager


class TestReviewManager(unittest.TestCase):
    """Test the review manager class"""

    def setUp(self):
        self.prepare_repository_files()
        self.create_manager_objects()
        self.create_participants()

    def prepare_repository_files(self):
        try:
            shutil.rmtree('/tmp/edms')
        except OSError:
            pass
        os.makedirs('/tmp/edms')
        os.makedirs('/tmp/edms/users')
        os.makedirs('/tmp/edms/documents')
        os.makedirs('/tmp/edms/reviews')
        os.makedirs('/tmp/edms/samples')
        stages = ['submission', 'request_1', 'request_2', 'response_1', 'response_2', 'evaluation_result']
        for stage in stages:
            with open('/tmp/edms/samples/{}.pdf'.format(stage), 'w') as stage_file:
                stage_file.write('Sample {} file'.format(stage))

    def create_manager_objects(self):
        self._user_manager = UserManager('/tmp/edms/users')
        self._document_manager = DocumentManager('/tmp/edms/documents')
        self._review_manager = ReviewManager('/tmp/edms/reviews', self._user_manager, self._document_manager)

    def create_participants(self):
        author = User('Author', 'Test', date(1980, 10, 1), 'author.test@mail.com', 'author')
        manager = User('Manager', 'Test', date(1985, 10, 1), 'manager.test@mail.com', 'manager')
        reviewer_1 = User('Reviewer1', 'Test', date(1985, 1, 1), 'reviewer1.test@mail.com', 'reviewer')
        reviewer_2 = User('Reviewer2', 'Test', date(1985, 1, 2), 'reviewer2.test@mail.com', 'reviewer')
        self._author_id = self._user_manager.add_user(author)
        self._manager_id = self._user_manager.add_user(manager)
        self._reviewer_1_id = self._user_manager.add_user(reviewer_1)
        self._reviewer_2_id = self._user_manager.add_user(reviewer_2)
        self._user_manager.add_role(self._author_id, 'author')
        self._user_manager.add_role(self._manager_id, 'manager')
        self._user_manager.add_role(self._reviewer_1_id, 'reviewer')
        self._user_manager.add_role(self._reviewer_2_id, 'reviewer')

    def tearDown(self):
        shutil.rmtree('/tmp/edms')

    def test_document_selection(self):
        submission = Document('Submission', 'First submission', 1, ['/tmp/edms/samples/submission.pdf'], 'pdf')
        submission_id = self._document_manager.add_document(submission)
        self._review_manager.select_document(submission_id)

    def test_submission(self):
        submission = Document('Submission', 'First submission', 1, ['/tmp/edms/samples/submission.pdf'], 'pdf')
        submission_id = self._document_manager.add_document(submission)
        self._review_manager.select_document(submission_id)
        self._review_manager.submit_document(self._author_id, self._manager_id, submission_id)
        self._review_manager.save_review()

    def test_submission_with_invalid_roles(self):
        submission = Document('Submission', 'First submission', 1, ['/tmp/edms/samples/submission.pdf'], 'pdf')
        submission_id = self._document_manager.add_document(submission)
        self._review_manager.select_document(submission_id)
        self._user_manager.remove_role(self._author_id, 'author')
        with self.assertRaises(ValueError):
            self._review_manager.submit_document(self._author_id, self._manager_id, submission_id)
        self._review_manager.save_review()

    def test_review_request_1(self):
        submission = Document('Submission', 'First submission', 1, ['/tmp/edms/samples/submission.pdf'], 'pdf')
        submission_id = self._document_manager.add_document(submission)
        request_1 = Document('request_1', 'First request', 1, ['/tmp/edms/samples/request_1.pdf'], 'pdf')
        request_1_id = self._document_manager.add_document(request_1)
        self._review_manager.select_document(submission_id)
        self._review_manager.submit_document(self._author_id, self._manager_id, submission_id)
        self._review_manager.send_reviewing_request_1(self._manager_id, self._reviewer_1_id, request_1_id)
        self._review_manager.save_review()

    def test_review_request_2(self):
        submission = Document('Submission', 'First submission', 1, ['/tmp/edms/samples/submission.pdf'], 'pdf')
        submission_id = self._document_manager.add_document(submission)
        request_1 = Document('request_1', 'First request', 1, ['/tmp/edms/samples/request_1.pdf'], 'pdf')
        request_1_id = self._document_manager.add_document(request_1)
        request_2 = Document('request_2', 'Second request', 1, ['/tmp/edms/samples/request_2.pdf'], 'pdf')
        request_2_id = self._document_manager.add_document(request_2)
        self._review_manager.select_document(submission_id)
        self._review_manager.submit_document(self._author_id, self._manager_id, submission_id)
        self._review_manager.send_reviewing_request_1(self._manager_id, self._reviewer_1_id, request_1_id)
        self._review_manager.send_reviewing_request_2(self._manager_id, self._reviewer_2_id, request_2_id)
        self._review_manager.save_review()

    def test_invalid_review_request_order(self):
        submission = Document('Submission', 'First submission', 1, ['/tmp/edms/samples/submission.pdf'], 'pdf')
        submission_id = self._document_manager.add_document(submission)
        request_1 = Document('request_1', 'First request', 1, ['/tmp/edms/samples/request_1.pdf'], 'pdf')
        request_1_id = self._document_manager.add_document(request_1)
        request_2 = Document('request_2', 'Second request', 1, ['/tmp/edms/samples/request_2.pdf'], 'pdf')
        request_2_id = self._document_manager.add_document(request_2)
        self._review_manager.select_document(submission_id)
        self._review_manager.submit_document(self._author_id, self._manager_id, submission_id)
        with self.assertRaises(ValueError):
            self._review_manager.send_reviewing_request_2(self._manager_id, self._reviewer_2_id, request_2_id)
            self._review_manager.send_reviewing_request_1(self._manager_id, self._reviewer_1_id, request_1_id)
        self._review_manager.save_review()

    def test_review_responses(self):
        submission = Document('Submission', 'First submission', 1, ['/tmp/edms/samples/submission.pdf'], 'pdf')
        submission_id = self._document_manager.add_document(submission)
        request_1 = Document('request_1', 'First request', 1, ['/tmp/edms/samples/request_1.pdf'], 'pdf')
        request_1_id = self._document_manager.add_document(request_1)
        request_2 = Document('request_2', 'Second request', 1, ['/tmp/edms/samples/request_2.pdf'], 'pdf')
        request_2_id = self._document_manager.add_document(request_2)
        response_1 = Document('response_1', 'First response', 1, ['/tmp/edms/samples/response_1.pdf'], 'pdf')
        response_1_id = self._document_manager.add_document(response_1)
        response_2 = Document('response_2', 'Second response', 1, ['/tmp/edms/samples/response_2.pdf'], 'pdf')
        response_2_id = self._document_manager.add_document(response_2)
        self._review_manager.select_document(submission_id)
        self._review_manager.submit_document(self._author_id, self._manager_id, submission_id)
        self._review_manager.send_reviewing_request_1(self._manager_id, self._reviewer_1_id, request_1_id)
        self._review_manager.send_reviewing_request_2(self._manager_id, self._reviewer_2_id, request_2_id)
        self._review_manager.send_review_1(self._reviewer_1_id, self._manager_id, response_1_id)
        self._review_manager.send_review_2(self._reviewer_2_id, self._manager_id, response_2_id)
        self._review_manager.save_review()

    def test_review_response_with_invalid_role(self):
        submission = Document('Submission', 'First submission', 1, ['/tmp/edms/samples/submission.pdf'], 'pdf')
        submission_id = self._document_manager.add_document(submission)
        request_1 = Document('request_1', 'First request', 1, ['/tmp/edms/samples/request_1.pdf'], 'pdf')
        request_1_id = self._document_manager.add_document(request_1)
        request_2 = Document('request_2', 'Second request', 1, ['/tmp/edms/samples/request_2.pdf'], 'pdf')
        request_2_id = self._document_manager.add_document(request_2)
        response_1 = Document('response_1', 'First response', 1, ['/tmp/edms/samples/response_1.pdf'], 'pdf')
        response_1_id = self._document_manager.add_document(response_1)
        response_2 = Document('response_2', 'Second response', 1, ['/tmp/edms/samples/response_2.pdf'], 'pdf')
        response_2_id = self._document_manager.add_document(response_2)
        self._review_manager.select_document(submission_id)
        self._review_manager.submit_document(self._author_id, self._manager_id, submission_id)
        self._review_manager.send_reviewing_request_1(self._manager_id, self._reviewer_1_id, request_1_id)
        self._review_manager.send_reviewing_request_2(self._manager_id, self._reviewer_2_id, request_2_id)
        self._review_manager.send_review_1(self._reviewer_1_id, self._manager_id, response_1_id)
        with self.assertRaises(ValueError):
            self._review_manager.send_review_2(self._author_id, self._manager_id, response_2_id)
        self._review_manager.save_review()

    def test_reviewing_process_with_evaluation(self):
        submission = Document('Submission', 'First submission', 1, ['/tmp/edms/samples/submission.pdf'], 'pdf')
        submission_id = self._document_manager.add_document(submission)
        request_1 = Document('request_1', 'First request', 1, ['/tmp/edms/samples/request_1.pdf'], 'pdf')
        request_1_id = self._document_manager.add_document(request_1)
        request_2 = Document('request_2', 'Second request', 1, ['/tmp/edms/samples/request_2.pdf'], 'pdf')
        request_2_id = self._document_manager.add_document(request_2)
        response_1 = Document('response_1', 'First response', 1, ['/tmp/edms/samples/response_1.pdf'], 'pdf')
        response_1_id = self._document_manager.add_document(response_1)
        response_2 = Document('response_2', 'Second response', 1, ['/tmp/edms/samples/response_2.pdf'], 'pdf')
        response_2_id = self._document_manager.add_document(response_2)
        evaluation_result = Document('response_2', 'Second response', 1, ['/tmp/edms/samples/evaluation_result.pdf'], 'pdf')
        evaluation_result_id = self._document_manager.add_document(evaluation_result)
        self._review_manager.select_document(submission_id)
        self._review_manager.submit_document(self._author_id, self._manager_id, submission_id)
        self._review_manager.save_review()
        self._review_manager.send_reviewing_request_1(self._manager_id, self._reviewer_1_id, request_1_id)
        self._review_manager.save_review()
        self._review_manager.send_reviewing_request_2(self._manager_id, self._reviewer_2_id, request_2_id)
        self._review_manager.save_review()
        self._review_manager.send_review_1(self._reviewer_1_id, self._manager_id, response_1_id)
        self._review_manager.save_review()
        self._review_manager.send_review_2(self._reviewer_2_id, self._manager_id, response_2_id)
        self._review_manager.save_review()
        self._review_manager.send_evaluation(self._manager_id, self._author_id, evaluation_result_id)
        self._review_manager.save_review()
