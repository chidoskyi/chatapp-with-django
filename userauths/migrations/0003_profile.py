# Generated by Django 5.0.6 on 2024-05-25 23:28

import django.db.models.deletion
import userauths.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0002_rename_bios_user_bio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150)),
                ('bio', models.CharField(max_length=150)),
                ('image', models.ImageField(default='default.jpg', upload_to=userauths.models.user_directory_path)),
                ('website', models.URLField(default='https://website.com')),
                ('facebook', models.URLField(default='https://facebook.com')),
                ('instagram', models.URLField(default='https://instagram.com')),
                ('twitter', models.URLField(default='https://twitter.com')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]