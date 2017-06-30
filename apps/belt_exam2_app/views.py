from django.shortcuts import render, redirect, reverse
from .models import User, Poke
from django.contrib import messages
from django.db.models import Count

def errorMessage(request, errors):
    for error in errors:
        messages.error(request, error)

def currentUser(request):
    user_id = request.session['user_id']
    return User.objects.get(id=user_id)

def index(request):
    
    return render(request, "belt_exam2_app/index.html")

def success(request):
    print "Inside the success method"
    current_user = currentUser(request)
    other_users = User.objects.exclude(id=current_user.id)
    users_poked_me = len(current_user.poked_by.values_list('poker_id', flat=True).distinct().exclude(id=current_user.id))
    my_pokes = list(Poke.objects.annotate(num_pokes=Count('poker', distinct=True)).filter(pokee=current_user).order_by('-num_pokes'))
    pokes = current_user.poked_by.all()

    print my_pokes
    

    content = {
        'other_users': other_users,
        'current_user': current_user,
        'users_poked_me': users_poked_me,
        'pokes': pokes,
        'my_pokes': my_pokes
    }

    
    

    return render(request, "belt_exam2_app/success.html", content)

def create_user(request):
    
    if request.method == 'POST':
        
        form_valid = User.objects.validate(request.POST)
        
        if form_valid == []:

            user = User.objects.register(request.POST)

            request.session['user_id'] = user.id
            
            return redirect('/success')

        errorMessage(request, form_valid)
        
        return redirect('/')

def logout(request):
    request.session.pop('user_id')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        
        data_check = User.objects.validate_login(request.POST)
        print data_check
        if type(data_check) == type(User()):

            request.session['user_id'] = data_check.id

            return redirect('/success')
        
        errorMessage(request, data_check)

        return redirect('/')


def poke(request, id):
    print "Inside the poke method."

    if request.method == "POST":
        current_user = currentUser(request)
        user = User.objects.get(id=id)
        poke = Poke.objects.create(poker=current_user, pokee=user)

    return redirect('/success')