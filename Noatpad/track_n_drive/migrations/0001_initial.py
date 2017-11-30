# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-30 10:00
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('make', models.CharField(default='make', help_text='Enter the make of the car.', max_length=50)),
                ('model', models.CharField(default='model', help_text='Enter the model of the car.', max_length=50)),
                ('year', models.IntegerField(default=1, help_text='Enter the year of the car.')),
                ('engine_type', models.CharField(help_text='Enter the engine type of the car.', max_length=50, null=True)),
                ('mileage', models.IntegerField(help_text='Enter the mileage of the car', null=True)),
                ('oil_type', models.CharField(help_text='Enter the oil type of the car.', max_length=50, null=True)),
                ('color', models.CharField(default='color', help_text='Enter the color of the car.', max_length=50)),
                ('registration', models.CharField(blank=True, help_text='Enter the registration of the car.', max_length=50, null=True)),
                ('vin_number', models.CharField(help_text='Enter the vin number of the car', max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarAddedInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('information_name', models.CharField(default='info name', help_text='Information Category', max_length=200)),
                ('information_contents', models.CharField(default='info content', help_text='Information to Add', max_length=200)),
                ('car', models.ForeignKey(blank=True, help_text='Car', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='info', to='track_n_drive.Car')),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('address', models.EmailField(default='you@example.com', help_text='Enter your Email.', max_length=254, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='EmailTimings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequency', models.IntegerField(default=1, help_text='How many times should you be reminded?')),
                ('reminder', models.CharField(blank=True, choices=[('w', 'Weeks Before'), ('d', 'Days Before')], default='w', help_text='Alert Type', max_length=1)),
                ('email', models.ForeignKey(help_text='Select an email.', on_delete=django.db.models.deletion.CASCADE, to='track_n_drive.Email')),
            ],
        ),
        migrations.CreateModel(
            name='FutureRepair',
            fields=[
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Enter the name for the repair.', max_length=200)),
                ('date_of_repair', models.DateField(default=datetime.date(2017, 11, 30), help_text='Enter a date for this repair')),
                ('car', models.ForeignKey(help_text='Select the car that was repaired', on_delete=django.db.models.deletion.CASCADE, related_name='futurerepair', to='track_n_drive.Car')),
            ],
            options={
                'ordering': ['date_of_repair'],
            },
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('insurance_num', models.CharField(default='Ins. #', help_text='Enter your insurance number', max_length=30, primary_key=True, serialize=False)),
                ('company', models.CharField(help_text='Enter your company', max_length=30, null=True)),
                ('coverage', models.CharField(help_text='Enter your coverage', max_length=30, null=True)),
                ('expiration_date', models.DateField(null=True)),
                ('car', models.ForeignKey(help_text='Car Insurance', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='insurance', to='track_n_drive.Car')),
            ],
            options={
                'ordering': ['expiration_date'],
            },
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('license_num', models.CharField(help_text='Enter your license number', max_length=50, primary_key=True, serialize=False)),
                ('license_class', models.CharField(help_text='Enter your license class', max_length=50)),
                ('expiration_date', models.DateField()),
            ],
            options={
                'ordering': ['expiration_date'],
            },
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateField(null=True)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('number', models.CharField(default='0000000000', help_text='Enter your phone number.', max_length=15, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='PhoneTimings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequency', models.IntegerField(default=1, help_text='How many times should you be reminded?')),
                ('reminder', models.CharField(blank=True, choices=[('w', 'Weeks Before'), ('d', 'Days Before')], default='w', help_text='Alert Type', max_length=1)),
                ('notification', models.ForeignKey(help_text='Notification', on_delete=django.db.models.deletion.CASCADE, related_name='phonetiming', to='track_n_drive.Notifications')),
                ('phone', models.ForeignKey(help_text='Select a Phone.', on_delete=django.db.models.deletion.CASCADE, to='track_n_drive.Phone')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fname', models.CharField(default='Joe', help_text='Enter your first name.', max_length=30)),
                ('lname', models.CharField(default='Schmo', help_text='Enter your last name.', max_length=30)),
                ('password', models.CharField(default='password', help_text='Enter your password.', max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileAddedInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('information_name', models.CharField(default='info name', help_text='Information Category', max_length=200)),
                ('information_contents', models.CharField(default='info content', help_text='Information to Add', max_length=200)),
                ('profile_info', models.ForeignKey(blank=True, help_text='User', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='info', to='track_n_drive.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Repair',
            fields=[
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Enter the name for the repair.', max_length=200)),
                ('cost', models.CharField(help_text='Enter them cost for the repair', max_length=20)),
                ('date_made', models.DateField(default=datetime.date(2017, 11, 30), help_text='Enter the date of repair')),
                ('car', models.ForeignKey(help_text='Select the car that was repaired', on_delete=django.db.models.deletion.CASCADE, related_name='repair', to='track_n_drive.Car')),
            ],
            options={
                'ordering': ['date_made'],
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.ForeignKey(help_text='Select an email', on_delete=django.db.models.deletion.CASCADE, to='track_n_drive.Email')),
                ('phone', models.ForeignKey(help_text='Select a phone', on_delete=django.db.models.deletion.CASCADE, to='track_n_drive.Phone')),
                ('profile', models.ForeignKey(help_text='User Settings', on_delete=django.db.models.deletion.CASCADE, to='track_n_drive.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='TechAddedInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('information_name', models.CharField(default='info name', help_text='Information Category', max_length=200)),
                ('information_contents', models.CharField(default='info content', help_text='Information to Add', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Technician',
            fields=[
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fname', models.CharField(help_text='Enter technician first name.', max_length=30)),
                ('lname', models.CharField(help_text='Enter technician last name.', max_length=30)),
                ('street', models.CharField(help_text='Enter the street address of the technician.', max_length=100)),
                ('city', models.CharField(help_text='Enter the city of the technician.', max_length=100)),
                ('company', models.CharField(blank=True, help_text='Enter the company of the technician.', max_length=100, null=True)),
                ('profile', models.ForeignKey(help_text='Customer', on_delete=django.db.models.deletion.CASCADE, related_name='tech', to='track_n_drive.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='techaddedinfo',
            name='tech',
            field=models.ForeignKey(blank=True, help_text='Technician', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='info', to='track_n_drive.Technician'),
        ),
        migrations.AddField(
            model_name='repair',
            name='technician',
            field=models.ForeignKey(blank=True, help_text='Select the technician for the repair', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='repair', to='track_n_drive.Technician'),
        ),
        migrations.AddField(
            model_name='phonetimings',
            name='setting_ref',
            field=models.ForeignKey(help_text='User Settings', on_delete=django.db.models.deletion.CASCADE, to='track_n_drive.Settings'),
        ),
        migrations.AddField(
            model_name='phone',
            name='profile',
            field=models.ForeignKey(blank=True, help_text='User Phone', null=True, on_delete=django.db.models.deletion.SET_NULL, to='track_n_drive.Profile'),
        ),
        migrations.AddField(
            model_name='notifications',
            name='profile',
            field=models.ForeignKey(help_text='Notify User', on_delete=django.db.models.deletion.CASCADE, to='track_n_drive.Profile'),
        ),
        migrations.AddField(
            model_name='license',
            name='profile',
            field=models.ForeignKey(blank=True, help_text='User License', null=True, on_delete=django.db.models.deletion.SET_NULL, to='track_n_drive.Profile'),
        ),
        migrations.AddField(
            model_name='futurerepair',
            name='notification',
            field=models.ForeignKey(blank=True, help_text='Notification association', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='futurerepairnotif', to='track_n_drive.Notifications'),
        ),
        migrations.AddField(
            model_name='futurerepair',
            name='technician',
            field=models.ForeignKey(blank=True, help_text='Select the technician for the repair', null=True, on_delete=django.db.models.deletion.SET_NULL, to='track_n_drive.Technician'),
        ),
        migrations.AddField(
            model_name='emailtimings',
            name='notification',
            field=models.ForeignKey(help_text='Notification', on_delete=django.db.models.deletion.CASCADE, related_name='emailtiming', to='track_n_drive.Notifications'),
        ),
        migrations.AddField(
            model_name='emailtimings',
            name='setting_ref',
            field=models.ForeignKey(help_text='User Settings', on_delete=django.db.models.deletion.CASCADE, to='track_n_drive.Settings'),
        ),
        migrations.AddField(
            model_name='email',
            name='profile',
            field=models.ForeignKey(blank=True, help_text='User Email', null=True, on_delete=django.db.models.deletion.SET_NULL, to='track_n_drive.Profile'),
        ),
        migrations.AddField(
            model_name='car',
            name='profile',
            field=models.ForeignKey(help_text='Which user owns this car?', on_delete=django.db.models.deletion.CASCADE, related_name='car', to='track_n_drive.Profile'),
        ),
    ]
