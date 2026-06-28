from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from timetable.forms import RoomForm
from timetable.models import Room
from timetable.services.permission_service import is_admin


@login_required
def room_list(request):
    rooms = Room.objects.all().order_by("name")
    return render(request, "timetable/room_list.html", {"rooms": rooms})


@login_required
@user_passes_test(is_admin)
def room_create(request):
    form = RoomForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Salle ajoutée avec succès.")
        return redirect("timetable:room_list")

    return render(request, "timetable/room_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def room_update(request, pk):
    room = get_object_or_404(Room, pk=pk)
    form = RoomForm(request.POST or None, instance=room)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Salle modifiée.")
        return redirect("timetable:room_list")

    return render(request, "timetable/room_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)

    if request.method == "POST":
        room.delete()
        messages.success(request, "Salle supprimée.")
        return redirect("timetable:room_list")

    return render(request, "timetable/confirm_delete.html", {"object": room})