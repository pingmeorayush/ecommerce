# Generated by Django 4.0.1 on 2022-01-27 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='images/default.png', upload_to='images/'),
        ),
    ]
