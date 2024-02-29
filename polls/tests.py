import datetime

from django.test import TestCase
from django.utils import timezone

from .models.question import Question

# Create your tests here.
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self) -> None:
        """
        Ensuring that was_published_recently() returns False for questions
        whose pub_date attributes are in the future.
        """

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_published_recently_with_old_question(self) -> None:
        """
        Ensuring that was_published_recently() returns False for questions
        whose pub_date attribute is older than one day
        """

        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        past_question = Question(pub_date=time)

        self.assertIs(past_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self) -> None:
        """
        Ensuring that was_published_recently() returns True for questions
        whose pub_date attribute is today or yesterday
        """
        one_day_ago = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        now = timezone.now()

        recent_question = Question(pub_date=one_day_ago)
        new_question = Question(pub_date=now)

        self.assertIs(recent_question.was_published_recently(), True)
        self.assertIs(new_question.was_published_recently(), True)