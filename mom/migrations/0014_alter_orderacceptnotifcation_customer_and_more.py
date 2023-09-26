# Generated by Django 4.0.6 on 2023-09-26 01:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
        ('mom', '0013_orderacceptnotifcation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderacceptnotifcation',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notify_order_accept_customer', to='customer.customer'),
        ),
        migrations.AlterField(
            model_name='orderacceptnotifcation',
            name='mom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notify_order_accept_mom', to='mom.mommodel'),
        ),
    ]