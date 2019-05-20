from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView

from superintendent.forms import NewMenuForm, SchoolModelForm, AddProductFormModel
from .models import Menu, School, Products


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


class AllProductsView(View):

    def get(self, request):
        prod_list = Products.objects.all().order_by('name')
        ctx = {'prod_list': prod_list}
        return render(request, "all_products.html", ctx)


class AddProductView(View):
    def get(self, request):
        form = AddProductFormModel
        ctx = {"form": form}
        return render(request, "add_product.html", ctx)

    def post(self, request):
        form = AddProductFormModel(request.POST)
        if form.is_valid():
            # form valid start
            name = form.cleaned_data['name']
            unit = form.cleaned_data['unit']
            calories = form.cleaned_data['calories']
            protein = form.cleaned_data['protein']
            fat = form.cleaned_data['fat']
            carbo = form.cleaned_data['carbo']
            calcium = form.cleaned_data['calcium']
            iron = form.cleaned_data['iron']
            vit_A = form.cleaned_data['vit_A']
            vit_B1 = form.cleaned_data['vit_B1']
            vit_B2 = form.cleaned_data['vit_B2']
            vit_C = form.cleaned_data['vit_C']
            group = form.cleaned_data['group']

            new_product = Products(name=name,
                                   unit=unit,
                                   calories=calories,
                                   protein=protein,
                                   fat=fat,
                                   carbo=carbo,
                                   calcium=calcium,
                                   iron=iron,
                                   vit_A=vit_A,
                                   vit_B1=vit_B1,
                                   vit_B2=vit_B2,
                                   vit_C=vit_C,
                                   group=group)
            new_product.save()
            # form valid stop
            return redirect('all-products')
        # Wyświetl niepoprawny formularz z błędami
        return render(request, 'add_product.html', {'form': form})
