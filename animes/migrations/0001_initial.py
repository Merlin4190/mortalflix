# Generated by Django 3.1.7 on 2021-03-22 01:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('category', models.CharField(choices=[('J', 'Japanese'), ('H', 'Hollywood')], max_length=2)),
                ('runtime', models.CharField(blank=True, default='', max_length=200)),
                ('label', models.CharField(choices=[('L', 'Latest'), ('R', 'Recently Released'), ('S', 'Coming Soon'), ('T', 'Top Rated')], max_length=2)),
                ('description', models.TextField()),
                ('avatar', models.ImageField(default=None, upload_to='images/avatar')),
                ('adlink', models.URLField(blank=True, default='')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('tag', models.CharField(choices=[('N', 'New'), ('SP', 'Season Priemere'), ('SF', 'Season Finale')], max_length=2)),
                ('adlink', models.URLField(blank=True, default='')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('anime', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='animes.anime')),
            ],
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, default='')),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('tag', models.CharField(choices=[('N', 'New'), ('SP', 'Season Priemere'), ('SF', 'Season Finale')], max_length=2)),
                ('adlink', models.URLField(blank=True, default='')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('anime', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='animes.anime')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='animes.season')),
            ],
        ),
        migrations.CreateModel(
            name='Download',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('link', models.URLField(unique=True)),
                ('mediaformat', models.CharField(choices=[('MP4', 'Mp4'), ('3GP', '3gp'), ('HD', 'High Definition')], max_length=3)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('anime', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='animes.anime')),
                ('episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='animes.episode')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='animes.season')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200)),
                ('phone', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('anime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='animes.anime')),
                ('episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='animes.episode')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='animes.season')),
            ],
        ),
        migrations.AddField(
            model_name='anime',
            name='genres',
            field=models.ManyToManyField(related_name='series', to='animes.Genre'),
        ),
    ]
