from django.shortcuts import render, get_object_or_404, redirect
from .models import Rating
from .forms import RatingForm, RegisterUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, logout
from urllib.request import Request, urlopen, URLError
import json
# Create your views here.

# signup/login auth views
def register_success(request):
	return render(request, 'movierating/register_success.html', {})

def login_success(request):
	return redirect('home')

def logout_view(request):
	logout(request)
	return redirect('home')

def signup(request):
	if request.method == "POST":
		form = RegisterUserForm(request.POST)
		if form.is_valid():
			form.save
			return redirect('register_success')
	else:
		form = RegisterUserForm()
	return render(request, 'movierating/signup.html', {'form':form})

# home/review index views

def home_site(request):
	ratings = Rating.objects.exclude(movie_review__isnull=True).exclude(movie_review__exact='').order_by('-id')[:10]
	return render(request, 'movierating/index.html', {'ratings':ratings})


def rating_detail(request, pk):
	rating = get_object_or_404(Rating, pk=pk)
	httprequest = Request('http://www.omdbapi.com/?t=' + rating.movie_title + '&plot=full')
	try:
		response = urlopen(httprequest)
		encoding = response.info().get_content_charset('utf-8')
		movie_data = response.read()
		movie_json = json.loads(movie_data.decode(encoding))
		if(movie_json["Response"]=="False"):
			movie_json = {'Poster':"N/A", 'Rated':'N/A', 'imbdRating':'N/A', 'Plot':'Movie not found'}

	except Exception:
		print("something went wrong")
	return render(request, 'movierating/rating_detail.html', {'rating': rating, 'movie_data':movie_json})

def rating_list(request):
	ratings = Rating.objects.filter(user=request.user).order_by('-id')
	return render(request, 'movierating/rating_list.html', {'ratings':ratings})

# review add/change/remove views

def rating_new(request):
	if request.method == "POST":
		form = RatingForm(request.POST, user=request.user, mode='new')
		if form.is_valid():
			print(form.errors)
			rating = form.save(commit=False)
			rating.user = request.user
			rating.save()
			return redirect('rating_list')
	else:
		form = RatingForm(user=request.user, mode='new')
	return render(request, 'movierating/rating_new.html', {'form':form})

def rating_edit(request, pk):
	rating = get_object_or_404(Rating, pk=pk)
	if request.method == "POST":
		form = RatingForm(request.POST, instance=rating, user=request.user, mode='edit')
		if form.is_valid():
			rating = form.save(commit=False)
			rating.user = request.user
			rating.save()
			return redirect('rating_list')
	else:
		form = RatingForm(instance=rating, user=request.user, mode='edit')
	return render(request, 'movierating/rating_new.html', {'form': form})

def rating_remove(request, pk):
	rating = get_object_or_404(Rating, pk=pk)
	rating.delete()
	return render(request, 'movierating/rating_remove.html')

# report views

def report_view(request):
	objs = Rating.objects.all().order_by('movie_title')
	return render(request, 'movierating/reports.html', {'objs':objs})

def report_detail(request, pk):
	rating = get_object_or_404(Rating,pk=pk)
	reports = Rating.objects.filter(movie_title=rating)
	return render(request, 'movierating/report_detail.html', {'reports':reports})