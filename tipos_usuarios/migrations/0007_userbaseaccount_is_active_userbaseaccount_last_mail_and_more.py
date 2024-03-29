# Generated by Django 4.2.6 on 2024-01-24 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tipos_usuarios', '0006_userbaseaccount_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbaseaccount',
            name='is_active',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AddField(
            model_name='userbaseaccount',
            name='last_mail',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userbaseaccount',
            name='mail_frequency',
            field=models.SmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='userbaseaccount',
            name='mail_notifications_active',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
