# Generated by Django 3.0.8 on 2020-07-31 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property_filter', '0035_basecsvfiltermodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseInFilterModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(null=True)),
                ('text', models.CharField(max_length=32)),
            ],
        ),
    ]
