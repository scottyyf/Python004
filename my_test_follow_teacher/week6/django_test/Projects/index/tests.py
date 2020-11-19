from django.test import TestCase

# Create your tests here.
import datetime

from django.utils import timezone
from .models import Question


class QuestionModelsTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        f = Question(pub_date=time)
        self.assertIs(f.was_published_recently(), False)
