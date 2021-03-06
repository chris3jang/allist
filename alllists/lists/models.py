from django.db import models

# Create your models here.


'''
class List(models.Model):
	list_title = models.CharField(max_length=255, blank=True)
	#completed = models.BooleanField(blank=False)
	items = models.ManyToManyField(Item, blank=True, related_name='', symmetrical=False)
	order_number = models.PositiveIntegerField(default=0)

	def __unicode__(self):
		return self.list_title
'''

class Item(models.Model):
	item_title = models.CharField(max_length=255, blank=True)
	#completed = models.BooleanField(blank=False)
	children = models.ManyToManyField("self", blank=True, related_name='parent', symmetrical=False)
	order_number = models.PositiveIntegerField(default=0)

	def __unicode__(self):
		return self.item_title

