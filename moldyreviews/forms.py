from django import forms
from .models import Rating
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

class RatingForm(forms.ModelForm):

	STATUS_CHOICES = (('Plan to watch', 'Plan to watch'), ('Watched', 'Watched'))
	RATING_CHOICES = (('',''),(1,1),(2,2),(3,3),(4,4),(5,5))
	movie_status = forms.ChoiceField(choices=STATUS_CHOICES)
	movie_rating = forms.ChoiceField(choices=RATING_CHOICES, required=False)

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		self.mode = kwargs.pop('mode')
		super(RatingForm, self).__init__(*args, **kwargs)
		if self.mode == 'edit':
			self.fields['movie_title'].widget.attrs['readonly'] = True


	class Meta:
		model = Rating
		fields = ('movie_title', 'movie_year', 'movie_status', 'movie_rating', 'movie_review')

	def clean_movie_title(self):
		title = self.cleaned_data["movie_title"]
		movies = Rating.objects.filter(user=self.user, movie_title=title)
		if movies and self.mode=='new':
			raise forms.ValidationError("You have already reviewed this movie")
		else:
			instance = getattr(self, 'instance', None)
			if self.mode =='edit':
				return instance.movie_title
			else:
				return self.cleaned_data['movie_title']

	def clean(self):
		status = self.cleaned_data["movie_status"]
		rating = self.cleaned_data["movie_rating"]
		review = self.cleaned_data["movie_review"]
		if status == 'Plan to watch':
			if rating or review:
				raise forms.ValidationError("You cannot rate or review a movie you have not watched yet")
		return self.cleaned_data

	def save(self, *args, **kwargs):
		self.clean()
		return super(RatingForm, self).save(*args, **kwargs)

class RegisterUserForm(UserCreationForm):
	email = forms.EmailField(required=True,label="Email",widget=forms.TextInput(attrs={'placehoder':'E-mail address'}))


	class Meta:
		model = User
		fields = ('username' , 'email', 'password1', 'password2')

	def clean(self):
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
			if self.cleaned_data['password1'] != self.cleaned_data['password2']:
				raise forms.ValidationError(_("The two password fields did not match."))
		return self.cleaned_data

class LoginForm(AuthenticationForm):

	class Meta:
		fields = ('username', 'password')