from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import Group, User,AnonymousUser
from .forms import CustomUserForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from mom.models import MomModel
from customer.models import Customer
from django.urls import reverse
from django.contrib import messages

def Register(request):
    if request.user.is_authenticated != True:
        form = CustomUserForm()
        if request.method == "POST":
            form = CustomUserForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                mom_group = Group.objects.get(name="moms")
                user.groups.add(mom_group)
                user.is_staff = True
                user.is_superuser = True
                user.save()

                MomModel.objects.create(user=user, email=user.email)
                messages.success(request,"your profile is created successfully")
                return redirect('moms:login')
        context = {"form": form, "formname": "moms"}
        return render(request, 'register.html', context)

    else:
        return redirect('moms:profile')


def CustomerRegister(request):
    if request.user.is_authenticated != True:
        form = CustomUserForm()
        if request.method == "POST":
            form = CustomUserForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                customer_group = Group.objects.get(name="customer")
                user.groups.add(customer_group)
                user.is_staff = False
                user.is_superuser = False
                user.save()
                Customer.objects.create(user=user, email=user.email)
                messages.success(request,"your profile is created successfully")

                return redirect('moms:login')

        context = {"form": form, "formname": "customer"}
        return render(request, 'register.html', context)
    
    else:
        return redirect('customer:customer')


def LoginPage(request):

    if request.user.is_authenticated !=True:
        if request.method == 'POST':
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                name = User.objects.get(id=request.user.id)
                for groupfetch in name.groups.all():
                    if (str(groupfetch) == "moms" or str(groupfetch) == "customer" or str(groupfetch) == "delivery"):
                        groupname = groupfetch
                        
                print("group name", groupname)
                if str(groupname) == "moms":
                    messages.success(request,f"you are login as {{user}}")
                    return redirect('moms:profile')
                elif str(groupname) == "customer":
                    messages.success(request,f"you are login as {{user}}")
                    return redirect('customer:customer')
                    # return redirect('customer:customer')
            else:
                return HttpResponse('cannot login')
        context = {}
        return render(request, 'login.html', context)
    else:
        user = User.objects.get(id = request.user.id)
        for groupfetch in user.groups.all():
            if (str(groupfetch) == "moms" or str(groupfetch) == "customer" or str(groupfetch) == "delivery"):
                groupname = groupfetch            
        print("group name", groupname)
        if str(groupname) == "moms":
            print("redirect home")
            return redirect('moms:profile')
        elif str(groupname) == "customer":
            print("redirect customer")
            return redirect('customer:customer')


def Logout(request):
    
    if isinstance(request.user,AnonymousUser):
        return redirect('moms:login')
    
    elif request.user.is_authenticated == True:        
        logout(request)
        return redirect('moms:login')

    else:
        return HttpResponse('error logout ')
    