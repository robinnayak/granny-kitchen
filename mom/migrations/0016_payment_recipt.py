# Generated by Django 4.0.6 on 2023-09-26 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mom', '0015_delete_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(blank=True, max_length=200)),
                ('total_amount', models.DecimalField(decimal_places=3, max_digits=8)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mom.order')),
                ('order_accept', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment_order_accept', to='mom.orderaccept')),
            ],
        ),
        migrations.CreateModel(
            name='Recipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipt_name', models.CharField(blank=True, max_length=200, null=True)),
                ('payment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment_recipt', to='mom.payment')),
            ],
        ),
    ]
