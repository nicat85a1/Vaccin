from typing import Any
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from campagin.models import Campagin
from vaccination.models import Vaccination

class CampaginViewsList(LoginRequiredMixin, generic.ListView):
    model = Campagin
    template_name = "campagin/campagin_list.html"
    paginate_by = 2
    ordering = ['-id']

class CampaginDetailView(LoginRequiredMixin, generic.DetailView):
    model = Campagin
    template_name = "campagin/campagin_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["registration"] = Vaccination.objects.filter(campaing=self.kwargs['pk']).count()
        return context
