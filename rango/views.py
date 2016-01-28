from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseNotFound, HttpResponseRedirect
from rango.models import Category, Page
import datetime
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

'''
def get_product(request):

    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    #likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        
    return HttpResponse("<a href='/rango/category/%s'><h4>%s</h4></br><img src=%s>" % (cat.slug, cat.name, cat.imgpath))
'''

def palautadata(request):
    if request.method == 'GET':
        cat_id = request.GET['category_id']
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        context_dict = {'sluggi': cat.slug,
                    'nimi': cat.name,
                    'kuvapolku': cat.imgpath,
                    'tykkaykset': cat.likes,
                   }
    return render(request, 'rango/categoryDiv.html', context_dict)

def like_product(request):
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        print("likeen meni");

    likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes =  likes
            cat.save()

    return HttpResponse(likes)

def index(request):

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')
    context_dict = {'categories': category_list,
                    'pageviews': page_list,
                   }
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    return render(request, 'rango/index.html', context_dict)

def categories(request):

    category_list = Category.objects.all()
    
    context_dict = {'categories': category_list}

    return render(request, 'rango/categories.html', context_dict)

@login_required
def about(request):
    #page_list = Page.objects.order_by('-views')
    #Get all objects
    pageObjects = Page.objects.all()
    categoryObjects = Category.objects.all()
    #serialize django's own format to JSON
    pageData = serializers.serialize('json', pageObjects)
    categoryData = serializers.serialize('json', categoryObjects)
    
    #prices = Page.objects.all()
    #prices_json = json.dumps({list(prices)}, cls=DjangoJSONEncoder)
    #print(data)
   
    context_dict = {'pageviews': pageData,
                    'categorylikes': categoryData,
                    'first': datetime.datetime.now().hour,
                    'toka': datetime.datetime.now().minute,
                   }
    #return HttpResponse(data, 'rango/about.html',content_type='application/json')
    return render(request, 'rango/about.html', context_dict)

def category(request, category_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}
    print(request)
    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug) #hakee kategorian paramatrinä tulevan slugin perusteella
        context_dict['category_name'] = category.name
        context_dict['imgpath'] = category.imgpath
        
        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages=Page.objects.filter(category=category)
        
        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
        
        context_dict['category_name_slug'] = category_name_slug
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us. 
        pass
    return render(request, 'rango/category.html', context_dict)

@login_required
def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
                cat = None
    
    if request.method == 'POST':
        print(cat)
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                #Ehkä tässä ois parempi käyttää redirectiä
                return category(request, category_name_slug)
        else:
            print(form.errors, "MOOO")
    else:
        #print("wrong method")
        form = PageForm(0)
        #print(PageForm)
    
    context_dict = {'form':form, 'category': cat}
    
    return render(request, 'rango/add_page.html', context_dict)
    

#Periaatteesa turha
def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s hours %s, minutes and %s secs .</body></html>" % (now.hour, now.minute, now.second)
    return HttpResponse(html)

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)

def min_ahead(request, offset, minu):
    try:    
        offset = int(offset)
        minute = int(minu)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset) + datetime.timedelta(minutes=minute)
    html = "<html><body>In %s hour(s) and %s minute(s), it will be %s.</body></html>" % (offset,minute, dt)
    return HttpResponse(html)

def register(request):
    
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False
    
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            
            user = user_form.save()
            
            user.set_password(user.password)
            user.save()
            
            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
            
            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                
            # Now we save the UserProfile model instance.
            registered = True
            # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user
        else:
            print(user_form.errors, profile_form.errors)
    #muussa tapauksessa pistä ne tyhjäks
    else: 
        user_form = UserForm()
        profile_form = UserProfileForm()
        
        
    return render(request,
                'rango/register.html', 
                {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    
    if request.method == 'POST':
        print(request.POST.get('password'))
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        #omaa saatoo
        if User.objects.filter(username=username).exists():
            print("user loytyy")
        else:
            print("no user")
            return render(request, 'rango/login.html', {'error': "User not found"})
        
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                login(request,user)
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                return HttpResponseRedirect('/rango/')
            else:
                return("Your account has been disabled")
        else:
            print("loggaus ei toimi: {0}, {1}".format(username, password))
            #return("invalidit credentiaalit tarjottu")
            return render(request, 'rango/login.html', {'error': "No matching username / password found!"})
    else:
    # No context variables to pass to the template system, hence the
    # blank dictionary object...
        return render(request, 'rango/login.html', {})

    
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/rango/')