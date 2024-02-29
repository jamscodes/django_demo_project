import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models.question import Question

# Create your tests here.
def create_question(question_text, days) -> Question:
    """
    Create a question with the given `question_text`
    and set its `pub_date` attribute to be now() offset
    by the given `days`. Negative `pub_date` indicates
    a question published in the past while positive
    indicates a question to be published in the future.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self) -> None:
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            []
        )

    def test_past_question(self) -> None:
        """
        Questions with a `pub_date` in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question", days=-30)
        response = self.client.get(reverse("polls:index"))
        
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question]
        )
    
    def test_future_question(self) -> None:
        """
        Questions with a `pub_date` in the future are not displayed
        on the index page.
        """
        create_question(question_text="Future question", days=30)
        response = self.client.get(reverse("polls:index"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            []
        )

    def test_future_question_and_past_question(self) -> None:
        """
        Even if both past and future questions exist, only past
        questions are displayed.
        """
        past_question = create_question(question_text="Past question", days=-30)
        create_question(question_text="Future question", days=30)
        response = self.client.get(reverse("polls:index"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [past_question]
        )

    def test_multiple_past_questions(self) -> None:
        """
        Index page should be allowed to display multiple questions
        if those questions all have valid `pub_date` values.
        """
        past_question_1 = create_question(question_text="Past question 1", days=-30)
        past_question_2 = create_question(question_text="Past question 2", days=-5)
        response = self.client.get(reverse("polls:index"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [past_question_2, past_question_1]
        )

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