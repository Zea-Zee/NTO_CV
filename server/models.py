from django.db import models

class ImageUpload(models.Model):
    image = models.ImageField(upload_to='uploads/')


class Image(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=10000)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Places(models.Model):
    my_id = models.IntegerField(default=0)
    XID = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    OSM = models.CharField(max_length=100)
    Lon = models.FloatField()
    Lat = models.FloatField()
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.name