from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView

from superintendent.forms import NewMenuForm, SchoolModelForm
from .models import Menu, School


class StartView(View):

    def get(self, request):
        return render(request, "index.html")


class SchoolUpdate(UpdateView):
    model = School
    template_name = "school.html"
    form_class = SchoolModelForm
    success_message = "Zmieniles rekord"

    def get_success_url(self):
        return reverse_lazy('index')


class NewMenuView(View):

    def get(self, request):
        form = NewMenuForm()
        ctx = {"form": form}
        return render(request, "new_menu.html", ctx)

    def post(self, request):
        form = NewMenuForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            name = form.cleaned_data['name']
            new_menu = Menu(date=date, name=name)
            new_menu.save()

            return redirect('obiady')
        return render(request, 'new_menu.html', {'form': form})


class MenuView(View):
    def get(self, request):
        menu = Menu.objects.all().order_by('date')
        ctx = {"menu": menu}
        return render(request, "menu.html", ctx)


class SchoolView(View):
    def get(self, request):
        school = School.objects.get(pk=1)
        ctx = {"school": school}
        return render(request, "base.html", ctx)