from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User
# Create your views here.
def publicProfile(request,u):
    context = {}
    print(u)
    obj = User.objects.filter(username=u)
    obj = obj.first()
    print(obj)
    context['obj'] = obj
    return render(request,'users/publicProfile.html',context)


def newMessage(request, m):
    Message.objects.create(author=request.user,content=m)
    return redirect('chat')
def chat(request):
    qs = Message.objects.order_by('id')[:100]
    context = {'qs':qs}
    return render(request,'users/chat.html',context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your Account has been created! You can now login!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html',{'form':form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile.html', context)
