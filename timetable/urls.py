from django.urls import path
from . import views

app_name = "timetable"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    path(
        "emploi-du-temps/",
        views.timetable_list,
        name="timetable_list"
    ),

    path(
        "emploi-du-temps/grille/",
        views.timetable_grid,
        name="timetable_grid"
    ),

    path(
        "emploi-du-temps/ajouter/",
        views.course_create,
        name="course_create"
    ),

    path(
        "emploi-du-temps/<int:pk>/modifier/",
        views.course_update,
        name="course_update"
    ),

    path(
        "emploi-du-temps/<int:pk>/supprimer/",
        views.course_delete,
        name="course_delete"
    ),

    path(
        "export/excel/",
        views.export_timetable_excel,
        name="export_excel"
    ),

    path(
        "mot-de-passe/",
        views.change_password,
        name="change_password"
    ),

    path(
        "chef/<int:user_id>/reset-password/",
        views.reset_chief_password,
        name="reset_chief_password"
    ),
    path(
        "enseignants/",
        views.teacher_list,
        name="teacher_list"
    ),

    path(
        "enseignants/ajouter/",
        views.teacher_create,
        name="teacher_create"
    ),

    path(
        "enseignants/<int:pk>/modifier/",
        views.teacher_update,
        name="teacher_update"
    ),

    path(
        "enseignants/<int:pk>/supprimer/",
        views.teacher_delete,
        name="teacher_delete"
    ),




    path(
        "departements/",
        views.department_list,
        name="department_list"
    ),

    path(
        "departements/ajouter/",
        views.department_create,
        name="department_create"
    ),

    path(
        "departements/<int:pk>/modifier/",
        views.department_update,
        name="department_update"
    ),

    path(
        "departements/<int:pk>/supprimer/",
        views.department_delete,
        name="department_delete"
    ),



    path(
        "sections/",
        views.section_list,
        name="section_list"
    ),

    path(
        "sections/ajouter/",
        views.section_create,
        name="section_create"
    ),

    path(
        "sections/<int:pk>/modifier/",
        views.section_update,
        name="section_update"
    ),

    path(
        "sections/<int:pk>/supprimer/",
        views.section_delete,
        name="section_delete"
    ),

    path(
        "niveaux/",
        views.level_list,
        name="level_list"
    ),

    path(
        "niveaux/ajouter/",
        views.level_create,
        name="level_create"
    ),

    path(
        "niveaux/<int:pk>/modifier/",
        views.level_update,
        name="level_update"
    ),

    path(
        "niveaux/<int:pk>/supprimer/",
        views.level_delete,
        name="level_delete"
    ),



    path(
        "salles/",
        views.room_list,
        name="room_list"
    ),

    path(
        "salles/ajouter/",
        views.room_create,
        name="room_create"
    ),

    path(
        "salles/<int:pk>/modifier/",
        views.room_update,
        name="room_update"
    ),

    path(
        "salles/<int:pk>/supprimer/",
        views.room_delete,
        name="room_delete"
    ),


    path(
        "matieres/",
        views.subject_list,
        name="subject_list"
    ),

    path(
        "matieres/ajouter/",
        views.subject_create,
        name="subject_create"
    ),

    path(
        "matieres/<int:pk>/modifier/",
        views.subject_update,
        name="subject_update"
    ),

    path(
        "matieres/<int:pk>/supprimer/",
        views.subject_delete,
        name="subject_delete"
    ),



        path(
        "chefs/",
        views.chief_list,
        name="chief_list"
    ),

    path(
        "chefs/ajouter/",
        views.chief_create,
        name="chief_create"
    ),
]