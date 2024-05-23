# Generated by Django 4.2.6 on 2024-05-23 10:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('topics', '0002_alter_topicmember_topic_alter_topicmember_user'),
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topicchatchannel',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='topicchatchannel',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='room_members', to='topics.topicmember'),
        ),
    ]