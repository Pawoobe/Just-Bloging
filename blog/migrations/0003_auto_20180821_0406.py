# Generated by Django 2.0.8 on 2018-08-20 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_photo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Photo',
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='%Y/%m/%d/orig'),
        ),
    ]
