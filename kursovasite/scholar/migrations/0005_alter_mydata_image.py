# Generated by Django 4.2.4 on 2023-11-24 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholar', '0004_alter_mydata_email_alter_mydata_sub_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mydata',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
