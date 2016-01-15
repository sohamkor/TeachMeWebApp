import site_general_settings
import datetime

class User(object):
    def __init__(self, firstName, lastName, userId, emailAddress):
        # Public Information
        self.firstName = firstName
        self.lastName = lastName
        self.userId = userId

        self.dateJoined = datetime.datetime.now()

        # Point system
        self.pointsEarned = 0 # Initially starts out with 0

        # Private information
        self.__emailAddress = emailAddress

        self.__versionOfSite = site_general_settings.getLatestStableVersion()
        self.__color = "white" # For use in the infection (in the breadth-first search)

        self.__isCoaching = {}
        self.__isBeingCoachedBy = {}

    def addUserToCoach(self, userObj, modifyOther=True):
        idOfUser = userObj.getUserId()

        if idOfUser in self.__isCoaching.keys():
            print(idOfUser, "already seems to be coached by", self.userId)
        else:
            self.__isCoaching[idOfUser] = userObj
            if modifyOther:
                userObj.beCoachedByUser(self, False)

    def beCoachedByUser(self, userObj, modifyOther=True):
        idOfUser = userObj.getUserId()

        if idOfUser in self.__isBeingCoachedBy.keys():
            print(idOfUser, "already seems to be coaching", self.userId)
        else:
            self.__isBeingCoachedBy[idOfUser] = userObj
            if modifyOther:
                userObj.addUserToCoach(self, False)

    def getUserId(self):
        return self.userId
 
    def getListOfPeopleImCoaching(self):
        return list(self.__isCoaching.items())

    def getListOfPeopleCoachingMe(self):
        return list(self.__isBeingCoachedBy.items())

    def getColor(self):
        return self.__color

    def setColor(self, colorToChange):
        self.__color = colorToChange

    def getCurrentVersionOfSiteUserIsUsing(self):
        return self.__versionOfSite

    def versionStringIsAlright(self, version):
        for index in range(1, len(version), 1):
            if version[index].isdigit():
                continue
            elif version[index] == '.':
                continue
            else:
                return False

        return True

    def setNewCurrentVersionOfSite(self, newVersionOfSite):
        newCheckedVersion = newVersionOfSite
        if "v" in newCheckedVersion:
            newCheckedVersion = newCheckedVersion[1:]
        if not self.versionStringIsAlright(newCheckedVersion):
            print("Invalid version specified. Please check to see that there are no invalid characters.")
            return 
        self.__versionOfSite = newCheckedVersion

    def printSiteReportOfUsersImCoaching(self):
        listOfPeopleImCoaching = self.getListOfPeopleImCoaching()

        if len(listOfPeopleImCoaching) == 0:
            print("You are not coaching anyone.")
            return

        for eachPersonTuple in listOfPeopleImCoaching:
            userName = eachPersonTuple[0]
            userObj = eachPersonTuple[1]

            usersCurrentVersion = userObj.getCurrentVersionOfSiteUserIsUsing()
            if "v" in usersCurrentVersion:
                indexOfV = usersCurrentVersion.find("v")
                usersCurrentVersion = usersCurrentVersion[:indexOfV] + usersCurrentVersion[indexOfV+1:]

            print(userName, "is using v" + usersCurrentVersion + " of the site.")

    def printSiteReportOfUsersImCoachedBy(self):
        listOfPeopleImCoachedBy = self.getListOfPeopleCoachingMe()

        if len(listOfPeopleImCoachedBy) == 0:
            print("You are not coached by anyone")
            return

        for eachPersonTuple in listOfPeopleImCoachedBy:
            userName = eachPersonTuple[0]
            userObj = eachPersonTuple[1]

            usersCurrentVersion = userObj.getCurrentVersionOfSiteUserIsUsing()
            if "v" in usersCurrentVersion:
                indexOfV = usersCurrentVersion.find("v")
                usersCurrentVersion = usersCurrentVersion[:indexOfV] + usersCurrentVersion[indexOfV+1:]

            print(userName, "is using v" + usersCurrentVersion + " of the site.")
