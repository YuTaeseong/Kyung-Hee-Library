from django.shortcuts import render, redirect
from . import forms
from selenium import webdriver
from django.http import Http404
from .models import library_profile, user_barrow_books, user_token
from bs4 import BeautifulSoup
import json
from django.http import JsonResponse

# Create your views here.

def do_you_sign_up(request) :
    if hasattr(request.user, 'library_profile') :
        return redirect('service')
    else :
        form = forms.library_sign_up_form()
        return render(request, 'library/sign_up.html',{'form' : form})

def library_sign_up(request) :
    if request.method == 'POST' :
        form = forms.library_sign_up_form(request.POST)
        if form.is_valid() :
            library_id = form.cleaned_data.get('library_id')
            library_password = form.cleaned_data.get('library_password')

            url_driver = '/Users/YuGeekLab/Desktop/phantomjs-2.1.1-windows/bin/phantomjs'

            try:
                driver = webdriver.PhantomJS(url_driver)
                driver.implicitly_wait(3)
            except:
                return Http404('some message')

            driver.get('https://khis.khu.ac.kr/identity/Login.ax?url=%2Fmylibrary%2FCirculation.ax')

            user_id = library_id
            user_pw = library_password

            driver.find_element_by_name('userID').send_keys(user_id)
            driver.find_element_by_name('password').send_keys(user_pw)

            driver.find_element_by_xpath('//*[@id="loginForm"]/dd[2]/a/span').click()

            driver.get('https://khis.khu.ac.kr/mylibrary/Circulation.ax')

            if driver.current_url == 'https://khis.khu.ac.kr/mylibrary/Circulation.ax':
                lib = library_profile()
                lib.username = request.user
                lib.library_id = library_id
                lib.library_password = library_password
                lib.save()
                return render(request, 'library/service.html')
            else:
                raise Http404('you should type right password')

    else:
        form = forms.library_sign_up_form()
        return render(request, 'library/sign_up.html', {'form': form})

def service(request):
    user = library_profile.objects.get(username = request.user)
    user_library_id = user.library_id
    user_library_password = user.library_password

    url_driver = '/Users/YuGeekLab/Desktop/phantomjs-2.1.1-windows/bin/phantomjs'
    try:
        driver = webdriver.PhantomJS(url_driver)
        driver.implicitly_wait(3)
    except:
        raise Http404('some message')

    driver.get('https://khis.khu.ac.kr/identity/Login.ax?url=%2Fmylibrary%2FCirculation.ax')

    driver.find_element_by_name('userID').send_keys(user_library_id)
    driver.find_element_by_name('password').send_keys(user_library_password)

    driver.find_element_by_xpath('//*[@id="loginForm"]/dd[2]/a/span').click()

    driver.get('https://khis.khu.ac.kr/mylibrary/Circulation.ax')

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    books_title = soup.select('#formRenew > table > tbody > tr > td.tleft > a')
    books_date = soup.select('#formRenew > table > tbody > tr > td:nth-of-type(6)')

    books_dic = {}
    for i in range(len(books_title)) :
        books_dic[books_title[i].string] = books_date[i].string.strip()

    books_json = json.dumps(books_dic)

    if user_barrow_books.objects.filter(username = request.user).exists() :
        barrow_books = user_barrow_books.objects.get(username = request.user)
        if barrow_books.info != books_json :
            barrow_books.info = books_json
            barrow_books.save()
        else:
            pass
    else:
        barrow_books = user_barrow_books(username = request.user)
        barrow_books.info = books_json
        barrow_books.save()

    return render(request, 'library/service.html', {})

def save_token(request) :
    token = request.GET.get('token', None)

    if user_token.objects.filter(token = token).exists() :
        data = {
            'is_taken': True
        }
    else :
        save_user_token = user_token(username = request.user)
        save_user_token.token = token
        save_user_token.save()
        data = {
            'is_taken': False
        }

    return JsonResponse(data)

def sign_up(request):
    if request.method == "POST":
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sign_up_ok')
    else:
        form = forms.CreateUserForm()
    return render(request, 'library/sign_up.html', {'form': form})

def sign_up_ok(request) :
    return render(request, 'library/sign_up_ok.html', {})