from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.http import HttpResponse, HttpResponseRedirect
#bring in some things to make auth easier
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Import the login_required decorator---> to be able to use @login_required
from django.contrib.auth.decorators import login_required

# import models
from .models import Cat
# access the FeedingForm
from .forms import FeedingForm, CatForm

# import Django form classes
# these handle CRUD for us
# we will comment this one out
# class CatCreate(CreateView):
#   model = Cat
#   fields = '__all__'
#   success_url = '/cats'
# not enough anymore, we need to associate a created cat with a user


class CatUpdate(UpdateView):
  model = Cat
  fields = ['name', 'breed', 'description', 'age']

  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.save()
    return HttpResponseRedirect('/cats/' + str(self.object.pk))


class CatDelete(DeleteView):
  model = Cat
  success_url = '/cats'


# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


# CATS
# protect to be shown only for member user => @login_required or @login_required()(?!)
@login_required
def cats_index(request):
    # cats = Cat.objects.all()
    # we want to have access to the user request.user - only cats that belong to one user
    cats = Cat.objects.filter(user = request.user)
    return render(request, 'cats/index.html', { 'cats': cats })

@login_required
def cats_show(request, cat_id):
    # we get access to that cat_id variable
    # query for the specific cat clicked
    cat = Cat.objects.get(id=cat_id)
    # lets make a feeding_form
    feeding_form = FeedingForm()
    return render(request, 'cats/show.html', { 
      'cat': cat,
      'feeding_form': feeding_form 
    })
# def cats_update(request, cat_id):
#   # create a catform
#   cat = Cat.objects.get(id=cat_id)
#   print('***************')
#   print(cat)
#   catform = CatForm(cat)
#   return render(request, 'cats/cat_form.html', {'form': catform })




# build out cats_new custom to use the userId
@login_required
def cats_new(request):
  # create new instance of cat form filled with submitted values or nothing
  cat_form = CatForm(request.POST or None)
  # if the form was posted and valid
  # if this is a GET request, it will be none (we are mergeing gET and POST route in one!!)
  if request.POST and cat_form.is_valid():
    new_cat = cat_form.save(commit=False)
    new_cat.user = request.user
    new_cat.save()
    # redirect to index
    return redirect('index')
  else:
    #this handle the GET request
    # render the page with the new cat form
    return render(request, 'cats/new.html', { 'cat_form': cat_form })

# FEEDING
@login_required
def add_feeding(request, pk):
  # this time we are passing the data from our request in that form
  form = FeedingForm(request.POST)
  # validate form.is_valid built in
  if form.is_valid():
    # don't save yet!! First lets add out cat_id
    new_feeding = form.save(commit=False)
    new_feeding.cat_id = pk
    # cats been added we can save
    new_feeding.save()
  return redirect('cats_show', cat_id = pk)


def sign_up(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A GET or a bad POST request, so render signup.html with an empty form
  #this will run after if it is not a POST or it is invalid
  form = UserCreationForm()
  return render(request, 'registration/signup.html', {
    'form': form, 
    'error_message': error_message
  })



  

# Instrcutions
# 1. Update index view function to look similar to the contact view function
# 2. Add a index.html page with the current HTML that is displayed
# 3. Update about view function to look similar to the contact view function
# 4. Add a about.html page with the current HTML that is displayed
# 5. Update your urls.py file (main_app) to look similar to the contact path

# 1. Make a view function
# 2. Make the html page
# 3. Add the view to the urls.py inside of main_app.urls

# In browser
# When I go to localhost:8000/contact
# Django -> urls -> /contact -> vews.contact (runs function) -> templates -> contact.html
