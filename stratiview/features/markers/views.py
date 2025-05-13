from django.shortcuts import render


def add_marker(request):
    key = request.GET.get('key')
    account = request.GET.get('account')

    print("Key:", key)
    print("Account:", account)