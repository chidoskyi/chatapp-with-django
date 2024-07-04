from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from userauths.models import User,Profiles
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from .models import Messages,Message,Room,Topic
from chatapp.forms import RoomForm
from django.contrib import messages


# Create your views here.

@login_required
def index(request):
    user = request.user
    users = User.objects.all()
    messages = Messages.get_message(user=request.user)
    active_direct = None
    directs = None
    # profile = get_object_or_404(Profile, user=user)

    if messages:
        message = messages[0]
        active_direct = message['user'].username
        directs = Messages.objects.filter(user=request.user, recipient=message['user'])
        directs.update(is_read=True)

        for message in messages:
            if message['user'].username == active_direct:
                message['unread'] = 0
    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
        'user': user,
        'users': users,
    }
    
    return render(request, "index2.html", context)


@login_required
def directs(request, username):
    user = request.user
    messages = Messages.get_message(user=user)
    active_direct = username
    directs = Messages.objects.filter(user=user, recipient__username=username)
    directs.update(is_read=True)

    for message in messages:
        if message['user'].username == username:
            message['unread'] = 0
    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
    }
    
    return render(request, "index.html", context)


def sendDirect(request):
    if request.method == "POST":
        from_user = request.user
        to_user_username = request.POST['to_user']
        body = request.POST['body']
        
        to_user = User.objects.get(username=to_user_username)
        Messages.sender_message(from_user, to_user, body)
        success = "Message Sent"
        return HttpResponse(success)
   
def deleteDirect(request, pk):
    message = Messages.objects.get(id=pk)
    message.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def UserSearch(request):
    query = request.GET.get('q')
    context = {}
    if query:
        users = User.objects.filter(Q(username__icontains=query))
        profiles = Profiles.objects.filter(Q(full_name=query))
        
        context = {
            'query': query,
            'users': users,
            'profiles': profiles,
        }
    
    return render(request, "search.html", context)

from django.views.decorators.csrf import csrf_exempt
@login_required
@csrf_exempt
def edit_message(request, message_id):
    print('Edit message view called')
    print('Request method:', request.method)
    print('Message ID:', message_id)
    
    if request.method == 'POST':
        body = request.POST.get('body')
        print('Message body:', body)
        
        message = get_object_or_404(Messages, id=message_id)
        print('Message object:', message)

        if request.user == message.sender:
            print('User is authorized to edit the message')
            message.body = body
            message.save()
            return JsonResponse({'status': 'success'})
        else:
            print('User is not authorized to edit the message')
            return JsonResponse({'status': 'error', 'message': 'Not authorized to edit this message'})

    print('Invalid request method')
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def createRoom(request):
    topics = Topic.objects.all
    if request.method == "POST":
        form = RoomForm(request.POST,request.FILES)
        topicName = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topicName)
        
        room = Room.objects.create(
            host = request.user,
            roomname = request.POST.get('roomname'),
            description = request.POST.get('description'),
            image = request.FILES.get('image'),
            topic = topic
        )
        room.members.add(request.user.id)
        return redirect("chat-room", pk=room.id)
    else:
        form = RoomForm()
        
    context = {
        "form":form,
        "topics":topics,
        "btn_val":"Create",
    }
    
    return render(request, "create-room.html", context)


def chat_list(request):
    user = request.user
    rooms = Room.objects.all()
    
    context = {
        "user":user,
        "rooms":rooms,
    }
    
    return render(request, "chat-rooms.html", context)

@login_required
def RoomView(request, pk):
    user = request.user
    room = Room.objects.get(id=pk)
    
    if not room:
        return redirect('index')
    roomMessages = room.message_set.all()[:20]
    all_users = User.objects.all()
    
    q = request.GET.get("q").strip() if request.GET.get('q') != None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(description__icontains=q)|
        Q(roomname__icontains=q)
    )
    
    roomsCount = rooms.count()
    rooms = rooms[:6]
    topics = Topic.objects.all()
    topicsCount = topics.count()
    topics = topics[:5]
    
    context = {
        "room":room,
        "topics":topics,
        "room_message":roomMessages,
        "user":user,
        "all_users":all_users,
        "rooms":rooms,
        "room_count":roomsCount,
        "topics_count":topicsCount,
    }
    
    return render(request, "chat-room.html", context)


@login_required
def join_room(request, pk):
    profile = Profiles.objects.get(user=request.user)
    room = Room.objects.get(id=pk)
    
    if not room:
        return redirect('index')
    
    if request.user.is_authenticated:
        room.members.add(request.user)
        messages.success(request, f"You joined the {room}'s room")
    else:
        messages.warning(request, "You need to login before you can join a room")
        
    return redirect('chat-room', pk=pk)
    
@login_required
def leave_room(request, pk):
    # profile = Profiles.objects.get(user=request.user)
    room = Room.objects.get(id=pk)
    
    if not room:
        return redirect('index')
    
    if request.user.is_authenticated:
        room.members.remove(request.user)
        messages.success(request, f"You Left the {room}'s room")
    else:
        messages.warning(request, "You need to login before you can join a room")
        
    return redirect('index')


@login_required    
def sendMsg(request, pk):
    if request.method == "POST":
        user = request.user
        room = Room.objects.get(id=pk)
        
        body = request.POST.get('body')
        new_chat = Message.objects.create(user=user, room=room, body=body)
        success = "Message Sent"
        return HttpResponse(success)
      
        