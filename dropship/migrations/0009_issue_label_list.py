# Generated by Django 2.2.4 on 2022-08-08 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dropship', '0008_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='label_list',
            field=models.ManyToManyField(blank=True, null=True, to='dropship.Label'),
        ),
    ]