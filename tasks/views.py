from asyncio import tasks
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView

from tasks.models import Task
# Create your views here.


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "tasks/create_task.html"
    fields = ["name", "start_date", "due_date", "project", "assignee"]

    def get_queryset(self):
        return Task.objects.filter(members=self.request.user)

    def form_valid(self, form):
        item = form.save(commit=False)
        item.members = self.request.user
        item.save()
        return redirect("show_project", pk=item.id)
