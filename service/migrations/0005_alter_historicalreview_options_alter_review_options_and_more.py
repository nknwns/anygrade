# Generated by Django 4.0.4 on 2023-01-16 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_historicalreview_template_review_template_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalreview',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Опрос', 'verbose_name_plural': 'historical Опросы'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'verbose_name': 'Опрос', 'verbose_name_plural': 'Опросы'},
        ),
        migrations.AlterField(
            model_name='historicalquestion',
            name='title',
            field=models.CharField(db_index=True, max_length=1024, verbose_name='Содержание'),
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(max_length=1024, unique=True, verbose_name='Содержание'),
        ),
    ]
