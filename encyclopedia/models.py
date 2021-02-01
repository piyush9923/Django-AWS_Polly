from django.db import models

# Create your models here.
class recordings(models.Model):
    blog_name = models.CharField(max_length=256, null=False)
    blog_audio = models.FileField(upload_to='recordings', null=True, blank=True)

    def __str__(self):
        return f"{self.blog_name}"