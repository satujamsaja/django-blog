# Generated by Django 2.2 on 2019-05-07 03:02

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20190429_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='post_header',
            field=versatileimagefield.fields.VersatileImageField(blank=True, default='', height_field='395', upload_to='page', width_field='1110'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_featured_image',
            field=versatileimagefield.fields.VersatileImageField(blank=True, default='', height_field='395', upload_to='post', width_field='1110'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_header',
            field=versatileimagefield.fields.VersatileImageField(blank=True, default='', height_field='250', upload_to='post', width_field='200'),
        ),
    ]