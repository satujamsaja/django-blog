# Generated by Django 2.2 on 2019-04-29 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20190428_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_featured_image',
            field=models.ImageField(blank=True, default='', upload_to='post'),
        ),
        migrations.AlterField(
            model_name='page',
            name='post_header',
            field=models.ImageField(blank=True, default='', upload_to='page'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_header',
            field=models.ImageField(blank=True, default='', upload_to='post'),
        ),
    ]