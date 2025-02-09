from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from .models import CarDealer, CarMake, CarModel
from .restapis import get_dealers_from_cf, get_request, get_dealer_by_id_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)
        
# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/user_login.html", context)
    if request.method == "POST":
        uname = request.POST["username"]
        psw = request.POST["psw"]
        user = authenticate(username = uname, password = psw)
        if user is not None:
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, "djangoapp/user_login.html", context)
    else:
        return render(request, "djangoapp/user_login.html", context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect("djangoapp:index")

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = 'https://dc634a7a.us-south.apigw.appdomain.cloud/api/dealership'
        dealerships = get_dealers_from_cf(url)
        context["dealers"] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id, dealer_name):
    context = {}
    if request.method == "GET":
        url = 'https://dc634a7a.us-south.apigw.appdomain.cloud/api/review'
        reviews = get_dealer_by_id_from_cf(url, dealer_id)
        context["reviews"] = reviews
        context["dealer_id"] = dealer_id
        context["dealer_name"] = dealer_name
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id, dealer_name):
    context = {}
    context["dealer_id"] = dealer_id
    context["dealer_name"] = dealer_name
    if request.method == "GET":
        return render(request, 'djangoapp/add_review.html', context)
    if request.method == "POST":
        if request.user.is_authenticated:
            review = {}
            review["name"] = request.user.first_name
            review["id"] = request.user.id
            review["dealership"] = dealer_id
            review["review"] = request.POST["review"]
            try:
                review["purchase"] = request.POST["purchase"]
            except:
                review["purchase"] = False
            review["purchase_date"] = "01/26/2022"
            review["car_make"] = request.POST["car_make"]
            review["car_model"] = request.POST["car_model"]
            review["car_year"] = request.POST["car_year"]

            json_payload = {}
            json_payload["review"] = review

            url = 'https://dc634a7a.us-south.apigw.appdomain.cloud/api/review'
            print(json_payload)

            response = post_request(url, json_payload, dealerId=dealer_id)
            test = "Status code: " + str(response["body"])
            return redirect('djangoapp:dealer_details', dealer_id=dealer_id, dealer_name =dealer_name)