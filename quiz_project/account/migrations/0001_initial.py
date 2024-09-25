# Generated by Django 5.1.1 on 2024-09-25 01:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_adress', models.EmailField(max_length=254, null=True, unique=True)),
                ('bio', models.TextField(null=True)),
                ('profile_img', models.ImageField(default='static\\images\\R.png', null=True, upload_to='static\\images')),
                ('location', models.CharField(max_length=30, null=True)),
                ('gender', models.CharField(choices=[('Nam', 'Nam'), ('Nu', 'Nu'), ('Khac', 'Khac')], max_length=10, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
