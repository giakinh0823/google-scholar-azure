# Generated by Django 3.1.5 on 2021-01-23 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_article_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='url',
            field=models.URLField(blank=True, default=None, max_length=2000, null=True),
        ),
    ]