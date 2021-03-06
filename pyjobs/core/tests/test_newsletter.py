from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from pyjobs.core.models import Job, Profile
from pyjobs.core.newsletter import subscribe_user_to_chimp


class NewsletterTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="v@m.com",
            email="v@m.com",
            password="top_secret",
            first_name="Vinicius",
            last_name="Mesel",
        )
        self.profile = Profile(
            user=self.user,
            github="http://www.aaa.com.br",
            linkedin="http://www.aaa.com.br",
            portfolio="http://www.aaa.com.br",
        )
        self.profile.save()

    def test_subscribe_to_newsletter(self):
        self.assertFalse(subscribe_user_to_chimp(self.profile))
