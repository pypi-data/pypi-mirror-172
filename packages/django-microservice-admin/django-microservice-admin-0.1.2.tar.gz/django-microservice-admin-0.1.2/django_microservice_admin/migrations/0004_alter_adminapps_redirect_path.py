# Generated by Django 3.2.7 on 2022-10-11 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_microservice_admin', '0003_rename_redirect_url_adminapps_redirect_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminapps',
            name='redirect_path',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
