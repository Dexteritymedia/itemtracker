# Generated by Django 4.2 on 2023-10-14 21:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0004_alter_itemday_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['-item'], 'verbose_name': 'Item', 'verbose_name_plural': 'Items'},
        ),
        migrations.AlterModelOptions(
            name='itemday',
            options={'ordering': ['-date'], 'verbose_name': 'Item', 'verbose_name_plural': 'Item'},
        ),
    ]
