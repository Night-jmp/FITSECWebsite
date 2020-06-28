from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import NewUserForm, FlagCheckForm, SignUpForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode

# Create your views here.
def homepage(request):
    return render(request = request,
                  template_name='main/home.html')

def register(request):
    if request.method  == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email') 
            userObj = User.objects.all().filter(email=email)
            
        
            if "fit.edu" not in email:
                messages.error(request, "Not a Florida Tech email!")
            elif userObj:
                messages.error(request, "Email address already registered!")
            else:
                user = form.save()
                user.refresh_from_db()
                user.profile.first_name = form.cleaned_data.get('first_name')
                user.profile.last_name = form.cleaned_data.get('last_name')
                user.profile.email = form.cleaned_data.get('email')
                # user can't login until link confirmed
                user.is_active = False
                user.save()
                subject = 'Please Activate Your Account'
                # load a template like get_template() 
                # and calls its render() method immediately.
                message = render_to_string('registration/activation_request.html', {
                    'user': user,
                    'domain': "www.fitsec.org",
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    # method will generate a hash value with user related data
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject, message)
                return render(request, 'registration/activation_sent.html')
    else:
        form = SignUpForm()
    return render(request, 'main/register.html', {'form': form})

#def register(request):
#    if request.method == "POST":
#        form = NewUserForm(request.POST)
#        if form.is_valid():
#            
#            username = form.cleaned_data.get('username')
#            email = form.cleaned_data.get('email')
#            user = User.objects.all().filter(email=email)
#            #if "fit.edu" not in email:
#            #    messages.error(request, "Not a Florida Tech email!")
#            if user:
#                messages.error(request, "Email address already registered!")
#            else:
#                # Need to add a wait for email validation here.
#                # Perhaps a validated field for users?
#                subject = "Welcome to FITSEC!"
#                message = "Thank you for registering your email."
#                from_mail = settings.EMAIL_HOST_USER
#                to_mail = [email, from_mail]
#                send_mail(subject, message, from_mail, to_mail)
#                messages.success(request, f"New account created: {username}")
#
#                user = form.save()
#                
#                #login(request, user)
#                return redirect(reverse('main:verify'))
#
#        else:
#            for msg in form.error_messages:
#                messages.error(request, f"{msg}: {form.error_messages[msg]}")
#
#            return render(request = request,
#                          template_name = "main/register.html",
#                          context={"form":form})
#
#    form = NewUserForm
#    return render(request = request,
#                  template_name = "main/register.html",
#                  context={"form":form})


def verify(request):
    return render(request=request, template_name="main/verify.html")
   

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
                if user.is_active:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}")
                    return redirect('/')
                else:
                    messages.error("Unverified account!")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
            #return redirect(reverse("main:verify"))
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


def writeups(request, slug=None):
    all_writeups = Writeup.objects.all()
    context = {'all_writeups': all_writeups}
    return render(request = request,
                  template_name='main/writeups.html', context=context)

def writeup(request, slug=None):
    writeup = Writeup.objects.get(slug=slug)
    context = {'writeup':writeup}
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

    domain_list = list(Training_Domain.objects.all())
    for domain in domain_list:
        if domain.slug in request.path:
            all_categories = Training_Domain.objects.get(slug=slug).training_category_set.all()
            context = {'all_categories': all_categories}
            request.path = "training/" + request.path
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
            try:
                completed = False
                user_training = list(TrainingCompletion.objects.all().filter(user=request.user.id))
                for training in user_training:
                    if training.module == training_module:
                        completed = True
            except:
                completed = False
            if completed != True:
                if request.method == "POST":
                    flag_check = FlagCheckForm(request.POST)
                    if flag_check.is_valid():
                        flag = flag_check.cleaned_data.get('input_flag')
                        if flag == training_module.flag:
                            TrainingCompletion.objects.create(module=training_module, user=request.user, completed=True)
                            currentFitcoins = Profile.objects.get(user=request.user.id).fitcoins
                            Profile.objects.filter(user=request.user.id).update(fitcoins=currentFitcoins + 10)
                            
                            messages.success(request, f'Correct flag! {flag}')

                            all_modules=training_module.category.training_set.all()
                            context = {'all_modules':all_modules}
                            return render(request=request, template_name='main/training.html', context=context)
                        else:
                            messages.error(request, f'Incorrect flag!')

            flag_check = FlagCheckForm()
            context = {'training_module':training_module, 'flag_check':flag_check,"completed":completed}
            return render(request = request, template_name='main/training.html', context=context)



@login_required
def trainings(request, slug=None):

    if "training" in request.path:
        all_training = Training_Domain.objects.all()
        context = {'all_training': all_training}
        return render(request = request,
                  template_name='main/training.html', context=context)


@login_required
def account(request):
    modules = Training.objects.all()
    completed = TrainingCompletion.objects.all().filter(user=request.user.id)
    domains = Training_Domain.objects.all()
    fitcoins = Profile.objects.get(user=request.user.id).fitcoins

    domainDict = {}
    for x in modules:
        if x.category.domain not in domainDict:
            domainDict.update({x.category.domain:[1,0]})
        else:
            domainDict[x.category.domain][0] += 1

    for x in completed:
        domainDict[x.module.category.domain][1] += 1

    catDict = {}
    for x in modules:
        if x.category not in catDict:
            catDict.update({x.category:[1,0]})
        else:
            catDict[x.category][0] += 1

    for x in completed:
        catDict[x.module.category][1] += 1
    
    context = {'modules':modules, 'completed':completed, 'domainDict':domainDict, 'catDict':catDict, 'fitcoins':fitcoins}
    return render(request=request, template_name="main/account.html", context=context)

@login_required
def internship(request, slug=None):
    internships = Internship.objects.all()
    context = {'internships': internships}
    return render(request=request, template_name="main/internship.html", context=context)

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'registration/activation_invalid.html')

@login_required
def store(request):
    items = StoreItem.objects.all()
    context = {'items':items}
    return render(request=request, template_name="main/store.html", context=context)
