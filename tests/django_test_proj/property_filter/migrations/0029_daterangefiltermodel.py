# Generated by Django 3.0.7 on 2020-07-06 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property_filter', '0028_allvaluesfiltermodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='DateRangeFilterModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('date_time', models.DateTimeField()),
            ],
        ),
    ]
