# Generated by Django 2.2 on 2019-04-26 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20190426_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='post_header',
            field=models.ImageField(default='', upload_to='page'),
        ),
        migrations.AddField(
            model_name='post',
            name='post_header',
            field=models.ImageField(default='', upload_to='post'),
        ),
    ]