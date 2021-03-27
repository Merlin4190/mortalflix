# Generated by Django 3.1.7 on 2021-03-27 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trailer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('imagelink', models.URLField(blank=True, default='')),
                ('link', models.URLField(unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='anime',
            name='category',
            field=models.CharField(choices=[('B', 'Bollywood'), ('C', 'Chinese'), ('F', 'French'), ('G', 'German'), ('Go', 'Gollywood'), ('H', 'Hollywood'), ('J', 'Japanese'), ('K', 'Korean'), ('N', 'Nollywood'), ('S', 'Spanish')], max_length=2),
        ),
    ]
