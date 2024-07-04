from userauths.models import User,Profiles


def default(request):
    users = User.objects.all()
    
    
    
    return {
        'users': users,
    }
    