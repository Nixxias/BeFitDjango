from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import ExerciseType, TrainingSession, PerformedExercise
import datetime
from django.utils import timezone

class BasicTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='u', password='p')
        self.type = ExerciseType.objects.create(name='Przysiad')
        self.session = TrainingSession.objects.create(user=self.user, start=timezone.now(), end=timezone.now()+datetime.timedelta(hours=1))
        self.perf = PerformedExercise.objects.create(user=self.user, session=self.session, exercise_type=self.type, load=50, sets=3, reps=5)

    def test_total_reps(self):
        self.assertEqual(self.perf.total_reps(), 15)
