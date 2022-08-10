# Generated by Django 2.2.4 on 2022-08-10 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dropship', '0003_auto_20220810_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='type',
            field=models.CharField(choices=[('BUG', 'BUG'), ('TASK', 'TASK'), ('STORY', 'STORY'), ('EPIC', 'EPIC')], db_column='type', default='BUG', max_length=8),
        ),
    ]
