from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from test1.global_function import CustomValidations as GF
import json
from manager.models import Task
import pika
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import AcceptTask
from manager.views import taskAddHighQueue, taskAddMediumQueue, taskAddLowQueue


def dashboard(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return HttpResponse(json.dumps({'status': 0, 'error': 'Please Login'}))
        #variable
        new_task = None
        task_id = getNewTask(request, 0)
        if task_id != 0:
            new_task = Task.objects.get(id=int(task_id))

            #check whether this task is cancelled
            if new_task.status == 3:
                task_id=getNewTask(request,1)
                new_task = None
                
        accepted_task = AcceptTask.objects.filter(user=request.user)

        context = { 'new_task': new_task, 'accepted_task': accepted_task }
        return render(request, 'deliveryBoy/dashboard.html', context)

def acceptTask(request, id):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return HttpResponse(json.dumps({'status': 0, 'error': 'Please Login'}))
        #variable
        existTask = None
        acceptTask = None
        task = None
        user = None
        try:
            task = Task.objects.get(id=id)
            user = User.objects.get(id=request.user.id)
        except Exception as e:
            return HttpResponse(json.dumps({'status': 0, 'error': str(e)}))

        try:
            existTask = AcceptTask.objects.get(user=user,task=task)
        except Exception as e:
            pass
        else:
            return redirect('/delivery-boy/dashboard/')
        #accepting task
        try:
            #calling que to remove this task from que
            task_id = getNewTask(request, 1)

            task.status = 1
            task.save()

            acceptTask = AcceptTask()
            acceptTask.user = user
            acceptTask.task = task
            acceptTask.save()
        except Exception as e:
            return HttpResponse(json.dumps({'status': 0, 'error': str(e)}))
        return redirect("/delivery-boy/dashboard/")


def getNewTask(request, ack_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()


    channel.queue_declare(queue='taskHigh')
    method_frame, header_frame, body = channel.basic_get(queue = 'taskHigh')

    if method_frame == None:
        connection.close()
        return getMediumTask(request, ack_id)
    else:            
        channel.basic_ack(delivery_tag=ack_id)
        connection.close() 
        return body

def getMediumTask(request, ack_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()


    channel.queue_declare(queue='taskMedium')
    method_frame, header_frame, body = channel.basic_get(queue = 'taskMedium')

    if method_frame == None:
        connection.close()
        return getLowTask(request, ack_id)
    else:            
        channel.basic_ack(delivery_tag=ack_id)
        connection.close() 
        return body

def getLowTask(request, ack_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()


    channel.queue_declare(queue='taskLow')
    method_frame, header_frame, body = channel.basic_get(queue = 'taskLow')

    if method_frame == None:
        connection.close()
        return 0
    else:            
        channel.basic_ack(delivery_tag=ack_id)
        connection.close() 
        return body

def declineTask(request, id):
    if request.method == 'GET':
        #variable
        task = None
        try:
            task = Task.objects.get(id=id)
        except Exception as e:
            return HttpResponse(json.dumps({'status': 0, 'error': str(e)}))

        try:
            task.status = 0
            task.save()

            acceptTask = AcceptTask.objects.get(user=request.user, task=task)
            acceptTask.delete()

            if task.priority == 2:
                taskAddHighQueue(request, task.id)
            elif task.priority == 1:
                taskAddMediumQueue(request, task.id)
            elif task.priority == 0:
                taskAddLowQueue(request, task.id)

        except Exception as e:
            return HttpResponse(json.dumps({'status': 0, 'error': str(e)}))

        return redirect("/delivery-boy/dashboard/")

def completedTask(request, id):
    if request.method == 'GET':
        #variable
        task = None
        try:
            task = Task.objects.get(id=id)
        except Exception as e:
            return HttpResponse(json.dumps({'status': 0, 'error': str(e)}))

        try:
            task.status = 2
            task.save()

        except Exception as e:
            return HttpResponse(json.dumps({'status': 0, 'error': str(e)}))

        return redirect("/delivery-boy/dashboard/")
