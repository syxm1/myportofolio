import uuid
from datetime import date

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from main.models import Certification, Education, Experience, Project
from main.serializers import ProjectSerializer


class PortfolioAPITestCases:
    def setUp(self):
        super().setUp()
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(
            username="visitor", password="test-password",
        )
        self.record = self.model.objects.create(**self.initial_data)
        self.list_url = reverse(f"api:{self.resource}-list")
        self.detail_url = reverse(f"api:{self.resource}-detail", args=[self.record.id])
        self.star_url = reverse(f"api:{self.resource}-star", args=[self.record.id])

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.record.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"query": self.search_term})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"query": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_record(self):
        url = reverse(f"api:{self.resource}-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                self.assertEqual(
                    self.client.post(self.list_url, self.payload, format="json").status_code,
                    401 if user is None else 403,
                )
                self.assertEqual(
                    self.client.patch(self.detail_url, {self.name_field: "Changed"}, format="json").status_code,
                    401 if user is None else 403,
                )
                self.assertEqual(
                    self.client.delete(self.detail_url).status_code,
                    401 if user is None else 403,
                )
        self.assertEqual(self.model.objects.count(), 1)
        self.record.refresh_from_db()
        self.assertEqual(getattr(self.record, self.name_field), self.initial_data[self.name_field])

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.model.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in self.invalid_cases:
            with self.subTest(changes=changes):
                response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn(field, response.data)
        self.assertEqual(self.model.objects.count(), 1)

    def test_text_fields_are_sanitized(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload,
            self.name_field: f"<b> {self.payload[self.name_field]} </b>",
            "description": "<p> Safe description </p>",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data[self.name_field], self.payload[self.name_field])
        self.assertEqual(response.data["description"], "Safe description")

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {self.name_field: "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.record.refresh_from_db()
        self.assertEqual(self.record.description, self.initial_data["description"])
        response = self.client.put(self.detail_url, {self.name_field: "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(self.model.objects.filter(pk=self.record.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_editor_can_update_but_cannot_create_or_delete(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {self.name_field: "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.record.refresh_from_db()
        self.assertEqual(getattr(self.record, self.name_field), "Changed")
        self.assertEqual(self.record.description, self.initial_data["description"])
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[self.name_field], self.payload[self.name_field])
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(self.model.objects.count(), 1)

    def test_staff_without_editor_group_cannot_manage(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {self.name_field: "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.record.refresh_from_db()
        self.assertEqual(getattr(self.record, self.name_field), self.initial_data[self.name_field])

    def test_options_does_not_change_data(self):
        response = self.client.options(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.record.refresh_from_db()
        self.assertEqual(getattr(self.record, self.name_field), self.initial_data[self.name_field])

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_token_authentication(self):
        token_url = reverse("api:token")
        response = self.client.post(
            token_url, {"username": "owner", "password": "test-password"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = Token.objects.get(user=self.owner)
        self.assertEqual(response.data["token"], token.key)
        self.assertEqual(
            self.client.post(token_url, {"username": "owner", "password": "wrong"}).status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        self.assertEqual(
            client.post(self.list_url, self.payload, format="json").status_code,
            status.HTTP_201_CREATED,
        )
        client.credentials(HTTP_AUTHORIZATION="Token invalid")
        self.assertEqual(
            client.post(self.star_url).status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.model.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ProjectSerializerTest(APITestCase):
    def test_contract_and_optional_image(self):
        serializer = ProjectSerializer(data={
            "id": str(uuid.uuid4()),
            "title": "Portfolio",
            "description": "A portfolio app",
            "tech_stack": "Flutter, Django",
            "project_url": "https://example.com/project",
            "project_image_url": "",
        })
        self.assertTrue(serializer.is_valid(), serializer.errors)
        project = serializer.save()
        self.assertIsInstance(project.id, uuid.UUID)
        self.assertIsInstance(serializer.data["id"], str)
        self.assertEqual(set(serializer.data), {
            "id", "title", "description", "tech_stack",
            "project_url", "project_image_url",
            "star_count", "is_starred", "starred_by_names",
        })
        self.assertEqual(serializer.data["project_image_url"], "")
        self.assertTrue(Project.objects.filter(pk=project.pk).exists())

    def test_required_fields_and_urls(self):
        serializer = ProjectSerializer(data={
            "title": "Portfolio", "description": "A portfolio app",
            "tech_stack": "Flutter", "project_url": "not-a-url",
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn("project_url", serializer.errors)


class TokenLogoutAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="owner", password="test-password",
        )
        self.logout_url = reverse("api:api_logout")

    def test_logout_requires_authentication(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_session_request_without_token_returns_no_content(self):
        self.client.force_login(self.user)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")

    def test_logout_revokes_current_token(self):
        token = Token.objects.create(user=self.user)
        other_user = User.objects.create_user(username="other")
        other_token = Token.objects.create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = self.client.post(self.logout_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Token.objects.filter(pk=token.key).exists())
        self.assertTrue(Token.objects.filter(pk=other_token.key).exists())
        self.assertEqual(
            self.client.post(self.logout_url).status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


class EducationAPITest(PortfolioAPITestCases, APITestCase):
    model = Education
    resource = "education"
    name_field = "institution"
    search_field = "institution"
    search_term = "UNIVERSITY"
    initial_data = {
        "institution": "University", "program": "Computer Science",
        "level": "undergraduate", "description": "My studies",
        "started_at": date(2023, 1, 1),
    }
    payload = {
        "institution": "New University", "program": "Software Engineering",
        "level": "graduate", "description": "A useful program",
        "thumbnail": "https://example.com/education.png",
        "started_at": "2024-01-01", "ended_at": None,
    }
    invalid_cases = [
        ({"institution": "   "}, "institution"),
        ({"institution": '<img src="x" onerror="alert(1)">'}, "institution"),
        ({"program": "<b></b>"}, "program"),
        ({"description": "<p> </p>"}, "description"),
        ({"thumbnail": "javascript:alert(1)"}, "thumbnail"),
    ]


class ExperienceAPITest(PortfolioAPITestCases, APITestCase):
    model = Experience
    resource = "experience"
    name_field = "title"
    search_field = "title"
    search_term = "DEVELOPER"
    initial_data = {
        "title": "Developer", "description": "My work",
        "category": "full-time", "started_at": date(2023, 1, 1),
    }
    payload = {
        "title": "New role", "description": "A useful role",
        "category": "research", "thumbnail": "https://example.com/work.png",
        "started_at": "2024-01-01", "ended_at": None,
    }
    invalid_cases = [
        ({"title": "   "}, "title"),
        ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
        ({"description": "<p> </p>"}, "description"),
        ({"thumbnail": "javascript:alert(1)"}, "thumbnail"),
    ]



class ProjectAPITest(PortfolioAPITestCases, APITestCase):
    model = Project
    resource = "project"
    name_field = "title"
    search_term = "PORTFOLIO"
    initial_data = {
        "title": "Portfolio", "description": "A portfolio app",
        "tech_stack": "Django", "project_url": "https://example.com/portfolio",
    }
    payload = {
        "title": "New project", "description": "A useful project",
        "tech_stack": "Flutter", "project_url": "https://example.com/new",
        "project_image_url": "",
    }
    invalid_cases = [
        ({"title": "   "}, "title"),
        ({"description": "<p></p>"}, "description"),
        ({"tech_stack": "<b></b>"}, "tech_stack"),
        ({"project_url": "javascript:alert(1)"}, "project_url"),
    ]


class CertificationAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="cert-owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="cert-visitor")
        self.record = Certification.objects.create(
            name="Cloud Certificate", issuer="Example Academy",
            credential_id="CERT-42", issue_date=date(2025, 2, 3),
        )
        self.list_url = reverse("api:certification-list")
        self.detail_url = reverse("api:certification-detail", args=[self.record.id])
        self.star_url = reverse("api:certification-star", args=[self.record.id])
        self.payload = {
            "name": "New Certificate", "issuer": "Example Academy",
            "credential_id": "CERT-43", "credential_url": "",
            "issue_date": "2025-03-04",
        }

    def test_public_read_search_and_missing_record(self):
        self.assertEqual(self.client.get(self.list_url).data[0]["name"], self.record.name)
        self.assertEqual(self.client.get(self.detail_url).data["credential_id"], "CERT-42")
        self.assertEqual(len(self.client.get(self.list_url, {"query": "CLOUD"}).data), 1)
        self.assertEqual(self.client.get(self.list_url, {"query": "missing"}).data, [])
        self.assertEqual(self.client.get(reverse(
            "api:certification-detail", args=[uuid.uuid4()],
        )).status_code, 404)

    def test_permissions_crud_and_validation(self):
        self.assertEqual(self.client.post(self.list_url, self.payload).status_code, 401)
        self.client.force_authenticate(user=self.visitor)
        self.assertEqual(self.client.post(self.list_url, self.payload).status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.post(self.list_url, {
            **self.payload, "credential_url": "not-a-url",
        }).status_code, 400)
        created = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(created.status_code, 201)
        self.assertEqual(self.client.patch(self.detail_url, {
            "name": "Updated Certificate",
        }, format="json").status_code, 200)
        self.assertEqual(self.client.put(self.detail_url, {
            "name": "Incomplete",
        }, format="json").status_code, 400)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 204)
        self.assertFalse(Certification.objects.filter(pk=self.record.pk).exists())

    def test_editor_and_star(self):
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        self.assertEqual(self.client.patch(self.detail_url, {
            "issuer": "Updated Academy",
        }, format="json").status_code, 200)
        self.assertEqual(self.client.post(self.list_url, self.payload).status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        self.assertFalse(self.client.post(self.star_url).data["is_starred"])
