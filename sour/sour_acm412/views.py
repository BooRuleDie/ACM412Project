from django.shortcuts import render, redirect
from django.db import IntegrityError
from .models import Users
from .utils import generatePasswordHash, checkPassword

# Create the Login Business Logic after the Signup View
def Login(request):
    try:
        # redirect user to home if he is authenticated
        if request.session["user_id"]:
            print(request.session["user_id"])
            return redirect("home")
    # if user is not authenticated don't do anything
    except KeyError:
        pass

    context = { "failedLogin" : False }

    # if user submit the HTML form
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            # fetch the user object
            user = Users.objects.get(username=username)
    
            if checkPassword(password, user.password):
                request.session["user_id"] = str(user.id)
                print(request.session["user_id"])
                return redirect("home")
            else:
                context['failedLogin'] = True
        # if username or password is wrong
        except (AttributeError, Users.DoesNotExist):
            context['failedLogin'] = True

    return render(request, 'login.html', context=context)

def Signup(request):
    try:
        # redirect user to home if he is authenticated
        if request.session["user_id"]:
            print(request.session["user_id"])
            return redirect("home")
    # if user is not authenticated don't do anything
    except KeyError:
        pass
    
    context = { "failedSignup" : False }

    # if request method is POST register the new user
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        username = request.POST['username']
        password = generatePasswordHash(request.POST['password']) 
        user = Users(firstname=firstname, lastname=lastname, email=email, username=username, password=password)
        
        try:
            user.save()
        # if user tries to enter a username that is already taken, return a warning message
        except IntegrityError:
            context['failedSignup'] = True
            return render(request, 'signup.html', context=context)
        
        # if signup process is successful redirect users to the login page
        return redirect('login')
    
    # if it's a GET request load the signup form
    return render(request, 'signup.html', context=context)

def Home(request):
        return render(request, 'home.html')
