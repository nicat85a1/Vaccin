

# Create your views here.
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from . models import Center , Storage
from . forms import CenterForm, StorageForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

@login_required
def center_list(request):
    centers = Center.objects.all().order_by('-id')
    paginator = Paginator(centers, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}

    return render(request, 'center/center_list.html', context)

@login_required
def center_detail(request,pk):
    center = Center.objects.get(pk=pk)
    context = {

        "center": center
    }
    return render(request, 'center/center_detail.html', context)

@login_required
@permission_required('center.add_center',raise_exception=True)
def create_center(request):
    if request.method == "POST":
        form = CenterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Center Created Successfully")
            return HttpResponseRedirect(reverse("center:list"))
        return render(request, "center/create_center.html", {"form":form})
    context = {
        "form": CenterForm()
    }
    return render(request, "center/create_center.html", context)

@login_required
@permission_required('center.change_center',raise_exception=True)
def update_center(request, pk):
    try:
        center = Center.objects.get(pk=pk)
    except Center.DoesNotExist:
        raise Http404("Center doesnt exist")
    if request.method == "POST":
        form = CenterForm(request.POST, instance=center)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("center:detail", kwargs={"pk":center.pk}))
        return render(request, "center/update_center.html", {"form":form})
    context = {

        "form": CenterForm(instance=center)
    }
    return render(request, "center/update_center.html", context)

@login_required
@permission_required('center.delete_center',raise_exception=True)
def delete_center(request, pk):
    center = Center.objects.get(pk=pk)
    if request.method == "POST":
        center.delete()
        return HttpResponseRedirect(reverse("center:list"))
    context = {

        "center":center
    }

    return render(request, "center/delete_center.html", context)


class StorageList(LoginRequiredMixin,ListView):
    queryset = Storage.objects.all()
    template_name = "storage/storage_list.html"
    ordering = ['-id']
    paginate_by = 2

    def get_queryset(self):
        return super().get_queryset().filter(center_id=self.kwargs['center_id'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['center_id'] = self.kwargs['center_id']
        return context
    

class StorageDetail(LoginRequiredMixin,DetailView):
    model = Storage
    template_name = "storage/storage_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['available_quantity'] = self.object.total_quantity - self.object.booked_quantity

        return context
    
class StorageCreate(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,CreateView):
    model = Storage
    form_class = StorageForm
    template_name = "storage/storage_create.html"
    success_message = 'Storage zad oldu'
    permission_required = ('center.add_storage',)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['center_id'] = self.kwargs['center_id']
        return kwargs
    
    def get_initial(self):
        initial = super().get_initial()
        initial['center'] = Center.objects.get(id=self.kwargs['center_id'])
        return initial
    
    def get_success_url(self):
        return reverse('center:storage_list', kwargs={'center_id':self.kwargs['center_id']})
    
class StorageUpdate(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    model = Storage
    form_class = StorageForm
    template_name = "storage/storage_update.html"
    permission_required = ('center.change_storage',)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['center_id'] = self.get_object().center.id
        return kwargs
    
    def get_success_url(self) -> str:
        return reverse('center:storage_list', kwargs={'center_id':self.get_object().center.id})

class StorageDelete(LoginRequiredMixin, PermissionRequiredMixin,DeleteView):
    model = Storage
    template_name = "storage/storage_delete.html"
    permission_required = ('center.delete_storage',)
    
    def get_success_url(self):
        return reverse('center:storage_list', kwargs={'center_id': self.object.center.id})