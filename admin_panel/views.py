from django.shortcuts import render,redirect

from userauths.models import User


# Create your views here.

def block_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_active = False
    user.save()
    return redirect('admin_panel:user_management')

def unblock_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_active = True
    user.save()
    return redirect('admin_panel:user_management')

def admin_dash(request):
    return render(request, 'admin_panel/admin_dash.html')

def user_management(request):
    cus = User.objects.all()
    context = {
        'cus' : cus,
    }
    return render(request, 'admin_panel/user_manage.html',context)