# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-22 08:01
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pretixbase', '0095_auto_20180604_1129'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('local_id', models.PositiveIntegerField()),
                ('state', models.CharField(choices=[('created', 'created'), ('pending', 'pending'), ('confirmed', 'confirmed'), ('canceled', 'canceled'), ('failed', 'failed'), ('refunded', 'refunded')], max_length=190)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('payment_date', models.DateTimeField(blank=True, null=True)),
                ('provider', models.CharField(blank=True, max_length=255, null=True, verbose_name='Payment provider')),
                ('info', models.TextField(blank=True, null=True, verbose_name='Payment information')),
                ('migrated', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('local_id',),
            },
        ),
        migrations.CreateModel(
            name='OrderRefund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('local_id', models.PositiveIntegerField()),
                ('state', models.CharField(choices=[('external', 'started externally'), ('created', 'created'), ('transit', 'in transit'), ('done', 'done'), ('failed', 'failed'), ('canceled', 'canceled')], max_length=190)),
                ('source', models.CharField(choices=[('admin', 'Organizer'), ('buyer', 'Customer'), ('external', 'External')], max_length=190)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('execution_date', models.DateTimeField(blank=True, null=True)),
                ('provider', models.CharField(blank=True, max_length=255, null=True, verbose_name='Payment provider')),
                ('info', models.TextField(blank=True, null=True, verbose_name='Payment information')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='refunds', to='pretixbase.Order', verbose_name='Order')),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='refunds', to='pretixbase.OrderPayment')),
            ],
            options={
                'ordering': ('local_id',),
            },
        ),
        migrations.AlterModelOptions(
            name='quota',
            options={'ordering': ('name',), 'verbose_name': 'Quota', 'verbose_name_plural': 'Quotas'},
        ),
        migrations.AlterField(
            model_name='orderfee',
            name='fee_type',
            field=models.CharField(choices=[('payment', 'Payment fee'), ('shipping', 'Shipping fee'), ('service', 'Service fee'), ('other', 'Other fees'), ('giftcard', 'Gift card')], max_length=100),
        ),
        migrations.AlterField(
            model_name='team',
            name='can_change_organizer_settings',
            field=models.BooleanField(default=False, help_text='Someone with this setting can get access to most data of all of your events, i.e. via privacy reports, so be careful who you add to this team!', verbose_name='Can change organizer settings'),
        ),
        migrations.AlterField(
            model_name='user',
            name='require_2fa',
            field=models.BooleanField(default=False, verbose_name='Two-factor authentication is required to log in'),
        ),
        migrations.AddField(
            model_name='orderpayment',
            name='fee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='pretixbase.OrderFee'),
        ),
        migrations.AddField(
            model_name='orderpayment',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payments', to='pretixbase.Order', verbose_name='Order'),
        ),
    ]
