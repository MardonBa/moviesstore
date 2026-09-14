from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Movie, Review, ReviewReport


class ReviewReportingTests(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            name='Reportable Movie',
            price=10,
            description='A test movie.',
            image='movie_images/test.jpg',
        )
        self.author = User.objects.create_user('author', password='password123')
        self.first_reporter = User.objects.create_user('reporter1', password='password123')
        self.second_reporter = User.objects.create_user('reporter2', password='password123')
        self.review = Review.objects.create(
            movie=self.movie,
            user=self.author,
            comment='This review may be reported.',
        )
        self.report_url = reverse(
            'movies.report_review', args=[self.movie.id, self.review.id]
        )

    def test_first_report_does_not_hide_a_review(self):
        self.client.force_login(self.first_reporter)
        self.client.post(self.report_url)

        self.review.refresh_from_db()
        self.assertFalse(self.review.is_hidden)
        self.assertEqual(ReviewReport.objects.filter(review=self.review).count(), 1)
        self.assertContains(
            self.client.get(reverse('movies.show', args=[self.movie.id])),
            self.review.comment,
        )

    def test_second_distinct_report_hides_the_review(self):
        self.client.force_login(self.first_reporter)
        self.client.post(self.report_url)
        self.client.force_login(self.second_reporter)
        self.client.post(self.report_url)

        self.review.refresh_from_db()
        self.assertTrue(self.review.is_hidden)
        self.assertEqual(ReviewReport.objects.filter(review=self.review).count(), 2)
        self.assertNotContains(
            self.client.get(reverse('movies.show', args=[self.movie.id])),
            self.review.comment,
        )

    def test_a_user_cannot_report_the_same_review_twice(self):
        self.client.force_login(self.first_reporter)
        self.client.post(self.report_url)
        self.client.post(self.report_url)

        self.assertEqual(ReviewReport.objects.filter(review=self.review).count(), 1)
