from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import (
    DetailView
)
from .tasks import *
from shared.utils import get_in_preferred_tz

# Create your views here.
def get_tasks(request):
    template_name = 'tasks/task_list.html'
    
    available_tasks = {}
    for task in available_tasks.keys():
        found = False
        for task_obj in Task.objects.all():
            if task_obj.task_name == task:
                found = True
        if not found:
            Task.objects.create(
                task_name = task,
                description = available_tasks[task]['description']
            )
    task_list = list()
    for task_obj in Task.objects.all():
        task = dict()
        task['id'] = task_obj.id
        task['description'] = task_obj.description
        task['current_state'] = Task.TASK_STATE_CHOICES[task_obj.current_state][1]
        if task_obj.last_run:
            task['last_run'] = get_in_preferred_tz(task_obj.last_run)
        task['last_run_status'] = Task.TASK_STATE_CHOICES[task_obj.last_run_status][1]
        task_list.append(task)
    context = {'task_list':task_list, 'curr_module_id': 'id_internals_module'}
    return render(request, template_name, context)

def get_task_state_to_name_mapping():
    task_sate_mapping = dict()
    for state, name in Task.TASK_STATE_CHOICES:
        task_sate_mapping[state] = name
    return task_sate_mapping

def run_task(request, id):
    task = get_object_or_404(Task, id=id)
    possibles = globals().copy()
    possibles.update(locals())
    method = possibles.get(task.task_name)
    if not method:
        raise NotImplementedError("Method %s not implemented" % task.task_name)
    
    if task.current_state == TaskState.Unknown.value:
        task.current_state = TaskState.Scheduled.value
        task.save()
    method()
    return HttpResponseRedirect('../../')

class TaskDetailView(DetailView):
    template_name = 'tasks/task_detail.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Task, id=id_)
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        print(data)
        return data
