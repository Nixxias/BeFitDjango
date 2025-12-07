from django.contrib import admin
from .models import ExerciseType, TrainingSession, PerformedExercise

@admin.register(ExerciseType)
class ExerciseTypeAdmin(admin.ModelAdmin):
    list_display = ('name','description')

@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = ('user','start','end')

@admin.register(PerformedExercise)
class PerformedExerciseAdmin(admin.ModelAdmin):
    list_display = ('user','session','exercise_type','load','sets','reps')
