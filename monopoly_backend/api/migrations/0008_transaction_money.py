# Generated by Django 4.1.5 on 2023-05-29 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='money',
            field=models.IntegerField(null=True),
        ),
    ]
