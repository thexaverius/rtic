# Generated by Django 3.1.4 on 2020-12-30 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('catOmschrijving', models.CharField(max_length=100)),
            ],
        ),
    ]
