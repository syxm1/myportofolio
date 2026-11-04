from django.urls import path

from main import api_views


app_name = "api"

urlpatterns = [
    path("educations/", api_views.education_list, name="education-list"),
    path("experiences/", api_views.experience_list, name="experience-list"),
    path("education/", api_views.education_list),
    path("experience/", api_views.experience_list),
]
