# Generated by Django 4.2.4 on 2023-08-30 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keywords_app', '0004_rename_states_to_search_keyword_congreso_search'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyword',
            name='estatal_search',
            field=models.ManyToManyField(related_name='estatal_search', to='keywords_app.states'),
        ),
    ]
