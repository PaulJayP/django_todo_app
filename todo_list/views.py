from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.utils.timezone import make_aware

from .forms import TodoForm,  TodoFormUpdate
from .models import TodoItem

# Create your views here.

###############################################


def index(request):
    """ Used in the main dashboard.task list view.
    Returns all TodoItem objects when unauthorised and a
    filtered set by user when logged in.

    :param request: Http request object.
    :return: A template containing TodoItem task objects.
    """

    if request.user.is_anonymous:
        item_list = TodoItem.objects.order_by("-updated_at")
    else:
        user = request.user
        item_list = TodoItem.objects.filter(user=user).order_by("-updated_at")

    form = TodoForm()

    page = {
        "forms": form,
        "list": item_list,
        "title": "TODO LIST",
    }
    return render(request, 'index.html', page)


@login_required()
def create_form(request):
    """ Used to return the TodoForm create.html task template.

    :param request: Http request object.
    :return: A TodoForm form template.
    """

    form = TodoForm()
    return render(request, 'create.html', {"forms": form})


@login_required()
def create_task(request):
    """ Used to create a new Task using POSTED form data.

    :param request: Http request object.
    :return: A redirect on success or fail.
    """

    form = TodoForm(request.POST)

    if form.is_valid():

        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        messages.info(request, "Task created")
        return index(request)

    messages.error(request, "Task not created")
    return create_form(request)


@login_required()
def delete_task(request, task_id):
    """ Used to delete an existing task.
    Requires the current User to own the Task record.

    :param request: Http request object.
    :param task_id: Task TodoItem id
    :return: A redirect on success or fail.
    """

    task = TodoItem.objects.get(id=task_id)

    # basic auth
    if task.user != request.user:
        messages.error(request, "Unauthorized to delete this task.")
        return index(request)

    task.delete()
    messages.info(request, "Task removed")
    return index(request)


@login_required()
def edit_form(request, task_id):
    """ Used to return a TodoFormUpdate template
    using the given task_id.
    Requires the current User to own the Task record.

    :param request: Http request object.
    :param task_id: Task TodoItem id
    :return: A redirect on success or fail.
    """

    task = TodoItem.objects.get(id=task_id)
    form = TodoFormUpdate(instance=task)

    # basic auth
    if task.user != request.user:
        messages.error(request, "Unauthorized to view this page.")
        return index(request)

    data = {
        'forms': form,
        'task_id': task_id,
    }

    loc_weather = {}
    if task.city.temp_code:
        loc_weather['temp_code'] = task.city.temp_code
        loc_weather['temp'] = task.city.temperature
    if loc_weather:
        data['loc_weather'] = loc_weather

    return render(request, 'edit.html', data)


@login_required()
def edit_task(request, task_id):
    """ Used to edit an existing Task TodoItem using
    the given task_id and POSTED form data.
    Requires the current User to own the Task record.

    :param request: Http request object.
    :param task_id: Task TodoItem id
    :return: A redirect on success or fail.
    """

    task = TodoItem.objects.get(id=task_id)
    form = TodoForm(request.POST, instance=task)

    # basic auth
    if task.user != request.user:
        messages.error(request, "Unauthorized to edit this task.")
        return index(request)

    form.data = request.POST

    if form.is_valid():
        obj = form.save(commit=False)

        if request.POST.get('task_complete') is not None:
            obj.completed_at = make_aware(datetime.utcnow())

        obj.save()

        messages.info(request, "Task updated")
        return index(request)

    messages.error(request, "Task not updated")
    return edit_form(request)
