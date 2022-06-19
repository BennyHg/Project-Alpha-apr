from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from tasks.models import Task
# Create your views here.


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "tasks/create_task.html"
    fields = ["name", "start_date", "due_date", "project", "assignee"]

    def get_queryset(self):
        return Task.objects.filter(members=self.request.user)

    def form_valid(self, form):
        job = form.save(commit=False)
        job.members = self.request.user
        job.save()
        return redirect("show_project", pk=job.id)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"

    def get_queryset(self):
        return Task.objects.filter(assignee=self.request.user)