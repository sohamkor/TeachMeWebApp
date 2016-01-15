from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User

from .models import Learner, Coach
from .tools_queue import Queue

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

def signUp(request):
    return render(request, 'teachingMainApp/signUp.html', {})

def processSignUp(request):
    firstname = request.POST.get("firstnameBox", "")
    lastname = request.POST.get("lastnameBox", "")
    username = request.POST.get("usernameBox", "")
    password = request.POST.get("passwordBox", "")

    if firstname == "" or lastname == "" or username == "" or password == "":
        return HttpResponseRedirect('/signUp')

    user = User.objects.create_user(username, password=password)
    user.first_name = firstname
    user.last_name = lastname
    user.save()

    learner = Learner(user=user)
    learner.save()

    return render(request, 'teachingMainApp/accountCreated.html', context={'firstname': firstname})


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

def processStudent(request):
    context = {}

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    usernameOfCoach = request.POST.get("usernameToBeCoachedBy", "")
    if usernameOfCoach == "":
        return HttpResponseRedirect('/')

    myUserList = Learner.objects.filter(user__username=request.user.username)
    myUser = myUserList[0]

    usersSpecificVersionNumber = myUser.versionOfSite
    renderDirectory = 'teachingMainApp/v' + usersSpecificVersionNumber + '/userCantBeFound.html'

    learnerList = Learner.objects.filter(user__username=usernameOfCoach)
    if len(learnerList) == 0:
        return render(request, renderDirectory, context={'coachUser': usernameOfCoach})
    coachObj = learnerList[0]    

    newCoachRelation = Coach(theUserToCoach=myUser, theUserWhoIsTheCoach=coachObj)
    newCoachRelation.save()

    renderDirectory = 'teachingMainApp/v' + usersSpecificVersionNumber + '/addedStudent.html'

    return render(request, renderDirectory, context={'myUsername': request.user.username, 'coachUsername': coachObj.user.username})

def rolloutAlgorithmPage(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    learnerList = Learner.objects.filter(user__username=request.user.username)
    currentUser = learnerList[0] # Got current user's Learner object

    usersSpecificVersionNumber = currentUser.versionOfSite
    renderDirectory = 'teachingMainApp/v' + usersSpecificVersionNumber + '/rolloutAlgorithm.html'

    context= {}

    return render(request, renderDirectory, context)

def totalInfectionPage(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    learnerList = Learner.objects.filter(user__username=request.user.username)
    currentUser = learnerList[0] # Got current user's Learner object

    usersSpecificVersionNumber = currentUser.versionOfSite
    renderDirectory = 'teachingMainApp/v' + usersSpecificVersionNumber + '/totalInfection.html'

    context= {}

    return render(request, renderDirectory, context)

def processTI(request):
    # In a production environment, this method could be made much more efficient
    # using a threaded/background process such as one that could be set up using
    # Celery. As the database gets larger and larger, this would allow the changes
    # to be made in the background while the user can still continue to browse the
    # site.
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    newVersionOfSite = request.GET.get("version", None)
    if "v" in newVersionOfSite:
        newVersionOfSite = newVersionOfSite[1:]

    # Set up the context
    context = {}
    listOfIdsModified = []

    learnerList = Learner.objects.filter(user__username=request.user.username)
    currentUser = learnerList[0] # Got current user's Learner object

    listOfIdsModified.append(currentUser.user.username)

    # Using a breadth-first search in order to analyze the user's connected
    # component and the other users that will also become infected

    infectionQueue = Queue()
    infectionQueue.enqueue(currentUser)

    # First make the changes for the user passed in as a parameter
    currentUser.versionOfSite = newVersionOfSite
    currentUser.save()

    # Now handle all of the users who are coaching the given user passed in as a parameter
    while infectionQueue.size() > 0:
        currUserNode = infectionQueue.dequeue()

        listOfPeopleCoachingMe = Coach.objects.filter(theUserToCoach__user__username=currUserNode.user.username)

        for eachIndividualNode in listOfPeopleCoachingMe:
            userObj = eachIndividualNode.theUserWhoIsTheCoach

            if not userObj.versionOfSite == newVersionOfSite:
                userObj.versionOfSite = newVersionOfSite
                userObj.save()

                listOfIdsModified.append(userObj.user.username)
                
                infectionQueue.enqueue(userObj)

    # The above algorithm will need to be executed again with the bottom part of the connected graph (users that userObjToStartInfectionFrom is coaching) and then re-add it to the queue
    infectionQueue.enqueue(currentUser)

    # The following loop will take care of all the users that the current user is coaching
    while infectionQueue.size() > 0:
        currUserNode = infectionQueue.dequeue()
        listOfPeopleImCoaching = Coach.objects.filter(theUserWhoIsTheCoach__user__username=currUserNode.user.username)

        for eachIndividualNode in listOfPeopleImCoaching:
            userObj = eachIndividualNode.theUserToCoach

            if not userObj.versionOfSite == newVersionOfSite:
                userObj.versionOfSite = newVersionOfSite
                userObj.save()

                listOfIdsModified.append(userObj.user.username)
                
                infectionQueue.enqueue(userObj)

    print("The infection algorithm finished executing!")

    request.session['listOfIdsUpgraded'] = listOfIdsModified

    return HttpResponseRedirect('/tiSuccess')

def totalInfectionSucceeded(request):
    if not request.user.is_authenticated() or request.session.get('listOfIdsUpgraded', '') == '':
        return HttpResponseRedirect('/')
    
    # Get appropriate version information again (since this was updated in the algorithm above)
    learnerList = Learner.objects.filter(user__username=request.user.username)
    currentUser = learnerList[0] # Got current user's Learner object

    usersSpecificVersionNumber = currentUser.versionOfSite
    renderDirectory = 'teachingMainApp/v' + usersSpecificVersionNumber + '/totalInfectionSuccess.html'

    # Set up the context
    context = {}
    context['listOfIdsUpgraded'] = request.session.get('listOfIdsUpgraded', '')

    request.session['listOfIdsUpgraded'] = ''

    return render(request, renderDirectory, context)

def limitedInfectionPage(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    learnerList = Learner.objects.filter(user__username=request.user.username)
    currentUser = learnerList[0] # Got current user's Learner object

    usersSpecificVersionNumber = currentUser.versionOfSite
    renderDirectory = 'teachingMainApp/v' + usersSpecificVersionNumber + '/limitedInfection.html'

    context= {}

    return render(request, renderDirectory, context)

def processLI(request):
    # In a production environment, this method could be made much more efficient
    # using a threaded/background process such as one that could be set up using
    # Celery. As the database gets larger and larger, this would allow the changes
    # to be made in the background while the user can still continue to browse the
    # site.
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    newVersionOfSite = request.GET.get("version", None)
    numOfUsersToInfect = eval(request.GET.get("numUsers", None))
    if "v" in newVersionOfSite:
        newVersionOfSite = newVersionOfSite[1:]

    # Set up the context
    context = {}

    # Initialize variables that will keep track of the amount of users changes
    userChangesNeededToBeMade = 1
    moveOnToSecond = False

    learnerList = Learner.objects.filter(user__username=request.user.username)
    currentUser = learnerList[0] # Got current user's Learner object

    # Using a breadth-first search in order to analyze the user's connected
    # component and the other users that will also become infected

    infectionQueue = Queue()
    infectionQueue.enqueue(currentUser)

    # This time, starting to analyze with the people the user specified is
    # coaching (and if the changes to the number of users needed to be made
    # exceeds that of the target number of users to infect, then there is
    # no need to continue processing the users who will be coaching the
    # current user), even though this will give rise to a situation that is
    # not ideal (i.e: A coach will have a bunch of students who will
    # themselves be on a newer version while the coach him/herself will be
    # on an older version), it will be a better scenario than having a
    # fraction of users that a coach is teaching to be on the newer one
    # while the other fraction to be on the older one, which marks a more
    # serious divide.

    # The following loop will take care of all the users that the current user is coaching
    while infectionQueue.size() > 0:
        currUserNode = infectionQueue.dequeue()

        listOfPeopleImCoaching = Coach.objects.filter(theUserWhoIsTheCoach__user__username=currUserNode.user.username)

        for eachIndividualNode in listOfPeopleImCoaching:
            userObj = eachIndividualNode.theUserToCoach

            if not userObj.versionOfSite == newVersionOfSite:
                userChangesNeededToBeMade += 1                    
                infectionQueue.enqueue(userObj)

    # The above algorithm will need to be executed again with the bottom part of the connected graph (users that userObjToStartInfectionFrom is coaching) and then re-add it to the queue
    infectionQueue.enqueue(currentUser)

    if userChangesNeededToBeMade < numOfUsersToInfect:
        moveOnToSecond = True # This ensures that we can keep track of the fact that we are able to go on to the second part of the algorithm
        
        while infectionQueue.size() > 0:
            currUserNode = infectionQueue.dequeue()

            listOfPeopleCoachingMe = Coach.objects.filter(theUserToCoach__user__username=currUserNode.user.username)

            for eachIndividualNode in listOfPeopleCoachingMe:
                userObj = eachIndividualNode.theUserWhoIsTheCoach

                if not userObj.versionOfSite == newVersionOfSite:
                    userChangesNeededToBeMade += 1
                    infectionQueue.enqueue(userObj)

    context['numOfChangesToMake'] = userChangesNeededToBeMade

    # Save some needed values for the finishLI method
    request.session['versionToChange'] = newVersionOfSite
    request.session['moveOnToSecond'] = moveOnToSecond

    usersSpecificVersionNumber = currentUser.versionOfSite
    renderDirectory = 'teachingMainApp/v' + usersSpecificVersionNumber + '/confirmLIChanges.html'

    return render(request, renderDirectory, context)

def finishLI(request):
    # In a production environment, this method could be made much more efficient
    # using a threaded/background process such as one that could be set up using
    # Celery. As the database gets larger and larger, this would allow the changes
    # to be made in the background while the user can still continue to browse the
    # site.
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    newVersionOfSite = request.session.get("versionToChange", None)
    if "v" in newVersionOfSite:
        newVersionOfSite = newVersionOfSite[1:]

    # Set up the context
    context = {}
    listOfIdsModified = []

    # Initialize variables that will keep track of the amount of users changes
    moveOnToSecond = request.session.get('moveOnToSecond', False)

    learnerList = Learner.objects.filter(user__username=request.user.username)
    currentUser = learnerList[0] # Got current user's Learner object

    listOfIdsModified.append(currentUser.user.username)

    # Using a breadth-first search in order to analyze the user's connected
    # component and the other users that will also become infected

    infectionQueue = Queue()
    infectionQueue.enqueue(currentUser)

    # First make the changes for the user passed in as a parameter
    currentUser.versionOfSite = newVersionOfSite
    currentUser.save()

    # This time, starting to analyze with the people the user specified is
    # coaching (and if the changes to the number of users needed to be made
    # exceeds that of the target number of users to infect, then there is
    # no need to continue processing the users who will be coaching the
    # current user), even though this will give rise to a situation that is
    # not ideal (i.e: A coach will have a bunch of students who will
    # themselves be on a newer version while the coach him/herself will be
    # on an older version), it will be a better scenario than having a
    # fraction of users that a coach is teaching to be on the newer one
    # while the other fraction to be on the older one, which marks a more
    # serious divide.

    # The following loop will take care of all the users that the current user is coaching
    while infectionQueue.size() > 0:
        currUserNode = infectionQueue.dequeue()

        listOfPeopleImCoaching = Coach.objects.filter(theUserWhoIsTheCoach__user__username=currUserNode.user.username)
        
        for eachIndividualNode in listOfPeopleImCoaching:
            userObj = eachIndividualNode.theUserToCoach

            if not userObj.versionOfSite == newVersionOfSite:
                userObj.versionOfSite = newVersionOfSite
                userObj.save()

                listOfIdsModified.append(userObj.user.username)
                infectionQueue.enqueue(userObj)

    # The above algorithm will need to be executed again with the bottom part of the connected graph (users that userObjToStartInfectionFrom is coaching) and then re-add it to the queue
    infectionQueue.enqueue(currentUser)

    if moveOnToSecond:        
        while infectionQueue.size() > 0:
            currUserNode = infectionQueue.dequeue()
            listOfPeopleCoachingMe = Coach.objects.filter(theUserToCoach__user__username=currUserNode.user.username)

            for eachIndividualNode in listOfPeopleCoachingMe:
                userObj = eachIndividualNode.theUserWhoIsTheCoach

                if not userObj.versionOfSite == newVersionOfSite:
                    userObj.versionOfSite = newVersionOfSite
                    userObj.save()

                    listOfIdsModified.append(userObj.user.username)
                    infectionQueue.enqueue(userObj)

    print("The limited infection algorithm finished successfully!")

    request.session['listOfIdsUpgraded'] = listOfIdsModified

    return HttpResponseRedirect('/liSuccess')

def limitedInfectionSucceeded(request):
    if not request.user.is_authenticated() or request.session.get('listOfIdsUpgraded', '') == '':
        return HttpResponseRedirect('/')
    
    # Get appropriate version information again (since this was updated in the algorithm above)
    learnerList = Learner.objects.filter(user__username=request.user.username)
    currentUser = learnerList[0] # Got current user's Learner object

    usersSpecificVersionNumber = currentUser.versionOfSite
    renderDirectory = 'teachingMainApp/v' + usersSpecificVersionNumber + '/limitedInfectionSuccess.html'

    # Set up the context
    context = {}
    context['listOfIdsUpgraded'] = request.session.get('listOfIdsUpgraded', '')

    request.session['listOfIdsUpgraded'] = ''

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
