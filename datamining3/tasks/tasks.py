from huey.contrib.djhuey import task, periodic_task, db_task, db_periodic_task, on_startup
from huey import crontab
from .models import Task, TaskState
import datetime


def set_task_state(name, state):
    try:
        task = Task.objects.get(task_name=name)
        
        if state.value == TaskState.Running.value:
            task.current_state = state.value
            task.last_run = datetime.datetime.now()
        else:
            task.last_run_status = state.value
            task.current_state = TaskState.Unknown.value
        task.save()
    except Task.DoesNotExist:
        print('Task ',name,' doesnt exist')