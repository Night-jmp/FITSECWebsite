from django.urls import path, include
from . import views


app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
  path("", views.homepage, name="homepage"),
  path("register/", views.register, name="register"),
  path("logout", views.logout_request, name="logout"),
  path("login", views.login_request, name="login"),
  path("verify", views.verify, name="verify"),
  path("contact", views.contact, name="contact"),
  path("about", views.about, name="about"),
  path("getinvolved", views.getinvolved, name="getinvolved"),
  path("terms", views.terms, name="terms"),
  path("press", views.press, name="press"),
  path("sponsors", views.sponsors, name="sponsors"),
  path("news", views.news, name="news"),
  path("dashboard", views.dashboard, name="dashboard"),
  path("account", views.account, name="account"),

  path("writeups", views.writeups, name="writeups"),
  path("writeups/<slug:slug>", views.writeup, name="writeup"),

  path("training", views.trainings, name="training"),
  path("training/<slug:slug>", views.training, name="training_modules"), # Need this to be training/<slug:slug>

  path("internship", views.internship, name="internship"),

  path("accounts/",include("django.contrib.auth.urls")),
  path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
]
