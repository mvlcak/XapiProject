# Generated by Django 3.2.8 on 2021-11-13 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_activity_object'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='object',
            field=models.CharField(max_length=600),
        ),
    ]
