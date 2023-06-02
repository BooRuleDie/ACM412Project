from django.shortcuts import render, redirect
from django.db import IntegrityError
from .models import Users, Topics, Comments
from .utils import generatePasswordHash, checkPassword, profilePicturePath

# Create the Login Business Logic after the Signup View
def Login(request):

    # redirect user to home if he is authenticated
    if "user_id" in request.session:
        return redirect("/")
    
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
                return redirect("/")
            else:
                context['failedLogin'] = True
        # if username or password is wrong
        except (AttributeError, Users.DoesNotExist):
            context['failedLogin'] = True

    return render(request, 'login.html', context=context)

def Signup(request):
    # redirect user to home if he is authenticated
    if "user_id" in request.session:
        return redirect("/")
    
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
    context = {
        "authenticated" : False,
        "last_8_topics" : Topics.objects.order_by('-created_at')[:8],
    }
    
    # change the content of Account Tab in the dashboard if user is authenticated -> Logout and Profile
    if "user_id" in request.session:
        context['authenticated'] = True
        context['current_user'] = request.session["user_id"]
    
    # if user hits the logout button, remove the session cookie
    if "logout" in request.POST:
        del request.session["user_id"]
        context['authenticated'] = False

    return render(request, 'home.html', context=context)

def Profile(request, user_id):
    user = Users.objects.get(id=user_id)
    context = {
            "user" : user,
            "summary": user.summary,
            "username" : user.username,
            "profile_owner_id" : str(user.id),
            "user_topics": Topics.objects.filter(user_id = user.id)[:8]
    }

    if "user_id" in request.session:
        context["authenticated"] = True
        context['current_user'] = request.session["user_id"]

    if "logout" in request.POST:
        del request.session["user_id"]
        context['authenticated'] = False

    return render(request, 'profile.html', context=context)

def TopicView(request, topic_id):
    topic = Topics.objects.get(id=topic_id)
    comments = Comments.objects.filter(topic_id = topic.id)[:4]
    context = {
        "topic_id" : topic.id,
        "title" : topic.title,
        "username" : topic.user_id.username,
        "user_id" : topic.user_id.id,
        "origin_comment" : topic.origin_comment,
        "comments" : [
                {
                    "comment_id" : comment.id,
                    "comment_username" : comment.user_id.username, # since user_id column refers to the Users Model we can fetch any info from Users model through user_id column
                    "comment_user_id" : comment.user_id.id,
                    "comment_content" : comment.comment,
                    "comment_upvotes" : comment.upvotes.count(),
                    "comment_downvotes" : comment.downvotes.count()
                } for comment in comments
        ]
    }
    
    if "user_id" in request.session:
        context["authenticated"] = True
        context['current_user'] = request.session["user_id"]

    if "logout" in request.POST:
        del request.session["user_id"]
        context['authenticated'] = False

    return render(request, 'topic.html', context=context)

def HandleModalSubmits(request):
    # if it's a POST request and user is authenticated
    if request.method == "POST" and "user_id" in request.session:
        
        # if user submit a topic registration request
        if "register-topic" in request.POST:            
            current_path = request.POST["current-path"]
            title = request.POST["topic-title"]
            comment = request.POST["topic-comment"]
            user = Users.objects.get(id = request.session["user_id"])
            
            # since user_id refers to the User Model you can't assign a string value, you must assign an instance of User model
            topic = Topics(title=title, origin_comment=comment, user_id=user)
            
            try:
                topic.save()
                return redirect(current_path)         
            # if an error occurs redirect users to the main page
            except IntegrityError:
                return redirect("/")           

        # if user submit a comment registration request
        if "register-comment" in request.POST:            
            current_path = request.POST["current-path"]
            topic_id = request.POST["topic-id"]
            topic_comment = request.POST["topic-comment"]
            user = Users.objects.get(id = request.session["user_id"])
            topic = Topics.objects.get(id = topic_id)
            
            # since user_id refers to the User Model you can't assign a string value, you must assign an instance of User model
            comment = Comments(comment = topic_comment, user_id = user, topic_id = topic)
            
            try:
                comment.save()
                return redirect(current_path)         
            # if an error occurs redirect users to the main page
            except IntegrityError:
                return redirect("/")
            
        # if user submit a update-user-info request
        if "update-profile-info" in request.POST:  
            user_id = request.session["user_id"]
            current_path = request.POST["current-path"]
            firstname = request.POST["firstname"]
            lastname = request.POST["lastname"]
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]
            summary = request.POST["summary"]
            user = Users.objects.get(id = user_id)
            # if there is such a key called profile-picture
            if "profile-picture" in request.FILES:     
                profile_picture = request.FILES["profile-picture"]
                pp_path, filename = profilePicturePath(user_id)
                user.profile_picture = filename
                
                # write the profile picture to the static directory in following format <user_id>_<timestamp>.png
                with open(pp_path, "wb") as fp:
                    for chunk in profile_picture.chunks():
                        fp.write(chunk)
            
            # apply the other changes
            user.firstname = firstname
            user.lastname = lastname
            user.username = username
            user.email = email
            user.summary = summary
            if user.password != password:
                user.password = generatePasswordHash(password)
            
            # save the changes
            user.save()
            
            return redirect(current_path)
            
    # if it's a GET request or if user is not authenticated return users to the login page
    return redirect("/login")


