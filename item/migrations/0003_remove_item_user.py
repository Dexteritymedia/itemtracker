# Generated by Django 4.2 on 2023-10-14 21:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0002_alter_item_item_type_alter_itemday_note_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='user',
        ),
    ]
