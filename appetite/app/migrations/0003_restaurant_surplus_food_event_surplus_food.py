# Generated by Django 4.2.7 on 2023-11-06 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_restaurant_surplus_food_restaurant_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='restaurant_surplus_food',
            fields=[
                ('rs_id', models.AutoField(primary_key=True, serialize=False)),
                ('food_type', models.CharField(max_length=255)),
                ('details', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='food_images/')),
                ('uploaded_on', models.DateTimeField(auto_now_add=True)),
                ('time_expire', models.TimeField(blank=True, null=True)),
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
                ('uploaded_on', models.DateTimeField(auto_now_add=True)),
                ('time_expire', models.TimeField(blank=True, null=True)),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.event_management')),
            ],
        ),
    ]
