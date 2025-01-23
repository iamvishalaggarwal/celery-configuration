from django.http.response import HttpResponse
from .tasks import task_func


# Create your views here.
def test(request):
    task_func.delay()
    return HttpResponse("Done")
