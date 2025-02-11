from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.

class Event(models.Model):
	name = models.CharField(max_length = 250)
	description = models.TextField()
	date = models.DateField()
	time = models.DateTimeField(auto_now_add = True)
	location = models.CharField(max_length = 250)
	category = models.ForeignKey("Category", on_delete = models.CASCADE, related_name = "event")

	def __str__(self):
		return self.name

	def clean(self):
		if self.date is not None and self.date < timezone.now().date():
			raise ValidationError("Event date can not be in the past.")

	def save(self, *args, **kwargs):
		self.clean()
		super().save(*args, **kwargs)


class Participant(models.Model):
	name = models.CharField(max_length = 250)
	email = models.EmailField(unique = True)
	event = models.ManyToManyField(Event, related_name = 'participant')

	def __str__(self):
		return self.name


class Category(models.Model):
	name = models.CharField(max_length = 250)
	description = models.TextField()

	def __str__(self):
		return self.name