# Generated by Django 3.1.7 on 2021-03-31 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameClan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GameClanInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('avatar', models.ImageField(height_field=100, upload_to='', width_field=100)),
                ('rating', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GameClanSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open_close', models.BooleanField(default=True)),
                ('min_rating', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GameClanUser',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('role', models.PositiveSmallIntegerField(choices=[(0, 'admin'), (1, 'player')], default=1)),
                ('entry', models.DateTimeField(auto_now_add=True)),
                ('clan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.gameclan')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GameClanChat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='message', max_length=30)),
                ('text', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('clan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.gameclan')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='gameclan',
            name='info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.gameclaninfo'),
        ),
        migrations.AddField(
            model_name='gameclan',
            name='settings',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.gameclansettings'),
        ),
    ]
