# Generated by Django 3.2.5 on 2021-07-26 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210726_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.IntegerField(choices=[(1, 'fiction'), (2, 'non-fiction')], default=1),
            preserve_default=False,
        ),
    ]
