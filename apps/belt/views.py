# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Quote, Favorite, Registration, Login
#TODO REMOVE AFTER TESTING
import bcrypt
import md5
# Create your views here.
def index(request):
    if request.session.has_key('id'):
        return redirect('/success/' + str(request.session['id']))
    return render(request, 'belt/index.html')


def register(request):
    if request.method == 'POST':
        newuser = Registration()
        newuser.first_name = request.POST['first_name'].lower()
        newuser.last_name = request.POST['last_name'].lower()
        newuser.email = request.POST['email'].lower()
        newuser.pw_1 = request.POST['pw_1'].encode()
        newuser.pw_2 = request.POST['pw_2'].encode()
        newuser.birthday = request.POST['birthday']
        newuser.validate()
        for x in newuser.message:
            messages.warning(request, x)
        if newuser.is_valid:
            newuser.create_user()
            request.session['id'] = newuser.id
            return redirect('success/{}'.format(request.session['id']))
        else:
            return redirect('/')
    else:
        return redirect('/')
        # try to move


def success(request, id):
    fav_user = User.objects.filter(id=request.session['id'])[0]
    quotes = Quote.objects.all()
    favorites = Favorite.objects.filter(user=fav_user)
    fav_id_list = []
    quote_id_list = []
    filtered_list = []
    for quote in quotes:
        quote_id_list.append(quote.id)
    for favorite in favorites:
        fav_id_list.append(favorite.quote.id)

    # print quote_id_list
    # print fav_id_list
    #****INITIAL MESSY LOGIC WITH FILTERING FAVORITE LISTS******
    x = 0
    while x < len(quote_id_list):
        unique = True
        y = 0
        while y <len(fav_id_list):
            if quote_id_list[x] == fav_id_list[y]:
                unique = False
            y += 1
        if unique == True:
            filtered_list.append(quote_id_list[x])
        x += 1
    print filtered_list

    filtered = []
    for x in filtered_list:
        pushed = Quote.objects.filter(id=x)[0]
        filtered.append(pushed)

    print "*" * 100
    print filtered[0].id
    #******END OF FILTERING FAVORITE LOGIC******

    if not request.session.has_key('id'):
        messages.warning(request, "DON'T YOU TAMPER WITH ME MAN")
        return redirect('/')
    id = request.session['id']
    user = User.objects.filter(id=id)
    context = {
            'users':user,
            'allquotes':quotes,
            'favorites':favorites,
            'filtered':filtered
    }
    return render(request, 'belt/logged.html', context)

def login(request):
    userlog = Login()
    userlog.email = request.POST['email']
    userlog.pw = request.POST['pw_1'].encode()
    userlog.validation()
    for x in userlog.message:
        messages.warning(request, x)
    if userlog.validate:
        request.session['id'] = userlog.id
        return redirect('/success/{}'.format(request.session['id']))
    else:
        return redirect('/')


def logout(request):
    request.session.pop('id')
    request.session.flush()
    return redirect('/')

def account(request):
    return redirect('/')

def createquote(request):
    quotes = Quote.objects.all()
    user = User.objects.filter(id=request.session['id'])[0]
    author = request.POST['author']
    message = request.POST['message']
    valid = True
    if len(author) < 3:
        valid = False
        messages.warning(request, "Author name must be longer than 3 characters!")
    if len(message) < 10:
        valid = False
        messages.warning(request, "Message must be longer than 10 characters!")
    if valid:
        quote = Quote.objects.create(content=message, author=author, user=user)
    context = {
        'allquotes': quotes
    }
    return redirect('/success/{}'.format(request.session['id']))

def favorite(request, quote_id):
    user = User.objects.filter(id=request.session['id'])[0]
    quote = Quote.objects.filter(id=quote_id)[0]
    fav = Favorite.objects.create(user=user, quote=quote)
    print "*" * 100
    print fav.quote.id
    return redirect('/success/{}'.format(request.session['id']))

def removefav(request, fav_id):
    Favorite.objects.filter(id=fav_id).delete()
    return redirect('/success/{}'.format(request.session['id']))

def individual(request, user_id):
    print "NO work"
    user = User.objects.get(id=user_id)
    quote_list = Quote.objects.filter(user=user)
    counter = len(quote_list)
    print counter
    context = {
        'user':user,
        'counter':counter,
        'quote':quote_list
    }
    return render(request, 'belt/individual.html', context)









    # def nein(request, word):
    #     messages.warning(request, "DON'T GO TO PLACES THAT DO NOT EXIST. IT'S DANGEROUS! 404! 404!")
    #     return redirect('/')
