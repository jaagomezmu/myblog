from django.http import HttpResponse

def index(request):
    return HttpResponse("This will be the blog index, work in progress")
