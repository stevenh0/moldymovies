from django.db import models
from django import forms
# Create your models here.

class Rating(models.Model):
	user = models.ForeignKey('auth.User')
	movie_title = models.CharField(max_length = 200)
	movie_year = models.CharField(max_length = 4)
	movie_status = models.CharField(max_length = 20)
	movie_rating = models.CharField(max_length = 1)
	movie_review = models.TextField(blank = True)

	def __str__(self):
		return self.movie_title
