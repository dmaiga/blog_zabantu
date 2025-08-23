from django.db import models
from django.utils.translation import gettext_lazy as _

class NewsletterSubscriber(models.Model):
    email = models.EmailField(_('email'), unique=True)
    subscribed_at = models.DateTimeField(_('date d\'inscription'), auto_now_add=True)

    def __str__(self):
        return self.email



class ContactMessage(models.Model):
    name = models.CharField("Nom", max_length=255)
    email = models.EmailField("Email")
    subject = models.CharField("Sujet", max_length=255)
    message = models.TextField("Message")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
