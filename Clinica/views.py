from django.shortcuts import render

from django.views import generic
# Create your views here.


class Index(generic.TemplateView):
    template_name = "pages/index.html"

# Logout temporal para que no mande error
class Logout(generic.TemplateView):
    template_name = "pages/index.html"
