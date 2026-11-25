from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import (
    api_view, permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Certification, Education, Experience, Project
from main.permissions import IsPortfolioOwnerOrEditorOrReadOnly
from main.serializers import (
    CertificationSerializer, EducationSerializer, ExperienceSerializer, ProjectSerializer,
)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_logout(request):
    if request.auth is not None:
        request.auth.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "HEAD", "POST"])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def education_list(request):
    if request.method in ("GET", "HEAD"):
        educations = Education.objects.prefetch_related("starred_by").order_by(
            "institution", "id"
        )
        query = request.query_params.get("query", "").strip()
        if query:
            educations = educations.filter(institution__icontains=query)
        serializer = EducationSerializer(
            educations, many=True, context={"request": request},
        )
        return Response(serializer.data)

    serializer = EducationSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "POST"])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_list(request):
    if request.method in ("GET", "HEAD"):
        experiences = Experience.objects.prefetch_related("starred_by").order_by(
            "title", "id"
        )
        query = request.query_params.get("query", "").strip()
        if query:
            experiences = experiences.filter(title__icontains=query)
        serializer = ExperienceSerializer(
            experiences, many=True, context={"request": request},
        )
        return Response(serializer.data)

    serializer = ExperienceSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def education_detail(request, education_id):
    education = get_object_or_404(
        Education.objects.prefetch_related("starred_by"), pk=education_id,
    )
    if request.method in ("GET", "HEAD"):
        serializer = EducationSerializer(education, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        education.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = EducationSerializer(
        education, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_detail(request, experience_id):
    experience = get_object_or_404(
        Experience.objects.prefetch_related("starred_by"), pk=experience_id,
    )
    if request.method in ("GET", "HEAD"):
        serializer = ExperienceSerializer(experience, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ExperienceSerializer(
        experience, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def education_star(request, education_id):
    education = get_object_or_404(Education, pk=education_id)
    if education.starred_by.filter(pk=request.user.pk).exists():
        education.starred_by.remove(request.user)
    else:
        education.starred_by.add(request.user)
    serializer = EducationSerializer(education, context={"request": request})
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def experience_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    if experience.starred_by.filter(pk=request.user.pk).exists():
        experience.starred_by.remove(request.user)
    else:
        experience.starred_by.add(request.user)
    serializer = ExperienceSerializer(experience, context={"request": request})
    return Response(serializer.data)



def _resource_list(request, model, serializer_class, search_field):
    if request.method in ("GET", "HEAD"):
        records = model.objects.prefetch_related("starred_by").order_by(search_field, "id")
        query = request.query_params.get("query", "").strip()
        if query:
            records = records.filter(**{f"{search_field}__icontains": query})
        return Response(serializer_class(
            records, many=True, context={"request": request},
        ).data)
    serializer = serializer_class(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def _resource_detail(request, model, serializer_class, record_id):
    record = get_object_or_404(model.objects.prefetch_related("starred_by"), pk=record_id)
    if request.method in ("GET", "HEAD"):
        return Response(serializer_class(record, context={"request": request}).data)
    if request.method == "DELETE":
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = serializer_class(
        record, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


def _resource_star(request, model, serializer_class, record_id):
    record = get_object_or_404(model, pk=record_id)
    if record.starred_by.filter(pk=request.user.pk).exists():
        record.starred_by.remove(request.user)
    else:
        record.starred_by.add(request.user)
    return Response(serializer_class(record, context={"request": request}).data)


@api_view(["GET", "HEAD", "POST"])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def project_list(request):
    return _resource_list(request, Project, ProjectSerializer, "title")


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def project_detail(request, project_id):
    return _resource_detail(request, Project, ProjectSerializer, project_id)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def project_star(request, project_id):
    return _resource_star(request, Project, ProjectSerializer, project_id)


@api_view(["GET", "HEAD", "POST"])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def certification_list(request):
    return _resource_list(request, Certification, CertificationSerializer, "name")


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def certification_detail(request, certification_id):
    return _resource_detail(request, Certification, CertificationSerializer, certification_id)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def certification_star(request, certification_id):
    return _resource_star(request, Certification, CertificationSerializer, certification_id)
