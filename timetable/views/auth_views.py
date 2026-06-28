from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from timetable.services.permission_service import is_admin


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            messages.success(request, "Mot de passe modifié.")
            return redirect("timetable:dashboard")
    else:
        form = PasswordChangeForm(request.user)

    return render(
        request,
        "timetable/change_password.html",
        {"form": form},
    )


@login_required
@user_passes_test(is_admin)
def reset_chief_password(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    user.set_password("1234")
    user.save()

    messages.success(
        request,
        f"Mot de passe de {user.username} réinitialisé à 1234.",
    )

    return redirect("timetable:chief_list")