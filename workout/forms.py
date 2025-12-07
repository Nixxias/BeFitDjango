from django import forms
from .models import ExerciseType, TrainingSession, PerformedExercise
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone

class ExerciseTypeForm(forms.ModelForm):
    class Meta:
        model = ExerciseType
        fields = ['name','description']
        labels = {
            'name': 'Nazwa ćwiczenia',
            'description': 'Opis (opcjonalnie)',
        }

class TrainingSessionForm(forms.ModelForm):
    class Meta:
        model = TrainingSession
        fields = ['start','end','notes']
        labels = {
            'start': 'Data i czas rozpoczęcia',
            'end': 'Data i czas zakończenia',
            'notes': 'Notatki (opcjonalnie)',
        }
        widgets = {
            'start': forms.DateTimeInput(attrs={'type':'datetime-local'}),
            'end': forms.DateTimeInput(attrs={'type':'datetime-local'}),
        }

    def save(self, commit=True, user=None):
        obj = super().save(commit=False)
        if user:
            obj.user = user
        if commit:
            obj.full_clean()
            obj.save()
        return obj

class PerformedExerciseForm(forms.ModelForm):
    class Meta:
        model = PerformedExercise
        fields = ['session','exercise_type','load','sets','reps']
        labels = {
            'session': 'Sesja treningowa',
            'exercise_type': 'Typ ćwiczenia',
            'load': 'Obciążenie (kg)',
            'sets': 'Liczba serii',
            'reps': 'Powtórzenia w serii',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.instance.user = user
            self.fields['session'].queryset = TrainingSession.objects.filter(user=user)
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, label="Adres Email")

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})            
