# Generated by Django 5.1.4 on 2024-12-19 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Urmart', '0003_rename_member_id_order_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_vip',
            field=models.BooleanField(default=False),
        ),
    ]