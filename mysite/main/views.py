from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import NewUserForm
from .models import Writeup, Training, Training_Domain, Training_Category
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
def homepage(request):
    return render(request = request,
                  template_name='main/home.html')

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            if "@my.fit.edu" not in email:
                messages.error(request, "Not a Florida Tech email!")
            else:
                # Need to add a wait for email validation here.
                # Perhaps a validated field for users?
                messages.success(request, f"New account created: {username}")
                login(request, user)
                return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

    form = NewUserForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})


@login_required
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "main/login.html",
                    context={"form":form})


def contact(request):
    return render(request = request,
                  template_name='main/contact.html')


def about(request):
    return render(request = request,
                  template_name='main/about.html')


def writeups(request):
    all_writeups = Writeup.objects.all()
    context = {'all_writeups': all_writeups}
    return render(request = request,
                  template_name='main/writeups.html', context=context)


def getinvolved(request):
    return render(request = request,
                  template_name='main/getinvolved.html')


def terms(request):
    return render(request = request,
                  template_name='main/terms.html')


def press(request):
    return render(request = request,
                  template_name='main/press.html')


def sponsors(request):
    return render(request = request,
                  template_name='main/sponsors.html')


def news(request):
    return render(request = request,
                  template_name='main/news.html')


@login_required
def dashboard(request):
    return render(request = request,
                  template_name='main/dashboard.html')

@login_required
def training(request, slug=None):
    test = Training_Domain.objects.all()
    test_list = list(test)

    if "training" in request.path:
        all_training = Training_Domain.objects.all()
        context = {'all_training': all_training}
        return render(request = request,
                  template_name='main/training.html', context=context)

    domain_list = list(Training_Domain.objects.all())
    for domain in domain_list:
        if domain.slug in request.path:
            all_categories = Training_Domain.objects.get(slug=slug).training_category_set.all()
            context = {'all_categories': all_categories}
            return render(request = request, template_name='main/training.html', context=context)


    category_list = list(Training_Category.objects.all())
    for category in category_list:
        if category.slug in request.path:
            all_modules = Training_Category.objects.get(slug=slug).training_set.all()
            context = {'all_modules':all_modules}
            return render(request = request, template_name='main/training.html', context=context)

    module_list = list(Training.objects.all())
    for module in module_list:
        if module.slug in request.path:
            training_module = Training.objects.get(slug=slug)
            context = {'training_module':training_module}
            return render(request = request, template_name='main/training.html', context=context)

   
