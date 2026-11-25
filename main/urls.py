from django.urls import path

from main.views import *

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("experience/", show_experience, name="show_experience"),
    path("education/", show_education, name="show_education"),
    path("projects/", show_projects, name="show_projects"),
    path("certifications/", show_certifications, name="show_certifications"),
    path("projects/add/", create_project, name="create_project"),
    path("certifications/add/", create_certification, name="create_certification"),
    path("projects/<uuid:project_id>/edit/", edit_project, name="edit_project"),
    path("certifications/<uuid:certification_id>/edit/", edit_certification, name="edit_certification"),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
    path("certifications/<uuid:certification_id>/delete/", delete_certification, name="delete_certification"),
    path("experience/add/", create_experience, name="create_experience"),
    path("education/add/", create_education, name="create_education"),
    path("experience/<uuid:experience_id>/edit/", edit_experience, name="edit_experience"),
    path("education/<uuid:education_id>/edit/", edit_education, name="edit_education"),
    path("api/experience", get_experience_json, name="get_experience_json"),
    path("api/education", get_education_json, name="get_education_json"),
    path("experience/<uuid:experience_id>/delete/",delete_experience,name="delete_experience"),
    path("education/<uuid:education_id>/delete/",delete_education,name="delete_education"),
    path("experience/<uuid:experience_id>/star/", toggle_star_experience, name="toggle_star_experience",),
    path("education/<uuid:education_id>/star/", toggle_star_education, name="toggle_star_education",),
    path("experience/add-ajax/", create_experience_ajax, name="create_experience_ajax"),
    path("education/add-ajax/", create_education_ajax, name="create_education_ajax"),
]