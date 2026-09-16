from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import Experience, Education
from main.forms import ExperienceForm, EducationForm

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

def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New experience has been successfully added!")
        return redirect("main:show_experience")

    context = {
        "name": "Hisyam",
        "form": form,
    }
    return render(request, "experience_form.html", context)

def create_education(request):
    form = EducationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New education has been successfully added!")
        return redirect("main:show_education")

    context = {
        "name": "Hisyam",
        "form": form,
    }
    return render(request, "education_form.html", context)