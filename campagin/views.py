from typing import Any
from django.shortcuts import render

# Create your views here.
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from campagin.models import Campaing
from vaccination.models import Vaccination

class CampaginViewsList(LoginRequiredMixin, generic.ListView):
    model = Campaing
    template_name = "campagin/campagin_list.html"
    paginate_by = 2
    ordering = ['-id']

class CampaginDetailView(LoginRequiredMixin, generic.DetailView):
    model = Campaing
    template_name = "campagin/campagin_detail.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["registration"] = Vaccination.objects.filter(campaing = self.kwargs("pk")).count()
        return context