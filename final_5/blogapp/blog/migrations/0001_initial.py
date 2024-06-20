# Generated by Django 3.2.9 on 2024-06-03 00:40

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('slug', models.SlugField(blank=True, editable=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('image', models.ImageField(upload_to='blogs')),
                ('description', ckeditor.fields.RichTextField()),
                ('is_active', models.BooleanField(default=False)),
                ('is_home', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, editable=False, unique=True)),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='blog.category')),
            ],
        ),
    ]