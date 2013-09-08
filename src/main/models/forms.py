from django.forms import ModelForm
from main.models.classifieds import Classified

class AddClassifiedForm(ModelForm):
	class Meta:
		model = Classified
		fields = [
			'title', 'content', 'category', 'status', 'type', 
			'currency', 'expires', 'price', 'phone', 'google_map',
			'image_1', 'image_2', 'image_3', 
		];

