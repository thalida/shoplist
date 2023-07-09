from django.shortcuts import render

from .models import List


def index(request):
    lists = List.objects.order_by("-updated_at")
    context = {"lists": lists}
    return render(request, "shop/index.html", context)

# def list_detail(request, list_id):
#     return HttpResponse("You're looking at list %s." % list_id)
