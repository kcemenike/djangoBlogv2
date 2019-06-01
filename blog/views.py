from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model

from blog.forms import ContactForm, LoginForm, RegisterForm

# Create your views here.
from django.http import HttpResponse
def homepage(request):
    return HttpResponse("hello world")

def home(request):
    context = {
        "title":"Title page",
        "content":"Welcome to the home page",
        #"premium_content":"If you can see this, you are a premium member"
    }
    # if user is autheiticated, show him premium content
    if request.user.is_authenticated:
        context["premium_content"] = "If you can see this, you are a premium member"
    else:
        context["premium_content"] = "If you can see this, you need to sign up for a premium account :-)"
    return render(request, 'home.html',context)

def aboutUs(request):
    context = {
        "title":"About Us",
        "content":"Welcome to the about page",
    }
    return render(request, "base.html", context)

def contactUs(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title":"Contact Us",
        "content":"Welcome to the contact page",
        "form":contact_form
    }
    # print(contact_form)
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    # if request.method == "POST":
    #     # print(request.POST)
    #     # print(type(request))
    #     # print(request.POST["csrfmiddlewaretoken"])
    #     # print(request.POST.get("fullname"))
    #     print(request.POST["fullname"],request.POST["email"],request.POST["content"])
    return render(request,"contact/view.html",context)

def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form":form
    }
    print(1, request.user.is_authenticated)
    if form.is_valid():
        print(form)
        print(form.cleaned_data)
        # context["form"] = LoginForm()
        # Authenticate user using builtin django authenticate and login modules
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(request, username=username, password=password)
        print(2, request.user.is_authenticated)
        if user is not None:
            print(3, request.user.is_authenticated) # should be false
            login(request, user)
            print(4, request.user.is_authenticated) #should be true
            # Redirect to a success page if you want
            return redirect("/")
        else:
            # Return an invalid login error message
            print("Password invalid")

    return render(request, "auth/login.html", context)

User = get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        print(form.cleaned_data)
        # get cleaned data from form and pass it into the create user method of User.objects
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']

        # new_user = User.objects.create_user(username, email, password)
        # print(new_user)
    return render(request, "auth/register.html", context)
