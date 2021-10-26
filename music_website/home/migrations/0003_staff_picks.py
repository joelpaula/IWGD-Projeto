# Generated by Django 3.2.8 on 2021-10-25 19:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0002_rating_creation_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff_Picks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('recommendations', models.TextField()),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('record', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='home.record')),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]