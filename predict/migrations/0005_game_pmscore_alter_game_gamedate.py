# Generated by Django 4.1.5 on 2023-02-01 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0004_game_p10_game_p11_game_p12_game_p13_game_p14_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='pmscore',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='gamedate',
            field=models.CharField(default='2023-02-01', max_length=10),
        ),
    ]
