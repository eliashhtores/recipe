# Generated by Django 3.2 on 2022-05-10 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuisine', '0003_recipe'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(null=True, upload_to='recipe_image'),
        ),
    ]
