# By Soham Koradia as a project for Khan Academy
'''
In order to use this algorithm, open up a Python terminal (by executing the
command 'python' in bash/command prompt), import this module (import
total_infection), import the User module (from site_user import User), create as
many users as you would like by running for example: bob = User("bob", "cat",
"bcat54", "bcat@meownetworks.com"). Basically this User constructor takes the
format: firstname, lastname, username, emailAddress. After making enough as you
see fit, you can add users to as student/coaches of others by running the
following User methods: beCoachedByUser(userWhoIsTheCoach) and
addUserToCoach(usernameToCoach). For example, here's a way to run that (assuming
sam is an already defined user variable name): sam.beCoachedByUser(bob). Once as
many coach/student relationships are setup, you can call this algorithm on any
given user like this: total_infection.infectConnection(sam, "v1.0.8"), where the
first parameter is the user to start the infection from and the second one is
the version number to roll out to them. After this finishes, check to see that
it worked by calling the printSiteReportOfUsersImCoachedBy() and
printSiteReportOfUsersImCoaching() methods of any User, for example,
bob.printSiteReportOfUsersImCoaching(), which should return the version each
specific user in your connected tree is on. This algorithm was incorporated into
the TeachMe webapp in order to demonstrate it in a real website environment.
Hope you like it!
'''

from site_user import User
from tools_queue import Queue

def infectConnection(userObjToStartInfectionFrom, newVersionOfSite):
    # Using a breadth-first search in order to analyze the user's connected
    # component and the other users that will also become infected

    infectionQueue = Queue()
    infectionQueue.enqueue(userObjToStartInfectionFrom)

    # First make the changes for the user passed in as a parameter
    userObjToStartInfectionFrom.setNewCurrentVersionOfSite(newVersionOfSite)

    # Now handle all of the users who are coaching the given user passed in as a parameter
    while infectionQueue.size() > 0:
        currUserNode = infectionQueue.dequeue()

        for eachIndividualNode in currUserNode.getListOfPeopleCoachingMe():
            userId = eachIndividualNode[0]
            userObj = eachIndividualNode[1]

            if not userObj.getCurrentVersionOfSiteUserIsUsing() == newVersionOfSite:
                userObj.setNewCurrentVersionOfSite(newVersionOfSite)
                infectionQueue.enqueue(userObj)

    # The above algorithm will need to be executed again with the bottom part of the connected graph (users that userObjToStartInfectionFrom is coaching) and then re-add it to the queue
    infectionQueue.enqueue(userObjToStartInfectionFrom)

    # The following loop will take care of all the users that the current user is coaching
    while infectionQueue.size() > 0:
        currUserNode = infectionQueue.dequeue()

        for eachIndividualNode in currUserNode.getListOfPeopleImCoaching():
            userId = eachIndividualNode[0]
            userObj = eachIndividualNode[1]

            if not userObj.getCurrentVersionOfSiteUserIsUsing() == newVersionOfSite:
                userObj.setNewCurrentVersionOfSite(newVersionOfSite)
                infectionQueue.enqueue(userObj)

    print("The total-infection was successful.")
