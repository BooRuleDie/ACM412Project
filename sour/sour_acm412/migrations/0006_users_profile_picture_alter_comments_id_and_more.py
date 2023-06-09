# Generated by Django 4.2.1 on 2023-05-31 13:08

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('sour_acm412', '0005_alter_users_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='profile_picture',
            field=models.CharField(default='pp.svg', max_length=255),
        ),
        migrations.AlterField(
            model_name='comments',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='topics',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='users',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
