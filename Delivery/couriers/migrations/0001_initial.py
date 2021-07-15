# Generated by Django 3.1.7 on 2021-03-23 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(verbose_name='region num')),
                ('average_time', models.IntegerField(default=0, verbose_name='average time of deliver in region')),
                ('completed_tasks', models.IntegerField(default=0, verbose_name='the total number of orders completed in the region')),
            ],
            options={
                'verbose_name': 'Region',
                'verbose_name_plural': 'Regions',
            },
        ),
        migrations.CreateModel(
            name='WorkingHours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('since', models.TimeField(verbose_name='start of job')),
                ('to', models.TimeField(verbose_name='end of job')),
            ],
            options={
                'verbose_name': 'Hours of Working',
            },
        ),
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('courier_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('courier_type', models.CharField(max_length=4)),
                ('earned_money', models.IntegerField(blank=True, default=0, verbose_name='earned money')),
                ('rating', models.FloatField(blank=True, default=0, verbose_name="courier's rating")),
                ('completed_tasks', models.IntegerField(blank=True, default=0, verbose_name='total delivered orders')),
                ('regions', models.ManyToManyField(blank=True, to='couriers.Region', verbose_name='Active regions')),
                ('working_hours', models.ManyToManyField(to='couriers.WorkingHours', verbose_name='Hours of Working')),
            ],
        ),
    ]