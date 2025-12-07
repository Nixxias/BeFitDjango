from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import ExerciseType, TrainingSession, PerformedExercise
from .forms import ExerciseTypeForm, TrainingSessionForm, PerformedExerciseForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Avg, Max, F, ExpressionWrapper, DecimalField, IntegerField
from .forms import UserRegisterForm
from django.contrib.auth import login

class ExerciseTypeListView(ListView):
    model = ExerciseType
    template_name = 'workout/exercisetype_list.html'
    context_object_name = 'types'

# Admin-only create/update/delete for ExerciseType
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class ExerciseTypeCreateView(AdminRequiredMixin, LoginRequiredMixin, View):
    def get(self, request):
        form = ExerciseTypeForm()
        return render(request, 'workout/exercisetype_form.html', {'form': form, 'title': 'Dodaj typ ćwiczenia'})

    def post(self, request):
        form = ExerciseTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Typ ćwiczenia dodany.')
            return redirect('exercise-types')
        return render(request, 'workout/exercisetype_form.html', {'form': form})

class ExerciseTypeUpdateView(AdminRequiredMixin, LoginRequiredMixin, View):
    def get(self, request, pk):
        obj = get_object_or_404(ExerciseType, pk=pk)
        form = ExerciseTypeForm(instance=obj)
        return render(request, 'workout/exercisetype_form.html', {'form': form, 'title': 'Edytuj typ ćwiczenia'})

    def post(self, request, pk):
        obj = get_object_or_404(ExerciseType, pk=pk)
        form = ExerciseTypeForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Zapisano zmiany.')
            return redirect('exercise-types')
        return render(request, 'workout/exercisetype_form.html', {'form': form})

class ExerciseTypeDeleteView(AdminRequiredMixin, LoginRequiredMixin, View):
    def post(self, request, pk):
        obj = get_object_or_404(ExerciseType, pk=pk)
        obj.delete()
        messages.success(request, 'Usunięto typ ćwiczenia.')
        return redirect('exercise-types')

# Training sessions CRUD - only owner can manage
class TrainingSessionListView(LoginRequiredMixin, ListView):
    model = TrainingSession
    template_name = 'workout/session_list.html'
    context_object_name = 'sessions'

    def get_queryset(self):
        return TrainingSession.objects.filter(user=self.request.user).order_by('-start')

class TrainingSessionCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = TrainingSessionForm()
        return render(request, 'workout/session_form.html', {'form': form, 'title':'Nowa sesja treningowa'})

    def post(self, request):
        form = TrainingSessionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Sesja zapisana.')
            return redirect('session-list')
        return render(request, 'workout/session_form.html', {'form': form})

class TrainingSessionUpdateView(LoginRequiredMixin, View):
    def get_object(self, pk):
        return get_object_or_404(TrainingSession, pk=pk, user=self.request.user)
    def get(self, request, pk):
        obj = self.get_object(pk)
        form = TrainingSessionForm(instance=obj)
        return render(request, 'workout/session_form.html', {'form': form, 'title':'Edytuj sesję'})
    def post(self, request, pk):
        obj = self.get_object(pk)
        form = TrainingSessionForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Zapisano zmiany.')
            return redirect('session-list')
        return render(request, 'workout/session_form.html', {'form': form})

class TrainingSessionDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        obj = get_object_or_404(TrainingSession, pk=pk, user=request.user)
        obj.delete()
        messages.success(request, 'Usunięto sesję.')
        return redirect('session-list')

# PerformedExercise CRUD - only owner can manage; session dropdown limited to user's sessions
class PerformedExerciseListView(LoginRequiredMixin, ListView):
    model = PerformedExercise
    template_name = 'workout/performed_list.html'
    context_object_name = 'performed'

    def get_queryset(self):
        return PerformedExercise.objects.filter(user=self.request.user).order_by('-session__start')

class PerformedExerciseCreateView(LoginRequiredMixin, CreateView):
    model = PerformedExercise
    form_class = PerformedExerciseForm
    template_name = 'workout/performed_form.html'
    success_url = reverse_lazy('performed-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Ćwiczenie zapisane.')
        return super().form_valid(form)

class PerformedExerciseUpdateView(LoginRequiredMixin, View):
    def get_object(self, pk):
        return get_object_or_404(PerformedExercise, pk=pk, user=self.request.user)

    def get(self, request, pk):
        obj = self.get_object(pk)
        form = PerformedExerciseForm(instance=obj, user=request.user)
        return render(request, 'workout/performed_form.html', {'form': form, 'title':'Edytuj wykonane ćwiczenie'})

    def post(self, request, pk):
        obj = self.get_object(pk)
        form = PerformedExerciseForm(request.POST, instance=obj, user=request.user)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.user = request.user
            inst.full_clean()
            inst.save()
            messages.success(request, 'Zapisano zmiany.')
            return redirect('performed-list')
        return render(request, 'workout/performed_form.html', {'form': form})

class PerformedExerciseDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        obj = get_object_or_404(PerformedExercise, pk=pk, user=request.user)
        obj.delete()
        messages.success(request, 'Usunięto ćwiczenie.')
        return redirect('performed-list')

# User statistics for last 4 weeks
def stats_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    now = timezone.now()
    four_weeks_ago = now - timezone.timedelta(weeks=4)
    sessions = TrainingSession.objects.filter(user=request.user, start__gte=four_weeks_ago)
    performed = PerformedExercise.objects.filter(user=request.user, session__in=sessions)
    # aggregate per exercise_type
    stats = performed.values('exercise_type__id','exercise_type__name').annotate(
        times=Sum(1),
        total_reps=Sum(ExpressionWrapper(F('sets')*F('reps'), output_field=IntegerField())),
        avg_load=Avg('load'),
        max_load=Max('load'),
    ).order_by('-total_reps')
    return render(request, 'workout/stats.html', {'stats': stats, 'sessions_count': sessions.count()})
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Konto zostało utworzone dla {user.username}!')
            return redirect('exercise-types')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})