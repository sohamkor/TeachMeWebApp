from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from .models import Learner, Coach

# The index page for the web-app
def index(request):
    context = {}
    
    if not request.user.is_authenticated():
        return render(request, 'teachingMainApp/index.html', context)

    return HttpResponseRedirect('/home')

def authenticateUser(request):
    if request.POST:
        username = str(request.POST.get("usernameBox", "None"))
        password = str(request.POST.get("passwordBox", "None"))
        print("The username is", username)
        print("The password is", password)

        # Authenticate the user based on the credentials he/she entered
        mainUser = authenticate(username=username, password=password)

        if mainUser is not None:
            login(request, mainUser)
            return HttpResponseRedirect('/home')
        else:
            context = {}
            return render(request, 'teachingMainApp/incorrectCredentials.html', context)
    else:
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/home')

def homePage(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    username = request.user.username
    learnerList = Learner.objects.filter(user__username=request.user.username)
    currentUser = learnerList[0] # Got current user's Learner object

    usersSpecificVersionNumber = currentUser.versionOfSite
    renderDirectory = 'teachingMainApp/v' + usersSpecificVersionNumber + '/home.html'

    # Start setting up the context
    context = {}
    context['username'] = username

    return render(request, renderDirectory, context)

def subjectsPage(request):
    context = {}
    
    if not request.user.is_authenticated():
        return render(request, 'teachingMainApp/subjectsPageWoLogin.html', context)

    learnerList = Learner.objects.filter(user__username=request.user.username)
    currentUser = learnerList[0] # Got current user's Learner object

    usersSpecificVersionNumber = currentUser.versionOfSite
    renderDirectory = 'teachingMainApp/v' + usersSpecificVersionNumber + '/subjects.html'

    return render(request, renderDirectory, context)

def myClassesPage(request):
    context = {}
    
    if not request.user.is_authenticated():
        return render(request, 'teachingMainApp/loginRequired.html', context)
    
    learnerList = Learner.objects.filter(user__username=request.user.username)
    currentUser = learnerList[0] # Got current user's Learner object

    usersSpecificVersionNumber = currentUser.versionOfSite
    renderDirectory = 'teachingMainApp/v' + usersSpecificVersionNumber + '/myClasses.html'

    username = request.user.username

    currentlyCoaching = Coach.objects.filter(theUserWhoIsTheCoach=currentUser)
    currentlyBeingCoachedBy = Coach.objects.filter(theUserToCoach=currentUser)

    context['username'] = username
    context['currentlyCoaching'] = currentlyCoaching
    context['currentlyBeingCoachedBy'] = currentlyBeingCoachedBy
    
    return render(request, renderDirectory, context)

def aboutUsPage(request):
    context = {}
    if not request.user.is_authenticated():
        return render(request, 'teachingMainApp/aboutUs.html', context)

    learnerList = Learner.objects.filter(user__username=request.user.username)
    currentUser = learnerList[0] # Got current user's Learner object

    usersSpecificVersionNumber = currentUser.versionOfSite
    renderDirectory = 'teachingMainApp/v' + usersSpecificVersionNumber + '/aboutUs.html'

    return render(request, renderDirectory, context)
    

def logOut(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    
    logout(request)
    return HttpResponseRedirect('/')
