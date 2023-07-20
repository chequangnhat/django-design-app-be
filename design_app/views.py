from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import UserDesign
from django.middleware.csrf import get_token

import json

User = get_user_model()


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # email = data['email']
        password = data['password']
        username = data['username']

        user = authenticate(request, 
                            password=password, username=username)
        if user is not None:
            login(request, user)
            csrf_token = get_token(request)
            return JsonResponse({'message': 'Login successful','csrf_token': csrf_token}, safe=False)
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=401)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def logout_view(request):
    print(request)
    logout(request)
    return JsonResponse({'message': 'logout successful'})

@csrf_exempt
@login_required
def check_login_view(request):
    if request.user.is_authenticated:
        # User is logged in
        # Do something for authenticated users
        print(request.user.email)
        data = {
            'username': request.user.username,
            'message': 'You are logged in.',
        }
    else:
        # User is not logged in
        # Do something for anonymous users
        data = {
            'message': 'You are not logged in.',
        }

    return JsonResponse(data)

@csrf_exempt
def get_data_test_view(request):
    if request.user.is_authenticated:

        user = User.objects.filter(email="test1@gmail.com").first()
        print(user)
        data = {
            'username': user.username,
            'message': 'get test data.',
        }
    else:
        # User is not logged in
        # Do something for anonymous users
        data = {
            'message': 'You are not logged in to get data.',
        }

    return JsonResponse(data)


@csrf_exempt
# @login_required
def save_design_view(request):
    data_request = json.loads(request.body)
    print(request.user)
    if request.user.is_authenticated:

        user_name = data_request['username']
        design = data_request['design']


        user = User.objects.filter(username=user_name).first()
        user_design = UserDesign.objects.filter(user=user).first()

        user_design.design = design
        user_design.save()

        print(user)
        data = {
            'username': user.username,
            'message': 'save data successful',
        }
    else:
        # User is not logged in
        # Do something for anonymous users
        data = {
            'message': 'something went wrong when saving the design',
        }

    return JsonResponse(data)

@csrf_exempt
# @login_required
def csrf_token_view(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token}, safe=False)

@login_required
@csrf_exempt
def get_design_data_view(request):
    data = json.loads(request.body)
  
    if request.user.is_authenticated:

        username = data['username']


        user = User.objects.filter(email="test1@gmail.com").first()
        print(user)
        data = {
            'username': user.username,
            'message': 'get test data.',
        }
    else:
        # User is not logged in
        # Do something for anonymous users
        data = {
            'message': 'You are not logged in to get data.',
        }

    return JsonResponse(data)

@csrf_exempt
def register_view(request):
    if request.method == 'POST':

        data = json.loads(request.body)

        email = data['email']
        password = data['password']
        username = data['username']
        print('email', email)
        if email and password:
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'Email already exists'}, status=400)
            user = User.objects.create_user(
                email=email, password=password, username=username)
            return JsonResponse({'message': 'Registration successful'})
        else:
            return JsonResponse({'message': 'Invalid data'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
