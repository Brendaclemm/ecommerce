# Generated by Django 5.0.6 on 2024-06-10 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0002_alter_cateogry_options_product_is_sale_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Cateogry",
            new_name="Category",
        ),
    ]
