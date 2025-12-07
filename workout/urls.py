from django.urls import path
from . import views

urlpatterns = [
    path('', views.ExerciseTypeListView.as_view(), name='exercise-types'),
    path('types/add/', views.ExerciseTypeCreateView.as_view(), name='exercise-type-add'),
    path('types/<int:pk>/edit/', views.ExerciseTypeUpdateView.as_view(), name='exercise-type-edit'),
    path('types/<int:pk>/delete/', views.ExerciseTypeDeleteView.as_view(), name='exercise-type-delete'),

    path('sessions/', views.TrainingSessionListView.as_view(), name='session-list'),
    path('sessions/add/', views.TrainingSessionCreateView.as_view(), name='session-add'),
    path('sessions/<int:pk>/edit/', views.TrainingSessionUpdateView.as_view(), name='session-edit'),
    path('sessions/<int:pk>/delete/', views.TrainingSessionDeleteView.as_view(), name='session-delete'),

    path('performed/', views.PerformedExerciseListView.as_view(), name='performed-list'),
    path('performed/add/', views.PerformedExerciseCreateView.as_view(), name='performed-add'),
    path('performed/<int:pk>/edit/', views.PerformedExerciseUpdateView.as_view(), name='performed-edit'),
    path('performed/<int:pk>/delete/', views.PerformedExerciseDeleteView.as_view(), name='performed-delete'),
    path('register/', views.register, name='register'),
    path('stats/', views.stats_view, name='stats'),
]
