from superintendent.models import School


def my_cp(request):
    name = School.objects.get(pk=1).name
    email = School.objects.get(pk=1).email
    ctx = {"name": name, "email": email}
    return ctx
