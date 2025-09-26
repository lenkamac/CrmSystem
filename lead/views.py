from django.shortcuts import render

# Create your views here.
def lead(request):
    return render(request, 'lead/lead_list.html')