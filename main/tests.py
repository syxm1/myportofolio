from datetime import date

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience
from main.models import Education

class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
            started_at=date(2024, 1, 1),
        )
        self.education = Education.objects.create(
            institution="Universitas Indonesia",
            program="S1 Ilmu Komputer",
            description="Fokus pada Data Science dan ML/AI Engineering.",
            level="undergraduate",
            started_at=date(2023, 8, 1),
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, reverse("api:experience-list"))
        self.assertContains(response, 'id="grid"')
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')
        api_response = self.client.get(reverse("api:experience-list"))
        self.assertEqual(api_response.json()[0]["title"], self.experience.title)
        self.assertEqual(api_response.json()[0]["description"], self.experience.description)

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan atau ditemukan.")
        self.assertEqual(self.client.get(reverse("api:experience-list")).json(), [])

    def test_completed_experience(self):
        self.experience.ended_at = timezone.localdate()
        self.experience.save()

        self.assertFalse(self.experience.is_ongoing)
        response = self.client.get(reverse("api:experience-detail", args=[self.experience.id]))
        self.assertEqual(response.json()["ended_at"], timezone.localdate().isoformat())

    def test_education_url_is_accessible(self):
        response = self.client.get(reverse("main:show_education"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_education_model(self):
        self.assertEqual(str(self.education), "Universitas Indonesia")
        self.assertEqual(self.education.level, "undergraduate")
        self.assertTrue(self.education.is_ongoing)

    def test_education_page(self):
        response = self.client.get(reverse("main:show_education"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")
        self.assertContains(response, reverse("api:education-list"))
        self.assertContains(response, 'id="grid"')
        self.assertContains(response, "Undergraduate")
        self.assertContains(response, "Sedang berlangsung")
        api_response = self.client.get(reverse("api:education-list"))
        self.assertEqual(api_response.json()[0]["institution"], self.education.institution)
        self.assertEqual(api_response.json()[0]["program"], self.education.program)
        self.assertEqual(api_response.json()[0]["description"], self.education.description)

    def test_empty_education_page(self):
        Education.objects.all().delete()
        response = self.client.get(reverse("main:show_education"))

        self.assertContains(response, "Belum ada riwayat pendidikan yang ditambahkan atau ditemukan.")
        self.assertEqual(self.client.get(reverse("api:education-list")).json(), [])

    def test_completed_education(self):
        self.education.ended_at = timezone.localdate()
        self.education.save()

        self.assertFalse(self.education.is_ongoing)
        response = self.client.get(reverse("api:education-detail", args=[self.education.id]))
        self.assertEqual(response.json()["ended_at"], timezone.localdate().isoformat())
