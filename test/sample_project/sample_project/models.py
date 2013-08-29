from django.db import models

class Event(models.Model):
  name = models.CharField(default="Some Event", max_length=64)
  event_date = models.DateTimeField()

  def __unicode__(self):
    return self.name