# Generated by Django 4.2.7 on 2023-11-05 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='delivery_agent',
            fields=[
                ('agent_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='agent_pic/')),
                ('id_proof', models.ImageField(blank=True, null=True, upload_to='agent_id/')),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('usertype', models.IntegerField(default=4)),
                ('available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='event_management',
            fields=[
                ('event_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField(blank=True)),
                ('phone_no', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='event_pic/')),
                ('id', models.ImageField(blank=True, null=True, upload_to='event_id/')),
                ('usertype', models.IntegerField(default=4)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='register',
            fields=[
                ('reg_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('phone_no', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('usertype', models.IntegerField(default=2)),
                ('password', models.CharField(max_length=100)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pic/')),
                ('id', models.ImageField(blank=True, null=True, upload_to='user_id/')),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='restaurant',
            fields=[
                ('restaurant_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField(blank=True)),
                ('phone_no', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='restaurant_pic/')),
                ('id', models.ImageField(blank=True, null=True, upload_to='restaurant_id/')),
                ('usertype', models.IntegerField(default=3)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='restaurant_surplus_food',
            fields=[
                ('rs_id', models.AutoField(primary_key=True, serialize=False)),
                ('food_type', models.CharField(max_length=255)),
                ('details', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='food_images/')),
                ('restaurant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='event_surplus_food',
            fields=[
                ('es_id', models.AutoField(primary_key=True, serialize=False)),
                ('food_type', models.CharField(max_length=255)),
                ('details', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='food_images/')),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.event_management')),
            ],
        ),
    ]
