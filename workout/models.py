from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

class ExerciseType(models.Model):
    name = models.CharField('Nazwa ćwiczenia', max_length=100, unique=True, help_text='Wprowadź czytelną nazwę ćwiczenia.')
    description = models.TextField('Opis', blank=True, help_text='Krótki opis ćwiczenia (opcjonalnie).')

    def clean(self):
        if len(self.name.strip()) < 2:
            raise ValidationError({'name': 'Nazwa musi mieć przynajmniej 2 znaki.'})

    def __str__(self):
        return self.name

class TrainingSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sessions')
    start = models.DateTimeField('Data i czas rozpoczęcia')
    end = models.DateTimeField('Data i czas zakończenia')
    notes = models.TextField('Notatki', blank=True)

    def clean(self):
        if self.end <= self.start:
            raise ValidationError({'end': 'Data zakończenia musi być późniejsza niż data rozpoczęcia.'})
       
        max_span = (self.end - self.start).days
        if max_span > 7:
            raise ValidationError('Sesja nie może trwać dłużej niż 7 dni.')

    def __str__(self):
        return f"Sesja {self.start.strftime('%Y-%m-%d %H:%M')} - {self.end.strftime('%Y-%m-%d %H:%M')}"

class PerformedExercise(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='performed_exercises')
    session = models.ForeignKey(TrainingSession, on_delete=models.CASCADE, related_name='performed_exercises')
    exercise_type = models.ForeignKey(ExerciseType, on_delete=models.PROTECT, related_name='performed')
    load = models.DecimalField('Obciążenie (kg)', max_digits=6, decimal_places=2, help_text='Podaj obciążenie w kilogramach.')
    sets = models.PositiveIntegerField('Liczba serii', help_text='Ile serii wykonano.')
    reps = models.PositiveIntegerField('Powtórzenia w serii', help_text='Ile powtórzeń w jednej serii.')

    def clean(self):
        errors = {}
        if self.load < 0:
            errors['load'] = 'Obciążenie nie może być ujemne.'
        if not (1 <= self.sets <= 100):
            errors['sets'] = 'Liczba serii musi być między 1 a 100.'
        if not (1 <= self.reps <= 1000):
            errors['reps'] = 'Liczba powtórzeń na serię musi być między 1 a 1000.'
        
        if self.session and self.user and self.session.user_id != self.user_id:
            errors['session'] = 'Sesja treningowa nie należy do zalogowanego użytkownika.'
        if errors:
            raise ValidationError(errors)

    def total_reps(self):
        return self.sets * self.reps

    def __str__(self):
        return f"{self.exercise_type.name} w {self.session} — {self.sets}x{self.reps} @ {self.load}kg"
