from django.shortcuts import render, redirect
from django import forms
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import User, Food, FoodCategory, FoodLog, Image, Weight
from .form import FoodForm, ImageForm


def index(request):
    return food_list_view(request)

User = get_user_model()

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        confirmation = request.POST['confirmation']

        if password != confirmation:
            return render(request, 'register.html', {
                'message': 'Passwords must match.',
                'categories': FoodCategory.objects.all()
            })

        try:
            user = User.objects.create(
                email=email,
                password=make_password(password)  
            )
            user.save()
        except IntegrityError:
            return render(request, 'register.html', {
                'message': 'Email already taken.',
                'categories': FoodCategory.objects.all()
            })

        login(request, user)
        return redirect('index')

    else:
        return render(request, 'register.html', {
            'categories': FoodCategory.objects.all()
        })

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {
                'message': 'Invalid email and/or password.',
                'categories': FoodCategory.objects.all()
            })
    else:
        return render(request, 'login.html', {
            'categories': FoodCategory.objects.all()
        })
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def food_details_view(request, food_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    food = Food.objects.get(id=food_id)

    return render(request, 'food.html', {
        'categories': FoodCategory.objects.all(),
        'food': food,
        'images': food.get_images.all(),
    })

def food_list_view(request):
    foods = Food.objects.all()

    for food in foods:
        food.image = food.get_images.first()

    page = request.GET.get('page', 1)
    paginator = Paginator(foods, 4)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {
        'categories': FoodCategory.objects.all(),
        'foods': foods,
        'pages': pages,
        'title': 'Food List'
    })


@login_required
def food_add_view(request):
    ImageFormSet = forms.modelformset_factory(Image, form=ImageForm, extra=2)

    if request.method == 'POST':
        food_form = FoodForm(request.POST, request.FILES)
        image_form = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())

        if food_form.is_valid() and image_form.is_valid():
            new_food = food_form.save(commit=False)
            if not new_food.calories:
                new_food.calories = (
                    (new_food.fat * 9) +
                    (new_food.carbohydrates * 4) +
                    (new_food.protein * 4)
                )
            new_food.save()

            for food_form in image_form.cleaned_data:
                if food_form:
                    image = food_form['image']

                    new_image = Image(food=new_food, image=image)
                    new_image.save()

            return render(request, 'food_add.html', {
                'categories': FoodCategory.objects.all(),
                'food_form': FoodForm(),
                'image_form': ImageFormSet(queryset=Image.objects.none()),
                'success': True
            })

        else:
            return render(request, 'food_add.html', {
                'categories': FoodCategory.objects.all(),
                'food_form': FoodForm(),
                'image_form': ImageFormSet(queryset=Image.objects.none()),
            })

    else:
        return render(request, 'food_add.html', {
            'categories': FoodCategory.objects.all(),
            'food_form': FoodForm(),
            'image_form': ImageFormSet(queryset=Image.objects.none()),
        })


@login_required
def food_log_view(request):
    if request.method == 'POST':
        foods = Food.objects.all()

        food = request.POST['food_consumed']
        food_consumed = Food.objects.get(food_name=food)

        user = request.user

        food_log = FoodLog(user=user, food_consumed=food_consumed)
        food_log.save()

    else: 
        foods = Food.objects.all()

    user_food_log = FoodLog.objects.filter(user=request.user)

    return render(request, 'food_log.html', {
        'categories': FoodCategory.objects.all(),
        'foods': foods,
        'user_food_log': user_food_log
    })


@login_required
def food_log_delete(request, food_id):
    food_consumed = get_object_or_404(FoodLog, id=food_id)

    if request.method == 'POST':
        food_consumed.delete()
        return redirect('food_log')

    return render(request, 'food_log_delete.html', {
        'food_item': food_consumed,
        'categories': FoodCategory.objects.all(),
    })


@login_required
def weight_log_view(request):
    '''
    It allows the user to record their weight
    '''
    if request.method == 'POST':

        weight = request.POST['weight']
        entry_date = request.POST['date']

        user = request.user

        weight_log = Weight(user=user, weight=weight, entry_date=entry_date)
        weight_log.save()

    user_weight_log = Weight.objects.filter(user=request.user)

    return render(request, 'profile.html', {
        'categories': FoodCategory.objects.all(),
        'user_weight_log': user_weight_log
    })

@login_required
def weight_log_edit(request, weight_id):
    weight_record = get_object_or_404(Weight, id=weight_id, user=request.user)

    if request.method == 'POST':
        weight_record.weight = request.POST['weight']
        weight_record.entry_date = request.POST['date']
        weight_record.save()

        return redirect('profile')  

    return render(request, 'weight_edit.html', {
        'weight_record': weight_record
    })

@login_required
def weight_log_delete(request, weight_id):
    weight_recorded = get_object_or_404(Weight, id=weight_id, user=request.user)

    if request.method == 'POST':
        weight_recorded.delete()
        return redirect('profile')

    return render(request, 'weight_delete.html', {
        'categories': FoodCategory.objects.all(),
        'weight_record': weight_recorded  
    })


def categories_view(request):
    return render(request, 'categories.html', {
        'categories': FoodCategory.objects.all()
    })


def category_details_view(request, category_name):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    category = FoodCategory.objects.get(category_name=category_name)
    foods = Food.objects.filter(category=category)

    for food in foods:
        food.image = food.get_images.first()

    page = request.GET.get('page', 1)
    paginator = Paginator(foods, 4)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(request, 'food_category.html', {
        'categories': FoodCategory.objects.all(),
        'foods': foods,
        'foods_count': foods.count(),
        'pages': pages,
        'title': category.category_name
    })

@login_required
def reset_daily_goal(request):
    if request.method == 'POST':
        user = request.user
        try:
            user.food_log.clear()
            messages.success(request, "Daily goal reset successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
        return redirect('food/foodlog') 
    return redirect('food/foodlog')
# Create your views here.
