# Generated by Django 4.2.4 on 2023-12-08 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholar', '0008_elseviermodel_mydata_h_index_alter_mydata_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mydata',
            name='h_index',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
