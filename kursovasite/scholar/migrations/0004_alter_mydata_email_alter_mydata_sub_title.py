# Generated by Django 4.2.4 on 2023-11-24 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholar', '0003_mydata_email_mydata_image_mydata_sub_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mydata',
            name='email',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='mydata',
            name='sub_title',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
    ]
