from django.shortcuts import render, redirect
from .models import Home
# create your view here.
def StartPage(request):
    return render(request, 'home/index.html')

def wwe_page(request):
    if request.method == 'POST':
        data = request.POST
        # can replace with data = request.POST.dict() if you want to convert QueryDict to a regular dict
        username = request.POST.get('username')
        email = request.POST.get('email')
        wrestler_name = request.POST.get('wrestler_name')
        wrestler_image = request.FILES.get('wrestler_image')
        wrestler_description = request.POST.get('wrestler_description')
        # print(username, email, wrestler_name, wrestler_image, wrestler_description)
        Home.objects.create(
            username=username,
            email=email,
            wrestler_name=wrestler_name,
            wrestler_image=wrestler_image,
            wrestler_description=wrestler_description
        )
        
        return redirect('/wwe_page/') 
    
    return render(request, 'home/wwe_page.html', context={'wrestlers': Home.objects.all()})

def delete_wrestler(request , id):
    query = Home.objects.get(id=id)
    query.delete()
    # after deleting the wrestler, redirect to the wwe_page
    return redirect('/wwe_page/') 
      
def update_wrestler(request, id):
    # This function can be implemented if you want to update wrestler details
    query = Home.objects.get(id=id)
 
    if request.method == 'POST':
        data = request.POST
        query.username = data.get('username')
        query.email = data.get('email')
        query.wrestler_name = data.get('wrestler_name')
        if 'wrestler_image' in request.FILES:   # Check if a new image is uploaded
            query.wrestler_image = request.FILES['wrestler_image']
        query.wrestler_description = data.get('wrestler_description')
        query.save()
        return redirect('/wwe_page/')
    
    return render(request, 'home/update_wrestler.html', context={'wrestler': query})