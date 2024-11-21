from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Message,Profile
from predict.models import Game
from django.contrib.auth.models import User
from .models import Message,Profile

import stripe
from datetime import datetime 

@login_required  # new
def shop(request):
    context={}
    ''' try:
        # Retrieve the subscription & product
        stripe_customer = StripeCustomer.objects.get(user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(stripe_customer.stripeSubscriptionId)
        product = stripe.Product.retrieve(subscription.plan.product)

        # Feel free to fetch any additional data from 'subscription' or 'product'
        # https://stripe.com/docs/api/subscriptions/object
        # https://stripe.com/docs/api/products/object

        context['subscription']=subscription
        context['product']= product
        context['active'] = True
        context['start'] = datetime.fromtimestamp(subscription.current_period_start)
        context['end'] = datetime.fromtimestamp(subscription.current_period_end)



    except StripeCustomer.DoesNotExist:
        context['active'] = False'''
    return render(request, 'users/shop.html',context)



#view other users public profiles, with there predictions
def publicProfile(request,u):
    context = {}
    print(u)
    obj = User.objects.filter(username=u)
    obj = obj.first()
    print(obj)
    context['obj'] = obj

    games = Game.objects.filter(author=obj).order_by('-date_posted')[:100]

    context['games'] = games

    return render(request,'users/publicProfile.html',context)

#Create a new message objeect
def newMessage(request, m):
    Message.objects.create(author=request.user,content=m)
    return redirect('stats-view')

#render cummunity view, no longer really used
#merged with profile view on live site
def community(request):
    qs = Message.objects.order_by('id')[:100]
    context = {'qs':qs}
    profiles = Profile.objects.order_by('id')
    context['profiles'] = profiles


    return render(request,'users/community.html',context)
    
#register a user, recieve form or render page
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
#User profile page, can update user settings, and export data.
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
