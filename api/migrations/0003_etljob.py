# Generated by Django 5.1.3 on 2024-11-24 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_transaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='ETLJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_name', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('running', 'Running'), ('success', 'Success'), ('failed', 'Failed')], default='pending', max_length=10)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('duration', models.DurationField(blank=True, null=True)),
                ('error_message', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'etl_jobs',
                'ordering': ['-start_time'],
            },
        ),
    ]
