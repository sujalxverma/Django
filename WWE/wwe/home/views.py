from django.shortcuts import render, redirect
from .models import Home
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# create your view here.
def StartPage(request):
    return render(request, "home/index.html")

@login_required(login_url='/login/')
def wwe_page(request):
    if request.method == "POST":
        data = request.POST
        # can replace with data = request.POST.dict() if you want to convert QueryDict to a regular dict
        username = request.POST.get("username")
        email = request.POST.get("email")
        wrestler_name = request.POST.get("wrestler_name")
        wrestler_image = request.FILES.get("wrestler_image")
        wrestler_description = request.POST.get("wrestler_description")
        # print(username, email, wrestler_name, wrestler_image, wrestler_description)
        Home.objects.create(
            username=username,
            email=email,
            wrestler_name=wrestler_name,
            wrestler_image=wrestler_image,
            wrestler_description=wrestler_description,
        )

        return redirect("/wwe_page/")

    return render(
        request, "home/wwe_page.html", context={"wrestlers": Home.objects.all()}
    )

@login_required(login_url='/login/')
def delete_wrestler(request, id):
    query = Home.objects.get(id=id)
    query.delete()
    # after deleting the wrestler, redirect to the wwe_page
    return redirect("/wwe_page/")

@login_required(login_url='/login/')
def update_wrestler(request, id):
    # This function can be implemented if you want to update wrestler details
    query = Home.objects.get(id=id)

    if request.method == "POST":
        data = request.POST
        query.username = data.get("username")
        query.email = data.get("email")
        query.wrestler_name = data.get("wrestler_name")
        if "wrestler_image" in request.FILES:  # Check if a new image is uploaded
            query.wrestler_image = request.FILES["wrestler_image"]
        query.wrestler_description = data.get("wrestler_description")
        query.save()
        return redirect("/wwe_page/")

    return render(request, "home/update_wrestler.html", context={"wrestler": query})


def login_page(request):
    
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        
        # first check if the user exists
     
        if(not User.objects.filter(username=username).first()):
            messages.info(request, 'User does not exist.')
            return redirect('/login/')  # Redirect to login page if user does not exist
            
        user = authenticate(request , username = username, password = password)
        if user is None :
            messages.info(request, 'Invalid credentials. Please try again.')
            return redirect('/login/')
        else :
            # messages.info(request, 'Login successful.')
            login(request, user)
            return redirect('/wwe_page/')  # Redirect to receipe page after successful login
         
    return render(request, "home/login.html")



def register_page(request):
    # This function can be implemented if you want to add a registration page
    if request.method == "POST":
        data = request.POST
        username = data.get("username")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        password = data.get("password")

        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(
                request, "Username already exists. Please try a different one."
            )
            return redirect(
                "/register/"
            )  # Redirect to register page if user already exists

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        """
        # user.set_password(password)  # Ensure the password is hashed, used when User.objects.create is not used
        # If we have used User.objects.create_user, we don't need to set password again, it automatically hashes the password.
        """
        # Save the user to the database
        user.save()
        messages.info(request, "Account created successfully.")
        return redirect(
            "/login/"
        )  # Redirect to login page after successful registration

    return render(request, "home/register.html")


def logout_page(request):
    logout(request)
    return redirect('/login/')  # Redirect to login page after logout

