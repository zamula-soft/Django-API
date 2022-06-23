from django.http import HttpResponse


def api(request):
    return HttpResponse("My best API")
