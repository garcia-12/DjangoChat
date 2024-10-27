from Demos.win32ts_logoff_disconnected import username
from django.contrib.messages.context_processors import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import *


# Create your views here.

def home(request):
    return render(request, 'home.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name= room).exists():
        return redirect('/' + room + '/?username=' + username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/' + room + '/?username=' + username)



def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    reply_to_id = request.POST.get('reply_to')  # Récupérer l'ID du message auquel on répond (si présent)

    room = Room.objects.get(id=room_id)

    # Si l'utilisateur répond à un message
    reply_to = None
    if reply_to_id:
        reply_to = Message.objects.get(id=reply_to_id)

    new_message = Message.objects.create(
        value=message,
        user=username,
        room=room,
        reply_to=reply_to  # Associer le message auquel on répond
    )
    new_message.save()
    # new_message = Message.objects.create(value=message, user=username, room=room_id)
    # new_message.save()
    return HttpResponse('Message envoyé avec succès')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details).order_by('date')
    messages_data = []
    for message in messages:
        messages_data.append({
            'id': message.id,
            'user': message.user,
            'value': message.value,
            'date': message.date,
            # 'reply_to': message.reply_to.id if message.reply_to else None  # Assurez-vous que reply_to est correct
            'reply_to': {
                'id': message.reply_to.id if message.reply_to else None,
                'value': message.reply_to.value if message.reply_to else None,}

            if message.reply_to else None  # Assurez-vous que reply_to est un objet et non seulement l'ID
        })

    print("Messages récupérés :", messages_data)  # Débogage

    return JsonResponse({'messages': messages_data})

@csrf_exempt
def delet_messages(request):
    if request.method == 'POST':
        message_id = request.POST['message_id']
        Message.objescts.filter(id=message_id).delete()
        return JsonResponse({'success': True})

@csrf_exempt
def send_message(request): #Pour modify
    if request.method == 'POST':
        message_id = request.POST['reply_to']
        if message_id:
            # Logique pour mettre à jour le message existant
            message = Message.objects.get(id=message_id)
            message.value = request.POST['message']
            message.save()
        else:
            # Logique pour créer un nouveau message
            Message.objects.create()