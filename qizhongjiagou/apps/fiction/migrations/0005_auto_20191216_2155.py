# Generated by Django 2.0.7 on 2019-12-16 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fiction', '0004_auto_20191213_0815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fiction',
            name='author',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='fiction', to='fiction.Author', verbose_name='小说作者'),
        ),
        migrations.AlterField(
            model_name='fiction_catelog',
            name='centent',
            field=models.CharField(max_length=64, verbose_name='章节路径'),
        ),
    ]
