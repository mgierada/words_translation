from django.db import models
from django.db.models.fields import IntegerField

# Create your models here.


class Translation(models.Model):
    i = IntegerField(primary_key=True)
    frontCard = models.CharField(max_length=20)
    backCard = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'Translation'

    def __str__(self):
        return '{} entry'.format(self.i)


def populate_db():
    import os
    import json

    json_path = os.path.join(os.getcwd(), 'db.json')
    print(json_path)
    with open(os.path.join(json_path), 'r') as f:
        data = json.load(f)
    questions = data['questions']
    for question in questions:
        i = question['id']
        frontCard = question['frontCard']
        backCard = question['backCard']
        Translation.objects.create(
            i=i,
            frontCard=frontCard,
            backCard=backCard
        )


# populate_db()