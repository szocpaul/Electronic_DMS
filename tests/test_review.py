import unittest

from reviews import Review


class TestReview(unittest.TestCase):
    """Test the review class

    The arguments of review methods are arbitrary objects which contains data about
    the messages of the review process.
    """

    def test_review_creation(self):
        review = Review()

    def test_valid_steps(self):
        review = Review()
        review.set_submission('Author submission (submission.doc)')
        review.set_review_request_1('Request the first reviewer')
        review.set_review_request_2('Request the second reviewer')
        review.set_review_response_1('Response from the first reviewer')
        review.set_review_response_2('Response from the second reviewer')
        review.set_evaluation_result('Evaluation result to the author')

    def test_invalid_steps(self):
        review = Review()
        with self.assertRaises(ValueError):
            review.set_review_request_1('Request the first reviewer')
        with self.assertRaises(ValueError):
            review.set_review_request_2('Request the second reviewer')
        with self.assertRaises(ValueError):
            review.set_review_response_1('Response from the first reviewer')
        with self.assertRaises(ValueError):
            review.set_review_response_2('Response from the second reviewer')
        with self.assertRaises(ValueError):
            review.set_evaluation_result('Evaluation result to the author')

    def test_invalid_previous_steps(self):
        review = Review()
        review.set_submission('Author submission (submission.doc)')
        review.set_review_request_1('Request the first reviewer')
        review.set_review_request_2('Request the second reviewer')
        with self.assertRaises(ValueError):
            review.set_review_request_2('Request the second reviewer')
        with self.assertRaises(ValueError):
            review.set_review_request_1('Request the first reviewer')
        with self.assertRaises(ValueError):
            review.set_submission('Author submission (submission.doc)')
