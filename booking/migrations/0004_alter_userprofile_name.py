# Generated by Django 4.2.2 on 2023-06-14 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_userprofile_fname_userprofile_lname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]