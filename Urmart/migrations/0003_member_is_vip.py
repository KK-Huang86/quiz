# Generated by Django 5.1.4 on 2024-12-24 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Urmart", "0002_shopsalesstats_remove_order_member_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="member",
            name="is_vip",
            field=models.BooleanField(default=False),
        ),
    ]
