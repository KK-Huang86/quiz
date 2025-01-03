# Generated by Django 5.1.4 on 2024-12-27 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("urmart", "0004_remove_member_is_vip"),
    ]

    operations = [
        migrations.AlterField(
            model_name="member",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name="shopsalesstats",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
