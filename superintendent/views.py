from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView

from superintendent.forms import NewMenuForm, SchoolModelForm, AddProductFormModel, ProductModelForm, InvoiceModelForm, \
    UsedForm, SearchProductForm, ContactForm
from .models import Menu, School, Products, Inventory


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


class AddProductView(LoginRequiredMixin, View):
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


class ModifyProductUpdate(LoginRequiredMixin, UpdateView):
    model = Products
    template_name = "edit_product.html"
    form_class = ProductModelForm
    success_message = "Zmieniles rekord"

    def get_success_url(self):
        return reverse_lazy('all-products')


class ProductView(View):
    def get(self, request, product_id):
        product = Products.objects.get(pk=product_id)
        ctx = {
            "product": product,
        }
        return render(request, "product.html", ctx)


class InvoiceView(View):
    def get(self, request):
        form = InvoiceModelForm
        ctx = {"form": form}
        return render(request, "invoice.html", ctx)

    def post(self, request):
        form = InvoiceModelForm(request.POST)
        if form.is_valid():
            # form valid start
            operation_date = form.cleaned_data['operation_date']
            operation_type = form.cleaned_data['operation_type']
            quantity = form.cleaned_data['quantity']
            price = form.cleaned_data['price']
            product = form.cleaned_data['product']

            new_item = Inventory(operation_date=operation_date,
                                 operation_type=operation_type,
                                 quantity=quantity,
                                 price=price,
                                 product=product
                                 )
            new_item.save()
            # form valid stop
            return redirect('index')
        return render(request, 'invoice.html', {'form': form})


class UsedView(View):

    def get(self, request):
        form = UsedForm()
        ctx = {"form": form}
        return render(request, "used.html", ctx)

    def post(self, request):
        form = UsedForm(request.POST)
        if form.is_valid():
            operation_date = form.cleaned_data['operation_date']
            operation_type = form.cleaned_data['operation_type']
            quantity = form.cleaned_data['quantity']
            price = form.cleaned_data['price']
            current_product = form.cleaned_data['product']
            product = Products.objects.get(name=current_product)
            new_item = Inventory(operation_date=operation_date,
                                 operation_type=operation_type,
                                 quantity=quantity,
                                 price=price,
                                 product=product
                                 )
            new_item.save()

            return redirect('obiady')
        return render(request, 'used.html', {'form': form})


class ReportView(View):
    def get(self, request):
        name = Products.objects.filter(inventory__operation_type='2').distinct().filter(
            inventory__operation_date='2019-05-20')
        quant = Inventory.quantity
        ctx = {"result": name, "quantity": quant}
        return render(request, "report.html", ctx)

    # def post(self, request):
    #     form = ReportForm(request.POST)
    #     if form.is_valid():
    #         operation_date = form.cleaned_data['name']
    #         result = Products.objects.filter(name__icontains=operation_date)
    #         empty_form = ReportForm()
    #         ctx = {
    #             "result": result,
    #             'form': empty_form,
    #         }
    #     return render(request, "report.html", ctx)


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        ctx = {'form': form}
        return render(request, 'login.html', ctx)

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            return redirect('index')
        ctx = {'form': form}
        return render(request, 'login.html', ctx)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class SearchProductView(View):
    def get(self, request):
        form = SearchProductForm()
        ctx = {'form': form}
        return render(request, "product_search.html", ctx)

    def post(self, request):
        form = SearchProductForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            product_result = Products.objects.filter(name__icontains=name)
            empty_form = SearchProductForm()
            ctx = {
                'product_result': product_result,
                'form': empty_form,
            }
        return render(request, "product_search.html", ctx)


class AddUserView(View):
    def get(self, request):
        form = UserCreationForm()
        ctx = {'form': form}
        return render(request, 'create_user.html', ctx)

    def post(self, request):
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('list-users')
        ctx = {'form': form}
        return render(request, 'create_user.html', ctx)


class ListUsersView(LoginRequiredMixin, View):
    def get(self, request):
        users = User.objects.all()
        ctx = {'users': users}
        return render(request, "list_users.html", ctx)


class ResetPasswordView(View):
    def get(self, request):
        form = PasswordResetForm()
        ctx = {'form': form}
        return render(request, 'reset_password.html', ctx)

    def post(self, request):
        form = PasswordResetForm(data=request.POST)
        if form.is_valid():
            form.save(request=request, from_email='blabla@blabla.com')
            return redirect('index')
        ctx = {'form': form}
        return render(request, 'reset_password.html', ctx)


def emailView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "email.html", {'form': form})


def successView(request):
    return HttpResponse('Success! Thank you for your message.')
