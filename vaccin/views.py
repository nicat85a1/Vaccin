from django.shortcuts import render, redirect
from django.views import View
from vaccin.models import Vaccine
from vaccin.forms import VaccineForm
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required , permission_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name="dispatch")
class VaccineList(View):
    def get(self, request):
        vaccine_list = Vaccine.objects.all()
        context = {
            "vaccine_list": vaccine_list
        }
        return render(request, "vaccine/vaccine_list.html", context)

@method_decorator(login_required, name="dispatch")
class VaccineDetail(View):
    def get(self, request, pk):
        vaccine_detail = get_object_or_404(Vaccine, pk=pk)
        context = {
            "vaccine_detail": vaccine_detail
        }
        return render(request, "vaccine/vaccine_detail.html", context)

@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required('vaccin.add_vaccin',raise_exception=True), name="dispatch")
class VaccineCreate(View):
    form_class = VaccineForm
    template_name = "vaccine/create_vaccine.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vaccin:list')
        return render(request, self.template_name, {'form': form})

@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required('vaccin.change_vaccin',raise_exception=True), name="dispatch")
class VaccineUpdate(View):
    form_class = VaccineForm
    template_name = "vaccine/update_vaccine.html"

    def get_object(self, pk):
        try:
            return Vaccine.objects.get(pk=pk)
        except Vaccine.DoesNotExist:
            raise Http404("Vaccine does not exist")

    def get(self, request, pk):
        vaccine = self.get_object(pk)
        form = self.form_class(instance=vaccine)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        vaccine = self.get_object(pk)
        form = self.form_class(request.POST, instance=vaccine)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("vaccin:detail", kwargs={"pk": vaccine.pk}))
        return render(request, self.template_name, {'form': form})

@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required('vaccin.delete_vaccin',raise_exception=True), name="dispatch")
class VaccineDelete(View):
    template_name = "vaccine/delete_vaccine.html"

    def get_object(self, pk):
        try:
            return Vaccine.objects.get(pk=pk)
        except Vaccine.DoesNotExist:
            raise Http404("Vaccine does not exist")

    def get(self, request, pk):
        vaccine = self.get_object(pk)
        return render(request, self.template_name, {'vaccine': vaccine})

    def post(self, request, pk):
        vaccine = self.get_object(pk)
        vaccine.delete()
        return HttpResponseRedirect(reverse("vaccin:list"))