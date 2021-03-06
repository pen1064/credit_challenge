# Generated by Django 4.0.1 on 2022-05-10 05:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Endpoints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('owner', models.CharField(max_length=128)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MLAlgorithm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('status', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=10000000)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=1000)),
                ('version', models.CharField(max_length=128)),
                ('parent_endpoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endpoints.endpoints')),
            ],
        ),
        migrations.CreateModel(
            name='MLRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_data', models.CharField(max_length=100000000)),
                ('response', models.CharField(max_length=1000000000)),
                ('full_response', models.CharField(max_length=1000000000)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('parent_algorithm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endpoints.mlalgorithm')),
            ],
        ),
    ]
