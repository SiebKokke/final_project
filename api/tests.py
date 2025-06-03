from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import CustomUser
from publishers.models import Publisher
from news.models import Article


class ArticleSubscriptionAPITest(APITestCase):
    """
    Tests that API returns only articles from publishers.
    """

    def setUp(self):
        """
        Set up test users, publisher, and articles.
        """
        self.reader = CustomUser.objects.create_user(
            username="reader",
            password="pass",
            role="reader"
        )
        self.journalist = CustomUser.objects.create_user(
            username="journalist",
            password="pass",
            role="journalist"
        )
        self.publisher = Publisher.objects.create(
            name="Sample Publisher",
            description="A test publisher."
        )
        self.publisher.journalists.add(self.journalist)
        self.article1 = Article.objects.create(
            title="Article 1",
            content="Content 1",
            approved=True,
            author=self.journalist,
            publisher=self.publisher
        )
        self.article2 = Article.objects.create(
            title="Article 2",
            content="Content 2",
            approved=True,
            author=self.journalist,
            publisher=None
        )

    def test_articles_for_subscribed_reader(self):
        """
        Reader should see articles from publishers they are subscribed to.
        """
        self.reader.subscriptions_publishers.add(self.publisher)
        self.client.login(username="reader", password="pass")
        url = reverse("api-article-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        article_ids = [article["id"] for article in response.data]
        self.assertIn(self.article1.id, article_ids)

    def test_articles_for_non_subscribed_reader(self):
        """
        Reader who is not subscribed should not see publisher articles.
        """
        self.client.login(username="reader", password="pass")
        url = reverse("article-list-api")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        article_ids = [article["id"] for article in response.data]
        self.assertNotIn(self.article1.id, article_ids)
