# Generated by Django 3.0.7 on 2020-06-25 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property_filter', '0019_auto_20200624_2033'),
    ]

    operations = [
        migrations.CreateModel(
            name='DateTimeFromToRangeFilterModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField()),
            ],
        ),
    ]
