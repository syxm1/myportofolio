from django.core.exceptions import ValidationError
from django.forms import DateInput, ModelForm, TextInput, Textarea, URLInput, Select
from django.utils.html import strip_tags

from main.models import Certification, Education, Experience, Project


def plain_text(value):
    """Buang tag HTML lalu rapikan spasi di awal/akhir."""
    return strip_tags(value or "").strip()


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience

        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at",
        ]

        labels = {
            "title": "Title",
            "description": "Description",
            "category": "Category",
            "thumbnail": "Thumbnail Link",
            "started_at": "Start Date",
            "ended_at": "End Date",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "e.g. Competitive Programming Teacher",
                }
            ),
            "description": Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "What did you do in this role?",
                }
            ),
            "category": Select(),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://...",
                }
            ),
            "started_at": DateInput(attrs={"type": "date"}),
            "ended_at": DateInput(attrs={"type": "date"}),
        }

    def clean_title(self):
        title = plain_text(self.cleaned_data["title"])
        if not title:
            raise ValidationError("Title tidak boleh hanya berisi tag HTML.")
        return title

    def clean_description(self):
        return plain_text(self.cleaned_data["description"])


class EducationForm(ModelForm):
    class Meta:
        model = Education

        fields = [
            "institution",
            "program",
            "level",
            "description",
            "thumbnail",
            "started_at",
            "ended_at",
        ]

        labels = {
            "institution": "Institution Name",
            "program": "Program",
            "level": "Level",
            "description": "Description",
            "thumbnail": "Thumbnail Link",
            "started_at": "Start Date",
            "ended_at": "End Date",
        }

        widgets = {
            "institution": TextInput(
                attrs={
                    "placeholder": "e.g. University of Indonesia",
                }
            ),
            "program": TextInput(
                attrs={
                    "placeholder": "e.g. Computer Science",
                }
            ),
            "level": Select(),
            "description": Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "What did you focus on or do here?",
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://...",
                }
            ),
            "started_at": DateInput(attrs={"type": "date"}),
            "ended_at": DateInput(attrs={"type": "date"}),
        }

    def clean_institution(self):
        institution = plain_text(self.cleaned_data["institution"])
        if not institution:
            raise ValidationError("Nama institusi tidak boleh hanya berisi tag HTML.")
        return institution

    def clean_program(self):
        program = plain_text(self.cleaned_data["program"])
        if self.fields["program"].required and not program:
            raise ValidationError("Program tidak boleh hanya berisi tag HTML.")
        return program

    def clean_description(self):
        return plain_text(self.cleaned_data["description"])


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title", "description", "category", "tech_stack",
            "project_url", "project_image_url",
        ]
        labels = {
            "title": "Project title",
            "description": "Description",
            "category": "Category",
            "tech_stack": "Tech stack",
            "project_url": "Project URL",
            "project_image_url": "Image URL (optional)",
        }
        widgets = {
            "description": Textarea(attrs={"rows": 4}),
            "category": Select(),
            "project_url": URLInput(attrs={"placeholder": "https://..."}),
            "project_image_url": URLInput(attrs={"placeholder": "https://..."}),
        }

    def clean_title(self):
        title = plain_text(self.cleaned_data["title"])
        if not title:
            raise ValidationError("Project title cannot be empty.")
        return title

    def clean_description(self):
        description = plain_text(self.cleaned_data["description"])
        if not description:
            raise ValidationError("Description cannot be empty.")
        return description

    def clean_tech_stack(self):
        tech_stack = plain_text(self.cleaned_data["tech_stack"])
        if not tech_stack:
            raise ValidationError("Tech stack cannot be empty.")
        return tech_stack


class CertificationForm(ModelForm):
    class Meta:
        model = Certification
        fields = ["name", "issuer", "credential_id", "credential_url", "issue_date"]
        labels = {
            "name": "Certification name",
            "issuer": "Issuer",
            "credential_id": "Credential ID",
            "credential_url": "Credential URL (optional)",
            "issue_date": "Issue date",
        }
        widgets = {
            "credential_url": URLInput(attrs={"placeholder": "https://..."}),
            "issue_date": DateInput(attrs={"type": "date"}),
        }

    def clean_name(self):
        name = plain_text(self.cleaned_data["name"])
        if not name:
            raise ValidationError("Certification name cannot be empty.")
        return name

    def clean_issuer(self):
        issuer = plain_text(self.cleaned_data["issuer"])
        if not issuer:
            raise ValidationError("Issuer cannot be empty.")
        return issuer

    def clean_credential_id(self):
        credential_id = plain_text(self.cleaned_data["credential_id"])
        if not credential_id:
            raise ValidationError("Credential ID cannot be empty.")
        return credential_id
