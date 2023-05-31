from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from .models import Author, Quote, Tag
import requests
from bs4 import BeautifulSoup

def signup(request):
    if request.method == 'POST':
        user = User.objects.create_user(request.POST['username'], password=request.POST['password'])
        user.save()
        return HttpResponseRedirect('/login')
    else:
        return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'login.html', {"error": "Invalid login credentials"})
    else:
        return render(request, 'login.html')

@login_required
def add_author(request):
    if request.method == 'POST':
        author = Author.objects.create(name=request.POST['name'], user=request.user)
        author.save()
        return HttpResponseRedirect('/authors')
    else:
        return render(request, 'add_author.html')

@login_required
def add_quote(request):
    if request.method == 'POST':
        author = Author.objects.get(id=request.POST['author_id'])
        quote = Quote.objects.create(text=request.POST['quote'], author=author)
        quote.save()
        return HttpResponseRedirect('/quotes')
    else:
        return render(request, 'add_quote.html')

def quote_list(request):
    quotes_list = Quote.objects.all()
    paginator = Paginator(quotes_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'quotes.html', {'page_obj': page_obj})

def search_by_tag(request, tag_name):
    tag = Tag.objects.get(name=tag_name)
    quotes = tag.quotes.all()
    return render(request, 'quotes.html', {'quotes': quotes})

def scrape_website(request):
    response = requests.get('http://quotes.toscrape.com')
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find_all('div', class_='quote')
    for quote in quotes:
        text = quote.find('span', class_='text').text
        author_name = quote.find('small', class_='author').text
        author, created = Author.objects.get_or_create(name=author_name)
        Quote.objects.create(text=text, author=author)
    return HttpResponseRedirect('/')
