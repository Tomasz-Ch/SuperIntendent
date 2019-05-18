from django.shortcuts import render, redirect
from django.views import View

from superintendent.forms import MenuForm


class StartView(View):

    def get(self, request):
        return render(request, "index.html")


class MenuView(View):

    def get(self, request):
        form = MenuForm()
        ctx = {"form": form}
        return render(request, "menu.html", ctx)

    def post(self, request):
        form = MenuForm(request.POST)
        if form.is_valid():
            # form valid start

            # form valid stop
            return redirect('menu')
        return render(request, 'add_group.html', {'form': form})
