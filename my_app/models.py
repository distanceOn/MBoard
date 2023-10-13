from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _



class CustomUser(AbstractUser):
    email_verification_code = models.CharField(max_length=6, null=True, blank=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_set",
        related_query_name="user",
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",
        related_query_name="user",
        verbose_name='user permissions'
    )



class CategoryChoices(models.TextChoices):
    TANKS = 'TN', _('Танки')
    HEALERS = 'HL', _('Хилы')
    DD = 'DD', _('ДД')
    TRADERS = 'TR', _('Торговцы')
    GUILD_MASTERS = 'GM', _('Гилдмастеры')
    QUEST_GIVERS = 'QG', _('Квестгиверы')
    BLACKSMITHS = 'BS', _('Кузнецы')
    LEATHERWORKERS = 'LW', _('Кожевники')
    ALCHEMISTS = 'AL', _('Зельевары')
    SPELL_CASTERS = 'SC', _('Мастера заклинаний')

class Advertisement(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.CharField(
        max_length=2,
        choices=CategoryChoices.choices,
        default=CategoryChoices.TANKS,
    )
    attached_file = models.FileField(upload_to='attachments/', null=True, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()

class Response(models.Model):
    user = models.ForeignKey(CustomUser, related_name='responses', on_delete=models.CASCADE)
    advertisement = models.ForeignKey(Advertisement, related_name='responses', on_delete=models.CASCADE)
    content = models.TextField()
    is_accepted = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)  # Поле для скрытия отклика


