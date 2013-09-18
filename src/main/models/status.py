from django.db import models

class ClassifiedStatus(models.Model):
	name = models.CharField(max_length = 200)

	class Meta:
		verbose_name_plural = 'Classifieds Status'
		app_label = "main"
		db_table = "main_classifieds_status"

	def __unicode__(self):
		return self.name
