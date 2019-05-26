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
    UsedForm, SearchProductForm, ContactForm, DateForm
from .models import Menu, School, Products, Inventory, MealNumber


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


from decimal import Decimal


class ReportView(View):
    def get(self, request):
        print(request.GET)
        start_date = request.GET.get('date_from', '2019-05-20')
        end_date = request.GET.get('date_to', start_date)
        print(start_date, end_date)

        product_id_list = [i.product_id for i in Inventory.objects.filter(operation_date__gte=start_date). \
            filter(operation_date__lte=end_date).filter(operation_type__exact=2).distinct()]
        product_id_set = set(product_id_list)
        products = Products.objects.filter(id__in=product_id_set)

        meals = MealNumber.objects.all().filter(meal_date__gte=start_date).\
            filter(meal_date__lte=end_date)
        meal_num = 0
        for m in meals:
            meal_num += m.meal_number


        rv = []
        sum_calories = 0
        sum_proteins = 0
        sum_fat = 0
        sum_carbo = 0
        sum_calcium = 0
        sum_iron = 0
        sum_vit_A = 0
        sum_vit_B1 = 0
        sum_vit_B2 = 0
        sum_vit_C = 0
        quant_total = 0
        value_total = 0

        for product in products:
            product_id = product.id
            events = Inventory.objects.all().filter(operation_type__exact=2). \
                filter(operation_date__gte=start_date).filter(operation_date__lte=end_date). \
                filter(product_id=product_id)

            value = Decimal(0)
            quant = Decimal(0)

            for e in events:
                value = value + Decimal(e.quantity) * e.price
                quant = quant + Decimal(e.quantity)
                quant_total += e.quantity
                value_total += Decimal(e.quantity) * e.price
                sum_calories += e.quantity * int(Products.objects.get(id=e.product_id).calories * 1000 / 100 / meal_num)
                sum_proteins += e.quantity * Products.objects.get(pk=e.product_id).protein * 1000 / 100 / meal_num
                sum_fat += e.quantity * Products.objects.get(pk=e.product_id).fat * 1000 / 100 / meal_num
                sum_carbo += e.quantity * Products.objects.get(pk=e.product_id).carbo * 1000 / 100 / meal_num
                sum_calcium += e.quantity * Products.objects.get(pk=e.product_id).calcium * 1000 / 100 / meal_num
                sum_iron += e.quantity * Products.objects.get(pk=e.product_id).iron * 1000 / 100 / meal_num
                sum_vit_A += e.quantity * Products.objects.get(pk=e.product_id).vit_A * 1000 / 100 / meal_num
                sum_vit_B1 += e.quantity * Products.objects.get(pk=e.product_id).vit_B1 * 1000 / 100 / meal_num
                sum_vit_B2 += e.quantity * Products.objects.get(pk=e.product_id).vit_B2 * 1000 / 100 / meal_num
                sum_vit_C += e.quantity * Products.objects.get(pk=e.product_id).vit_C * 1000 / 100 / meal_num
            rv.append({
                "value": value,
                "product": product,
                "quant": quant,
            })

        cal_norm = 900
        prot_norm = 28
        fat_norm = 27
        carbo_norm = 139
        calcium_norm = 0.3
        iron_norm = 4.3
        vit_A_norm = 1520
        vit_B1_norm = 0.5
        vit_B2_norm = 0.6
        vit_C_norm = 26
        cal_real = int((sum_calories / cal_norm) * 100)
        prot_real = int((sum_proteins / prot_norm) * 100)
        fat_real = int((sum_fat / fat_norm) * 100)
        carbo_real = int((sum_carbo / carbo_norm) * 100)
        calcium_real = int((sum_calcium / calcium_norm) * 100)
        iron_real = int((sum_iron / iron_norm) * 100)
        vit_A_real = int((sum_vit_A / vit_A_norm) * 100)
        vit_B1_real = int((sum_vit_B1 / vit_B1_norm) * 100)
        vit_B2_real = int((sum_vit_B2 / vit_B2_norm) * 100)
        vit_C_real = int((sum_vit_C / vit_C_norm) * 100)

        ctx = {"result": rv,
               'quant_total': quant_total,
               'value_total': value_total,
               'calories': sum_calories,
               'proteins': sum_proteins,
               'fat': sum_fat,
               'carbo': sum_carbo,
               'calcium': sum_calcium,
               'iron': sum_iron,
               'vit_A': sum_vit_A,
               'vit_B1': sum_vit_B1,
               'vit_B2': round(sum_vit_B2, 1),
               'vit_C': sum_vit_C,
               'cal_real': cal_real,
               'prot_real': prot_real,
               'fat_real': fat_real,
               'carbo_real': carbo_real,
               'calcium_real': calcium_real,
               'iron_real': iron_real,
               'vit_A_real': vit_A_real,
               'vit_B1_real': vit_B1_real,
               'vit_B2_real': vit_B2_real,
               'vit_C_real': vit_C_real}
        return render(request, "report.html", ctx)

    def post(self, request):
        form = DateForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['date_from']
            end_date = form.cleaned_data['date_to']

            return redirect(reverse_lazy('report') + '?' + f'date_from={start_date}&date_to={end_date}')
        ctx = {'form': form}
        return render(request, 'report.html', ctx)


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


class InvReportView(View):
    def get(self, request):
        print(request.GET)
        start_date = request.GET.get('date_from', '2019-05-20')
        end_date = request.GET.get('date_to', start_date)
        print(start_date, end_date)

        product_id_list = [i.product_id for i in Inventory.objects.filter(operation_date__gte=start_date). \
            filter(operation_date__lte=end_date).filter(operation_type__exact=2).distinct()]
        product_id_set = set(product_id_list)
        products = Products.objects.filter(id__in=product_id_set)

        rv = []

        quant_total_in = 0
        value_total_in = 0
        quant_total_out = 0
        value_total_out = 0
        for product in products:
            product_id = product.id
            events_out = Inventory.objects.all().filter(operation_type__exact=2). \
                filter(operation_date__gte=start_date).filter(operation_date__lte=end_date). \
                filter(product_id=product_id)
            events_in = Inventory.objects.all().filter(operation_type__exact=1). \
                filter(operation_date__gte=start_date).filter(operation_date__lte=end_date). \
                filter(product_id=product_id)

            value_in = Decimal(0)
            quant_in = Decimal(0)
            for e in events_in:
                value_in = value_in + Decimal(e.quantity) * e.price
                quant_in = quant_in + Decimal(e.quantity)
                quant_total_in += e.quantity
                value_total_in += Decimal(e.quantity) * e.price

            value_out = Decimal(0)
            quant_out = Decimal(0)
            for e in events_out:
                value_out = value_out + Decimal(e.quantity) * e.price
                quant_out = quant_out + Decimal(e.quantity)
                quant_total_out += e.quantity
                value_total_out += Decimal(e.quantity) * e.price

            quant_saldo = quant_in - quant_out
            value_saldo = value_in - value_out
            quant_total_saldo = quant_total_in - quant_total_out
            value_total_saldo = value_total_in - value_total_out


            rv.append({
                "quant_in": quant_in,
                "value_in": value_in,
                "quant_out": quant_out,
                "value_out": value_out,
                "product": product,
                "quant_saldo": quant_saldo,
                "value_saldo": value_saldo
            })

        ctx = {"result": rv,
               'quant_total_in': quant_total_in,
               'value_total_in': value_total_in,
               'quant_total_out': quant_total_out,
               'value_total_out': value_total_out,
               'quant_total_saldo': quant_total_saldo,
               'value_total_saldo': value_total_saldo,
               }

        return render(request, "inv_report.html", ctx)

    def post(self, request):
        form = DateForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['date_from']
            end_date = form.cleaned_data['date_to']

            return redirect(reverse_lazy('inv-report') + '?' + f'date_from={start_date}&date_to={end_date}')
        ctx = {'form': form}
        return render(request, 'inv_report.html', ctx)
