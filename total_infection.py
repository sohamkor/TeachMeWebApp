# By Soham Koradia as a project for Khan Academy

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
