from django.shortcuts import render

from main.models import Experience
from main.models import Education

def show_main(request):
    context = {
        "name": "Hisyam",
        "npm": "2506614763",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Sophomore year Computer Science Student at University of Indonesia. Currently focusing on Data Science and ML/AI Engineering."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Hisyam",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_education(request):
    context = {
        "name": "Hisyam",
        "education_list": Education.objects.all(),
    }
    return render(request, "education.html", context)