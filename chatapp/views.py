from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Room, Message

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(username=username)
        if not user:
            user = User.objects.create(username=username, email=email, password=password)
            login(request, user)
            return redirect('home')
        else:
            login(request, user[0])
            return redirect('home')
    else:
        pass
    return render(request, 'registration/signup.html')

@login_required(login_url="/login")
def home(request):
    users = User.objects.all()
    if request.method == 'POST':
        reci_id = request.POST.get("reci")
        reci = User.objects.get(id=reci_id)
        print(reci.id)
        room = Room.objects.filter(users=request.user).filter(users=reci)

        if not room:
            room = Room.objects.create(room_name=str(reci.username+request.user.username))
            room.users.add(reci, request.user)
        else:
            room = room[0]
        
        return redirect(f'room/{room.id}')
    
    current_user = request.user
    other_users = User.objects.exclude(id=current_user.id)
    chat_data = []

    for user in other_users:
        # Get the room shared by current_user and user
        room = Room.objects.filter(users=current_user).filter(users=user).first()
        if room:
            last_msg = Message.objects.filter(room=room).last()
        else:
            last_msg = None
        chat_data.append({
            'user': user,
            'last_message': last_msg.message if last_msg else '',
        })
    
    return render(request, 'home.html', context={'chat_data': chat_data})
def room(request, room_id):
    message = Message.objects.filter(room_id=room_id)
    room = Room.objects.filter(id=room_id)[0]
    other_users = room.users.exclude(id=request.user.id).first().username
    return render(request, 'room.html', context={'messages': message, 'room': room, 'recipient': other_users})

def defs(request):
    return render(request, 'def.html')

# Create your views here.
