from django.db import models


class Quote(object):
    def __init__(self, character, line, episode):
        self.character = character
        self.line = line
        self.episode = episode


class Snippet(models.Model):
    title = models.CharField(max_length=80)
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(max_length=80, default="python")

    class Meta:
        app_label = "test_app"


class Explosive(object):
    def __init__(self, safe, boom):
        self.safe = safe
        self.boom = boom


class Continent(models.Model):
    name = models.CharField(max_length=120)
    code = models.TextField()

    class Meta:
        app_label = "test_app"


class Country(models.Model):
    name = models.CharField(max_length=120)
    code = models.TextField()
    continent = models.ForeignKey("test_app.Continent", on_delete=models.CASCADE)

    class Meta:
        app_label = "test_app"


class Region(models.Model):
    name = models.CharField(max_length=120)
    code = models.TextField()
    country = models.ForeignKey("test_app.Country", on_delete=models.CASCADE)

    class Meta:
        app_label = "test_app"


class Province(models.Model):
    name = models.CharField(max_length=120)
    code = models.TextField()
    region = models.ForeignKey("test_app.Region", on_delete=models.CASCADE)

    class Meta:
        app_label = "test_app"


class City(models.Model):
    name = models.CharField(max_length=120)
    code = models.TextField()
    province = models.ForeignKey("test_app.province", on_delete=models.CASCADE)

    class Meta:
        app_label = "test_app"
