from django.db import models

class Client(models.Model):
    registration_email = models.TextField(unique=True)
    form_mail = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.registration_email
