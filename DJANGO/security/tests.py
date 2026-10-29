from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Resource, ResourceRole, Role, RoleUser

User = get_user_model()


class AuthenticationApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="clinic-user",
            password="SecureClinicPass-942!",
            email="clinic@example.test",
        )

    def test_login_returns_user_and_jwt_pair(self):
        response = self.client.post(
            reverse("custom_login"),
            {"username": "clinic-user", "password": "SecureClinicPass-942!"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["user"]["username"], "clinic-user")
        self.assertFalse(response.data["user"]["is_superuser"])

    def test_refresh_rotates_tokens(self):
        login = self.client.post(
            reverse("custom_login"),
            {"username": "clinic-user", "password": "SecureClinicPass-942!"},
            format="json",
        )

        response = self.client.post(
            reverse("custom_token_refresh"),
            {"refresh": login.data["refresh"]},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_profile_can_update_email(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(
            reverse("custom_profile"),
            {"email": "updated@example.test"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], "updated@example.test")

    def test_permissions_endpoint_returns_effective_resource_grants(self):
        role = Role.objects.create(name="Recepción")
        resource = Resource.objects.create(name="pacientes")
        RoleUser.objects.create(user=self.user, role=role)
        ResourceRole.objects.create(role=role, resource=resource)
        self.client.force_authenticate(self.user)

        response = self.client.get(reverse("auth_permissions"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["permissions"],
            [{
                "resource": "pacientes",
                "method": "*",
                "path": "/api/pacientes/",
                "roleId": role.id,
                "roleName": "Recepción",
            }],
        )

    def test_superuser_permissions_include_wildcard_grant(self):
        self.user.is_superuser = True
        self.user.save(update_fields=("is_superuser",))
        self.client.force_authenticate(self.user)

        response = self.client.get(reverse("auth_permissions"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["permissions"][0]["resource"], "*")

    def test_user_api_hashes_password_and_does_not_return_it(self):
        self.user.is_superuser = True
        self.user.save(update_fields=("is_superuser",))
        self.client.force_authenticate(self.user)

        response = self.client.post(
            reverse("user-list"),
            {
                "username": "new-clinic-user",
                "email": "new-clinic-user@example.test",
                "password": "Clinic-Access-9482!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertNotIn("password", response.data)
        created_user = User.objects.get(username="new-clinic-user")
        self.assertTrue(created_user.check_password("Clinic-Access-9482!"))
