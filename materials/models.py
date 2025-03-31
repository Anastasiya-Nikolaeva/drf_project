from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200)
    preview_image = models.ImageField(upload_to="course_previews/")
    description = models.TextField()

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    preview_image = models.ImageField(upload_to="lesson_previews/")
    video_url = models.URLField()
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
