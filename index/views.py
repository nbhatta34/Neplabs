from django.shortcuts import render

# Create your views here.
def index_page(request):
    context = {}
    return render(request, 'index/index.html', context)

def user_dashboard(request):
    context = {}
    return render(request, 'index/userDash.html', context)
