# Generated by Django 3.1.4 on 2020-12-17 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20201217_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='desc_en_us',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='categories',
            name='desc_es',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='categories',
            name='name_en_us',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='categories',
            name='name_es',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='desc_en_us',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='desc_es',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='price_en_us',
            field=models.DecimalField(decimal_places=3, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='price_es',
            field=models.DecimalField(decimal_places=3, max_digits=11, null=True),
        ),
    ]
