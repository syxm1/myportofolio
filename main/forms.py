from django.forms import DateInput, ModelForm, TextInput, Textarea, URLInput, Select

from main.models import Education, Experience


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