# Generated by Django 5.0.6 on 2024-07-03 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0005_topic_room_message'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['date'], 'verbose_name': 'Room Message', 'verbose_name_plural': 'Room Messages'},
        ),
    ]