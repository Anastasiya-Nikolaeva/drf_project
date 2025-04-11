from django.db import models
from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    preview_image = models.ImageField(
        upload_to="course_previews/", null=True, blank=True
    )
    description = models.TextField()

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    preview_image = models.ImageField(
        upload_to="lesson_previews/", null=True, blank=True
    )
    video_url = models.URLField(null=True, blank=True)
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
