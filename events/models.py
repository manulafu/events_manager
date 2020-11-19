from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Event(models.Model):
	title = models.CharField(max_length=250, unique_for_date='date')
	description = models.TextField(max_length=300)
	image = models.ImageField(upload_to='events_images')
	date = models.DateField()
	location = models.CharField(max_length=100)
	allowed_attendees = models.IntegerField()
	attendees = models.ManyToManyField(User, related_name='atendees', blank=True, default=None)
	waitlist = models.IntegerField()
	startTime = models.TimeField()
	endTime = models.TimeField()

	class Meta:
		ordering = ('date',)
		unique_together = ['title', 'date']

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('events:event_detail', args=[str(self.id)])

	def available(self):
		attendees = self.attendees.count()
		allowed = self.allowed_attendees
		if attendees < allowed:
			return True
		else:
			return False

	def get_available_spots(self):
		return self.allowed_attendees - self.attendees.count()

@receiver(post_delete, sender=Event)
def submission_delete(sender, instance, **kwargs):
	instance.image.delete(False)
