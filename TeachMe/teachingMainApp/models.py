from django.db import models
from django.contrib.auth.models import User

class Learner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)

    # Also keeping track of points (which could be implemented later on)
    pointsEarned = models.IntegerField(default=0)

    # Set up the default version for each user, which primarily begins at v1.0.0
    # but in a production enviroment, would be obtained from a general setttings
    # file that is kept up to date
    versionOfSite = models.CharField(max_length=40, default="1.0.0")

    def __str__(self):
        return self.user.username

class Coach(models.Model):
    theUserToCoach = models.ForeignKey(Learner, related_name='userToCoach')

    theUserWhoIsTheCoach = models.ForeignKey(Learner, related_name='userWhoIsTheCoach')

    def __str__(self):
        return self.theUserWhoIsTheCoach.user.username + " is now coaching " + self.theUserToCoach.user.username
