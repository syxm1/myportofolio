from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from main import api_views


app_name = "api"

urlpatterns = [
    path("auth/token/", obtain_auth_token, name="api_token_auth"),
    path("auth/logout/", api_views.api_logout, name="api_logout"),
    path("token/", obtain_auth_token, name="token"),
    path("projects/", api_views.project_list, name="project-list"),
    path("projects/<uuid:project_id>/", api_views.project_detail, name="project-detail"),
    path("projects/<uuid:project_id>/star/", api_views.project_star, name="project-star"),
    path("certifications/", api_views.certification_list, name="certification-list"),
    path("certifications/<uuid:certification_id>/", api_views.certification_detail, name="certification-detail"),
    path("certifications/<uuid:certification_id>/star/", api_views.certification_star, name="certification-star"),
    path("educations/", api_views.education_list, name="education-list"),
    path("educations/<uuid:education_id>/", api_views.education_detail, name="education-detail"),
    path("educations/<uuid:education_id>/star/", api_views.education_star, name="education-star"),
    path("experiences/", api_views.experience_list, name="experience-list"),
    path("experiences/<uuid:experience_id>/", api_views.experience_detail, name="experience-detail"),
    path("experiences/<uuid:experience_id>/star/", api_views.experience_star, name="experience-star"),
    path("education/", api_views.education_list),
    path("education/<uuid:education_id>/", api_views.education_detail),
    path("education/<uuid:education_id>/star/", api_views.education_star),
    path("experience/", api_views.experience_list),
    path("experience/<uuid:experience_id>/", api_views.experience_detail),
    path("experience/<uuid:experience_id>/star/", api_views.experience_star),
]
