from datetime import date

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth.models import Group, User
from main.models import Certification, Education, Experience, Project

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



class PortfolioCollectionPageTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Portfolio App", description="A sample project",
            category="Web Development", tech_stack="Django, Flutter",
            project_url="https://example.com/project",
        )
        self.certification = Certification.objects.create(
            name="Cloud Certificate", issuer="Example Academy",
            credential_id="CERT-42", issue_date=date(2025, 2, 3),
        )
        self.owner = User.objects.create_superuser(
            username="owner-pages", password="test-password", email="owner@example.com",
        )
        self.editor = User.objects.create_user(
            username="editor-pages", password="test-password",
        )
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.visitor = User.objects.create_user(
            username="visitor-pages", password="test-password",
        )

    def test_public_pages_and_navbar(self):
        home = self.client.get(reverse("main:show_main"))
        self.assertContains(home, reverse("main:show_projects"))
        self.assertContains(home, reverse("main:show_certifications"))
        projects = self.client.get(reverse("main:show_projects"))
        certifications = self.client.get(reverse("main:show_certifications"))
        self.assertTemplateUsed(projects, "portfolio_collection.html")
        self.assertTemplateUsed(certifications, "portfolio_collection.html")
        self.assertContains(projects, self.project.title)
        self.assertContains(projects, self.project.tech_stack)
        self.assertContains(certifications, self.certification.name)
        self.assertContains(certifications, self.certification.credential_id)
        self.assertNotContains(projects, "Modify Project")

    def test_search_and_empty_state(self):
        projects = self.client.get(reverse("main:show_projects"), {"query": "missing"})
        certifications = self.client.get(
            reverse("main:show_certifications"), {"query": "Academy"},
        )
        self.assertContains(projects, "Belum ada project")
        self.assertNotContains(projects, self.project.title)
        self.assertNotContains(certifications, self.certification.name)
        self.assertContains(
            self.client.get(reverse("main:show_certifications"), {"query": "Cloud"}),
            self.certification.name,
        )

    def test_owner_can_create_and_delete_both_records(self):
        self.client.force_login(self.owner)
        project_response = self.client.post(reverse("main:create_project"), {
            "title": "Another Project", "description": "A new project",
            "category": "Mobile Development", "tech_stack": "Flutter",
            "project_url": "https://example.com/another", "project_image_url": "",
        })
        certificate_response = self.client.post(reverse("main:create_certification"), {
            "name": "Another Certificate", "issuer": "Example Academy",
            "credential_id": "CERT-43", "credential_url": "",
            "issue_date": "2025-03-04",
        })
        self.assertRedirects(project_response, reverse("main:show_projects"))
        self.assertRedirects(certificate_response, reverse("main:show_certifications"))
        self.assertTrue(Project.objects.filter(title="Another Project").exists())
        self.assertTrue(Certification.objects.filter(name="Another Certificate").exists())

        project_delete = reverse("main:delete_project", args=[self.project.id])
        certification_delete = reverse(
            "main:delete_certification", args=[self.certification.id],
        )
        self.assertEqual(self.client.get(project_delete).status_code, 405)
        self.assertRedirects(self.client.post(project_delete), reverse("main:show_projects"))
        self.assertRedirects(
            self.client.post(certification_delete), reverse("main:show_certifications"),
        )
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())
        self.assertFalse(Certification.objects.filter(pk=self.certification.pk).exists())

    def test_editor_can_edit_but_not_create_or_delete(self):
        self.client.force_login(self.editor)
        project_edit = reverse("main:edit_project", args=[self.project.id])
        certification_edit = reverse(
            "main:edit_certification", args=[self.certification.id],
        )
        self.assertContains(self.client.get(project_edit), "Edit Project")
        self.assertContains(self.client.get(certification_edit), "Edit Certification")
        self.assertRedirects(self.client.post(project_edit, {
            "title": "Updated Project", "description": self.project.description,
            "category": self.project.category, "tech_stack": self.project.tech_stack,
            "project_url": self.project.project_url, "project_image_url": "",
        }), reverse("main:show_projects"))
        self.assertRedirects(self.client.post(certification_edit, {
            "name": "Updated Certificate", "issuer": self.certification.issuer,
            "credential_id": self.certification.credential_id,
            "credential_url": "", "issue_date": "2025-02-03",
        }), reverse("main:show_certifications"))
        self.project.refresh_from_db()
        self.certification.refresh_from_db()
        self.assertEqual(self.project.title, "Updated Project")
        self.assertEqual(self.certification.name, "Updated Certificate")
        self.assertEqual(self.client.post(reverse("main:create_project"), {}).status_code, 403)
        self.assertEqual(self.client.post(reverse("main:create_certification"), {}).status_code, 403)
        self.assertEqual(self.client.post(
            reverse("main:delete_project", args=[self.project.id]),
        ).status_code, 403)
        self.assertEqual(self.client.post(
            reverse("main:delete_certification", args=[self.certification.id]),
        ).status_code, 403)

    def test_invalid_create_shows_errors_without_saving(self):
        self.client.force_login(self.owner)
        response = self.client.post(reverse("main:create_project"), {
            "title": "<b></b>", "description": "A project",
            "category": "Other", "tech_stack": "Django",
            "project_url": "not-a-url",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a valid URL")
        self.assertEqual(Project.objects.count(), 1)
