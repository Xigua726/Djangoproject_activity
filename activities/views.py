from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from activities.forms import ActivityForm
from activities.models import Activity


# Create your views here.

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
    return render(request,"login.html")

def user_logout(request):
    logout(request)
    return redirect("index")

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request,"register.html",{"form":form})

def index(request):
    q = request.GET.get("q", "").strip()
    activities = Activity.objects.all()
    if q:
        activities = activities.filter(title__icontains=q)
    return render(request,"activity_list.html",
                  {"activities":activities, "q":q})

@login_required
def add(request):
    if request.method == "POST":
        form = ActivityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = ActivityForm()
    return render(request, "activity_form.html", {"form":form})

@login_required
def edit(request,pk):
    activity = get_object_or_404(Activity,pk=pk)

    if request.method == "POST":
        form = ActivityForm(request.POST,instance=activity)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = ActivityForm(instance=activity)
    return render(request ,"activity_form.html",{"form":form})

@login_required
def delete(request,pk):
    activity = get_object_or_404(Activity,pk=pk)

    if request.method == "POST":
        activity.delete()
        return redirect("index")

    return render(request, "activity_confirm_delete.html", {"activity":activity})

