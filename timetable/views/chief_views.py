from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from timetable.forms import ChiefUserForm
from timetable.services.permission_service import is_admin


@login_required
@user_passes_test(is_admin)
def chief_list(request):
    chiefs = User.objects.filter(
        managed_section__isnull=False
    ).select_related(
        "managed_section",
        "managed_section__department",
    )

    return render(request, "timetable/chief_list.html", {"chiefs": chiefs})


@login_required
@user_passes_test(is_admin)
def chief_create(request):
    form = ChiefUserForm(request.POST or None, initial={"password": "1234"})

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Chef créé avec succès.")
        return redirect("timetable:chief_list")

    return render(request, "timetable/chief_form.html", {"form": form})