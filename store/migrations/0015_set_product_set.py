# Generated by Django 5.2.3 on 2025-06-19 08:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_delete_set'),
    ]

    operations = [
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(blank=True, editable=False, max_length=100, null=True, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/sets/')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='set',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.set'),
        ),
    ]
