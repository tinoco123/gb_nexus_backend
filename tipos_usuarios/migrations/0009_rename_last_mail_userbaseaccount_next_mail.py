# Generated by Django 4.2.6 on 2024-02-02 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tipos_usuarios', '0008_remove_userbaseaccount_mail_notifications_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userbaseaccount',
            old_name='last_mail',
            new_name='next_mail',
        ),
    ]
