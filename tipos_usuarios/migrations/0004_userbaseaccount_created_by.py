# Generated by Django 4.2.4 on 2023-09-20 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tipos_usuarios', '0003_cliente'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbaseaccount',
            name='created_by',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
