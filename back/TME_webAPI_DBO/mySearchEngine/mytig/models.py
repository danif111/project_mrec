from django.db import models

# Create your models here.
class Book(models.Model):
    b_id = models.IntegerField(default='-1')
    title = models.CharField(blank=True, max_length=1024, null=True)
    content = models.CharField(max_length=250)
    image = models.CharField(max_length=250)


    # class Meta:
    #     ordering = ('tigID',)

class Word(models.Model):
    token = models.CharField(max_length=250)

    # class Meta:
    #     ordering = ('tigID',)

class Reference(models.Model):
    word = models.ForeignKey('Word', on_delete=models.CASCADE)
    book_reference = models.ForeignKey('Book', on_delete=models.CASCADE)
    occurrence = models.IntegerField(default='-1')

    class Meta:
        ordering = ('occurrence',)
