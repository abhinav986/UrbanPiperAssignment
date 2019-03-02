from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from test1.global_function import CustomValidations as GF
import json
from .models import Task
import pika
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

# Create your views here.

def dashboard(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return HttpResponse(json.dumps({'status': 0, 'error': 'Please Login'}))
        else:
            tasks = Task.objects.filter(createdBy=request.user)
            context = { 'tasks': tasks }
            return render(request, 'manager/dashboard.html', context)

@csrf_exempt
def createTask(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return HttpResponse(json.dumps({'status': 0, 'error': 'Please Login'}))
        
        return render(request, 'manager/taskCreate.html')
    
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponse(json.dumps({'status': 0, 'error': 'Please Login'}))
        
        #parameter validation
        string = []
        stringRequired = ['title','priority']
        inte = []
        intRequired = []
        msg, status = GF.dataValidation(request, string, stringRequired, inte, intRequired)
        if status == 0:
            return HttpResponse(json.dumps({'status': 0, 'error': msg}))
        #user
        user = User.objects.get(id=request.user.id)
        task = None

        try:
            task = Task()
            task.title = request.POST['title']
            task.createdBy = user
            task.priority = request.POST['priority']
            task.status = 0
            task.save()
        except Exception as e:
            return HttpResponse(json.dumps({'status': 0, 'error': str(e)}))
        
        #add task to queue
        if task.priority == str(2):
            taskAddHighQueue(request, task.id)
        elif task.priority == str(1):
            taskAddMediumQueue(request, task.id)
        elif task.priority == str(0):
            taskAddLowQueue(request, task.id)

        return redirect("/manager/dashboard/")

def taskAddHighQueue(request, id):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()


    channel.queue_declare(queue='taskHigh')

    channel.basic_publish(exchange='',
                        routing_key='taskHigh',
                        body=str(id))
    print("added")
    connection.close()

def taskAddMediumQueue(request, id):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()


    channel.queue_declare(queue='taskLow')

    channel.basic_publish(exchange='',
                        routing_key='taskLow',
                        body=str(id))
    print("added")
    connection.close()

def taskAddLowQueue(request, id):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()


    channel.queue_declare(queue='taskLow')

    channel.basic_publish(exchange='',
                        routing_key='taskLow',
                        body=str(id))
    print("added")
    connection.close()

def cancelTask(request, id):
    if request.method == 'GET':
        #variable
        task = None
        try:
            task = Task.objects.get(id=id)
        except Exception as e:
            return HttpResponse(json.dumps({'status': 0, 'error': str(e)}))
        try:
            task.status = 3
            task.save()
        except Exception as e:
            return HttpResponse(json.dumps({'status': 0, 'error': str(e)}))
        return redirect("/manager/dashboard/")
