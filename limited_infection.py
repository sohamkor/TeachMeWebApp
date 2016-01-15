# By Soham Koradia as a project for Khan Academy

from site_user import User
from tools_queue import Queue

def infectLimitedConnection(userObjToStartInfectionFrom, updatedVersionNum, numOfUsersToInfect):
    # Using a technique similar to how total_infection was implemented, knowing that the infected a specific amount of users won't be plausible depending on how the connected graphs among users look like, in this algorithm, first an analysis will be done of the number of users that can be infected (which will be kept similar if not equal to how many were passed into the argument) while maintaining the principle that consistent versions of the site should be given to the coaches as well as the students that they are teaching, therefore, limited_infection may take quite a bit longer than it's total_infection counterpart. In a production environment, one possible implementation would be that a user can extracted from the whose connected graph can be found to have the correct number of users to be infected, as specified, and as the rollout percentage becomes greater, the users who are still on the older version can then be selected, so that the number of people on the new update remain fairly consistent to how many are wanted at any given point.

    ''' 
    Since the code given here is only used to analyze how many users would need to be changed, if there are a large number of users, then the time complexity would grow greatly, causing the program to take much larger amounts of time, therefore in order to increase the speed of the function, at the expense of lesser flexibility for the user, the part until asking the user for permission to continue may be commented out, so that the changes will be without informing the user, which will also save tons of time for it to execute (in a production environment, this can be done via threading and parallel executions)
        '''

    infectionQueue = Queue()
    infectionQueue.enqueue(userObjToStartInfectionFrom)

    userChangesNeededToBeMade = 1
    moveOnToSecond = False

    newVersionOfSite = updatedVersionNum

    # This time, starting to analyze with the people the user specified is coaching (and if the changes to the number of users needed to be made exceeds that of the target number of users to infect, then there is no need to continue processing the users who will be coaching the current user), even though this will give rise to a situation that is not ideal (i.e: A coach will have a bunch of students who will themselves be on a newer version while the coach him/herself will be on an older version), it will be a better scenario than having a fraction of users that a coach is teaching to be on the newer one while the other fraction to be on the older one, which marks a more serious divide.

    # The following loop will take care of all the users that the current user is coaching
    while infectionQueue.size() > 0:
        currUserNode = infectionQueue.dequeue()

        for eachIndividualNode in currUserNode.getListOfPeopleImCoaching():
            userId = eachIndividualNode[0]
            userObj = eachIndividualNode[1]

            if not userObj.getCurrentVersionOfSiteUserIsUsing == newVersionOfSite:
                userChangesNeededToBeMade += 1
                infectionQueue.enqueue(userObj)

    if userChangesNeededToBeMade < numOfUsersToInfect:
        moveOnToSecond = True # This ensures that we can keep track of the fact that we are able to go on to the second part of the algorithm
        # In this case the users who are coaching the current users can also be accounted for
        infectionQueue.enqueue(userObjToStartInfectionFrom)

        while infectionQueue.size() > 0:
            currUserNode = infectionQueue.dequeue()

            for eachIndividualNode in currUserNode.getListOfPeopleCoachingMe():
                userId = eachIndividualNode[0]
                userObj = eachIndividualNode[1]

                if not userObj.getCurrentVersionOfSiteUserIsUsing == newVersionOfSite:
                    userChangesNeededToBeMade += 1
                    infectionQueue.enqueue(userObj)

    # Prompt the user as to whether or not they want to go forward with infecting the given number of users as calculated using the aboc algorithms

    continueAlgorithm = input("In order to roll this out in a structered way, we have determined that " + str(userChangesNeededToBeMade) + " user(s) need to be infected. This ensures that for the most part classes have students who are uniformly using the same new version. Do you want to make the changes? ")

    if continueAlgorithm.upper() == 'YES' or continueAlgorithm.upper() == 'Y':
        userObjToStartInfectionFrom.setNewCurrentVersionOfSite(newVersionOfSite)
        infectionQueue.enqueue(userObjToStartInfectionFrom)        

        # The following loop will take care of all the users that the current user is coaching
        while infectionQueue.size() > 0:
            currUserNode = infectionQueue.dequeue()

            for eachIndividualNode in currUserNode.getListOfPeopleImCoaching():
                userId = eachIndividualNode[0]
                userObj = eachIndividualNode[1]

                if not userObj.getCurrentVersionOfSiteUserIsUsing == newVersionOfSite:
                    userObj.setNewCurrentVersionOfSite(newVersionOfSite)
                    infectionQueue.enqueue(userObj)

        infectionQueue.enqueue(userObjToStartInfectionFrom)

        if moveOnToSecond:
            # Make the changes
            while infectionQueue.size() > 0:
                currUserNode = infectionQueue.dequeue()

                for eachIndividualNode in currUserNode.getListOfPeopleCoachingMe():
                    userId = eachIndividualNode[0]
                    userObj = eachIndividualNode[1]

                    if not userObj.getCurrentVersionOfSiteUserIsUsing == newVersionOfSite:
                        userObj.setNewCurrentVersionOfSite(newVersionOfSite)
                        infectionQueue.enqueue(userObj)
    
    elif continueAlgorithm.upper() == 'NO' or continueAlgorithm.upper() == 'N':
        print("Aborting due to user's choice.")
        return
    else:
        print("Invalid input recognized. Aborting.")
        return   
 
    print("The limited-infection was successful.") 
