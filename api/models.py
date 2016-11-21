from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.timezone import now,utc
# from django.utils.timezone import utc
# Create your models here.
class Entry(models.Model):
    user = models.ForeignKey(User)
    pub_date = models.DateTimeField(default=now)
    title = models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True)
    body = models.TextField()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        # For automatic slug generation.
        if not self.slug:
            self.slug = slugify(self.title)[:50]

        return super(Entry, self).save(*args, **kwargs)


class UserProfile(models.Model):
    """
    A model to store extra information for each user.
    """
    user = models.OneToOneField(User, related_name='profile')
    gender = models.CharField(_("gender"), max_length=10)
    birth_year = models.PositiveIntegerField(_("birth year"))

    def __unicode__(self):
        return self.user.get_full_name()


class Recipe(models.Model):
    name = models.CharField(max_length=50)
    content = models.TextField()

    def __unicode__(self):
        return self.name




class Post(models.Model):
    # title = models.CharField(max_length=50)
    text  = models.CharField(max_length=200,blank=True,null=True,default="")
    image = models.ImageField(
        upload_to='static/posts',
        verbose_name='image',
        blank=True,
        null=True
    )
    video = models.FileField(
        upload_to='static/videos',
        verbose_name='video',
        null=True,
        blank = True

    )
    created = models.DateTimeField(default=now)

    def __unicode__(self):
        return self.text

    def get_hours(self):
        if self.created:
            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            timediff = now - self.created
            print timediff.total_seconds()
            return timediff.total_seconds()


























def signals_import():
    """ A note on signals.
    The signals need to be imported early on so that they get registered
    by the application. Putting the signals here makes sure of this since
    the models package gets imported on the application startup.
    """
    from tastypie.models import create_api_key

    models.signals.post_save.connect(create_api_key, sender=User)

signals_import()
