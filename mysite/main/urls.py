from django.urls import path
from . import views


app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
  path("", views.homepage, name="homepage"),
  path("register/", views.register, name="register"),
  path("logout", views.logout_request, name="logout"),
  path("login", views.login_request, name="login"),

  path("contact", views.contact, name="contact"),
  path("about", views.about, name="about"),
  path("getinvolved", views.getinvolved, name="getinvolved"),
  path("terms", views.terms, name="terms"),
  path("press", views.press, name="press"),
  path("sponsors", views.sponsors, name="sponsors"),
  path("news", views.news, name="news"),
  path("dashboard", views.dashboard, name="dashboard"),
<<<<<<< HEAD
<<<<<<< Updated upstream
=======
=======
>>>>>>> 89afd688c5257b6df77563486137eae0558e8210

  path("writeups", views.writeups, name="writeups"),
  path("writeups/<slug:slug>", views.writeup, name="writeup"),

  path("training", views.training, name="training"),
<<<<<<< HEAD
  #path("<slug:slug>", views.training, name="training_modules"), # Need this to be training/<slug:slug>
>>>>>>> Stashed changes
=======
  path("<slug:slug>", views.training, name="training_modules"), # Need this to be training/<slug:slug>
>>>>>>> 89afd688c5257b6df77563486137eae0558e8210
]
