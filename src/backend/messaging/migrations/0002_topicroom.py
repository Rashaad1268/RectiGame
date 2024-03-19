# Generated by Django 4.2.6 on 2024-02-23 18:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import messaging.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('topics', '0002_alter_topic_icon'),
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, null=True)),
                ('code', models.SlugField(blank=True, max_length=20, unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topic_room_creator', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(related_name='topic_room_member', to=settings.AUTH_USER_MODEL)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='topics.topic')),
            ],
        ),
    ]
