# Generated by Django 2.0.2 on 2018-03-05 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='food_type',
            field=models.CharField(default='beef', max_length=200, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='food',
            unique_together=set(),
        ),
    ]
