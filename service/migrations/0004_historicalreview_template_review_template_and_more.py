# Generated by Django 4.0.4 on 2023-01-16 05:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('service', '0003_category_author_historicalcategory_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalreview',
            name='template',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='service.template', verbose_name='Изначальный шаблон'),
        ),
        migrations.AddField(
            model_name='review',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='service.template', verbose_name='Изначальный шаблон'),
        ),
        migrations.AlterField(
            model_name='review',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author_review', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
    ]
