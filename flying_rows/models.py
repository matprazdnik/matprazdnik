from django.db import models
from main_app.models import Participant

class ParticipantUpdateTime(models.Model):
    participant = models.ForeignKey(Participant);
    last_update_time = models.IntegerField();

    def __str__(self):
        return str(self.participant) + "; time: " + str(self.last_update_time)