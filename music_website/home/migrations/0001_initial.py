# Generated by Django 3.2.8 on 2021-10-24 11:23

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discogs_artist_id', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
                ('bio', models.TextField()),
                ('picture_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('creation_date', models.DateTimeField(verbose_name='Data de Criação')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discogs_release_id', models.IntegerField()),
                ('title', models.CharField(max_length=200)),
                ('year', models.IntegerField()),
                ('cover_url', models.URLField()),
                ('artist_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.artist')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(0, message='Rating mínimo é 0'), django.core.validators.MaxValueValidator(5, message='Rating máximo é 5')])),
                ('review', models.TextField()),
                ('record_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='home.record')),
                ('user_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user_id', 'record_id')},
            },
        ),
        migrations.CreateModel(
            name='Like_Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField()),
                ('artist_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='home.artist')),
                ('user_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user_id', 'artist_id')},
            },
        ),
        migrations.CreateModel(
            name='Collection_Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=100)),
                ('collection_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='home.collection')),
                ('record_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='home.record')),
            ],
            options={
                'unique_together': {('record_id', 'collection_id')},
            },
        ),
    ]
