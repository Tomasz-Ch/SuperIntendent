# Generated by Django 2.2.1 on 2019-05-18 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superintendent', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]
