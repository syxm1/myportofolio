from django.shortcuts import render

from main.models import Experience


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
        "name": "Burhan",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)