# Generated by Django 4.2.6 on 2023-11-02 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Delivery_Kolomyia', '0004_dish_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dish',
            name='restaurant_id',
        ),
        migrations.AddField(
            model_name='dish',
            name='restaurant',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Delivery_Kolomyia.restaurant'),
        ),
    ]
