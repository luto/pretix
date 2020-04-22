# Generated by Django 3.0.4 on 2020-04-20 15:06

from decimal import Decimal

import django.db.models.deletion
import jsonfallback.fields
from django.conf import settings
from django.core.cache import cache
from django.db import migrations, models
from django.db.models import Count

import pretix.base.models.base
import pretix.base.models.fields
import pretix.base.models.orders


def fwd(app, schema_editor):
    Team = app.get_model('pretixbase', 'Team')
    Team.objects.filter(can_change_organizer_settings=True).update(can_manage_gift_cards=True)


def mail_migrator(app, schema_editor):
    Event_SettingsStore = app.get_model('pretixbase', 'Event_SettingsStore')

    for ss in Event_SettingsStore.objects.filter(
            key__in=['mail_text_order_approved', 'mail_text_order_placed', 'mail_text_order_placed_require_approval']
    ):
        chgd = ss.value.replace("{date}", "{expire_date}")
        if chgd != ss.value:
            ss.value = chgd
            ss.save()
            cache.delete('hierarkey_{}_{}'.format('event', ss.object_id))


def set_show_hidden_items(apps, schema_editor):
    Voucher = apps.get_model('pretixbase', 'Voucher')
    Voucher.objects.filter(quota__isnull=False).update(show_hidden_items=False)


def make_checkins_unique(apps, se):
    Checkin = apps.get_model('pretixbase', 'Checkin')
    for d in Checkin.objects.order_by().values('list_id', 'position_id').annotate(c=Count('id')).filter(c__gt=1):
        for c in Checkin.objects.filter(list_id=d['list_id'], position_id=d['position_id'])[:d['c'] - 1]:
            c.delete()


class Migration(migrations.Migration):
    replaces = [('pretixbase', '0108_auto_20190201_1527'), ('pretixbase', '0109_auto_20190208_1432'),
                ('pretixbase', '0110_auto_20190219_1245'), ('pretixbase', '0111_auto_20190219_0949'),
                ('pretixbase', '0112_auto_20190304_1726'), ('pretixbase', '0113_auto_20190312_0942'),
                ('pretixbase', '0114_auto_20190316_1014'), ('pretixbase', '0115_auto_20190323_2238'),
                ('pretixbase', '0116_auto_20190402_0722'), ('pretixbase', '0117_auto_20190418_1149'),
                ('pretixbase', '0118_auto_20190423_0839'), ('pretixbase', '0119_auto_20190509_0654'),
                ('pretixbase', '0120_auto_20190509_0736'), ('pretixbase', '0121_order_email_known_to_work'),
                ('pretixbase', '0122_orderposition_web_secret'), ('pretixbase', '0123_auto_20190530_1035'),
                ('pretixbase', '0124_seat_seat_guid'), ('pretixbase', '0125_voucher_show_hidden_items'),
                ('pretixbase', '0126_item_show_quota_left'), ('pretixbase', '0127_auto_20190711_0705'),
                ('pretixbase', '0128_auto_20190715_1510'), ('pretixbase', '0129_auto_20190724_1548'),
                ('pretixbase', '0130_auto_20190729_1311'), ('pretixbase', '0131_auto_20190729_1422'),
                ('pretixbase', '0132_auto_20190808_1253'), ('pretixbase', '0133_auto_20190830_1513'),
                ('pretixbase', '0134_auto_20190909_1042'), ('pretixbase', '0135_auto_20191007_0803'),
                ('pretixbase', '0136_auto_20190918_1742'), ('pretixbase', '0137_auto_20191015_1141'),
                ('pretixbase', '0138_auto_20191017_1151'), ('pretixbase', '0139_auto_20191019_1317'),
                ('pretixbase', '0140_voucher_seat'), ('pretixbase', '0141_seat_sorting_rank')]

    dependencies = [
        ('pretixbase', '0107_auto_20190129_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='generate_tickets',
            field=models.NullBooleanField(verbose_name='Allow ticket download'),
        ),
        migrations.AddField(
            model_name='invoiceline',
            name='event_date_from',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='invoiceline',
            name='subevent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                    to='pretixbase.SubEvent'),
        ),
        migrations.AlterField(
            model_name='event',
            name='plugins',
            field=models.TextField(blank=True, default='', verbose_name='Plugins'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='testmode',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='testmode',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(
            code=make_checkins_unique,
            reverse_code=django.db.migrations.operations.special.RunPython.noop,
        ),
        migrations.AlterUniqueTogether(
            name='checkin',
            unique_together={('list', 'position')},
        ),
        migrations.AddField(
            model_name='question',
            name='dependency_question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='dependent_questions', to='pretixbase.Question'),
        ),
        migrations.AddField(
            model_name='question',
            name='dependency_value',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cartposition',
            name='is_bundled',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='cartposition',
            name='addon_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='addons', to='pretixbase.CartPosition'),
        ),
        migrations.AlterField(
            model_name='orderposition',
            name='addon_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='addons', to='pretixbase.OrderPosition'),
        ),
        migrations.AddField(
            model_name='item',
            name='require_bundling',
            field=models.BooleanField(default=False,
                                      help_text='If this option is set, the product will only be sold as part of bundle products.',
                                      verbose_name='Only sell this product as part of a bundle'),
        ),
        migrations.CreateModel(
            name='ItemBundle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=1, verbose_name='Number')),
                ('designated_price', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.00'),
                                                         help_text="If set, it will be shown that this bundled item is responsible for the given value of the total gross price. This might be important in cases of mixed taxation, but can be kept blank otherwise. This value will NOT be added to the base item's price.",
                                                         max_digits=10, verbose_name='Designated price part')),
                ('base_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bundles',
                                                to='pretixbase.Item')),
                ('bundled_item',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bundled_with',
                                   to='pretixbase.Item', verbose_name='Bundled item')),
                ('bundled_variation',
                 models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                   related_name='bundled_with', to='pretixbase.ItemVariation',
                                   verbose_name='Bundled variation')),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='revoked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='itemvariation',
            name='original_price',
            field=models.DecimalField(blank=True, decimal_places=2,
                                      help_text='If set, this will be displayed next to the current price to show that the current price is a discounted one. This is just a cosmetic setting and will not actually impact pricing.',
                                      max_digits=7, null=True, verbose_name='Original price'),
        ),
        migrations.AddField(
            model_name='subevent',
            name='is_public',
            field=models.BooleanField(default=True,
                                      help_text='If selected, this event will show up publicly on the list of dates for your event.',
                                      verbose_name='Show in lists'),
        ),
        migrations.AddField(
            model_name='question',
            name='hidden',
            field=models.BooleanField(default=False, help_text='This question will only show up in the backend.',
                                      verbose_name='Hidden question'),
        ),
        migrations.AlterField(
            model_name='cartposition',
            name='attendee_name_parts',
            field=jsonfallback.fields.FallbackJSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='cartposition',
            name='subevent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='pretixbase.SubEvent'),
        ),
        migrations.AlterField(
            model_name='cartposition',
            name='voucher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='pretixbase.Voucher'),
        ),
        migrations.AlterField(
            model_name='event',
            name='is_public',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='invoiceaddress',
            name='name_parts',
            field=jsonfallback.fields.FallbackJSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='item',
            name='sales_channels',
            field=pretix.base.models.fields.MultiStringField(default=['web']),
        ),
        migrations.AlterField(
            model_name='order',
            name='sales_channel',
            field=models.CharField(default='web', max_length=190),
        ),
        migrations.AlterField(
            model_name='orderposition',
            name='attendee_name_parts',
            field=jsonfallback.fields.FallbackJSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='orderposition',
            name='subevent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='pretixbase.SubEvent'),
        ),
        migrations.AlterField(
            model_name='orderposition',
            name='voucher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='pretixbase.Voucher'),
        ),
        migrations.AlterField(
            model_name='staffsessionauditlog',
            name='method',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(db_index=True, max_length=190, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='order',
            name='email_known_to_work',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderposition',
            name='web_secret',
            field=models.CharField(db_index=True, default=pretix.base.models.orders.generate_secret, max_length=32),
        ),
        migrations.CreateModel(
            name='SeatingPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=190)),
                ('layout', models.TextField()),
                ('organizer',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seating_plans',
                                   to='pretixbase.Organizer')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, pretix.base.models.base.LoggingMixin),
        ),
        migrations.CreateModel(
            name='SeatCategoryMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('layout_category', models.CharField(max_length=190)),
                ('event',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seat_category_mappings',
                                   to='pretixbase.Event')),
                ('product',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seat_category_mappings',
                                   to='pretixbase.Item')),
                ('subevent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                               related_name='seat_category_mappings', to='pretixbase.SubEvent')),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=190)),
                ('blocked', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seats',
                                            to='pretixbase.Event')),
                ('product',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seats',
                                   to='pretixbase.Item')),
                ('subevent',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seats',
                                   to='pretixbase.SubEvent')),
                ('seat_guid', models.CharField(db_index=True, default=None, max_length=190)),
            ],
        ),
        migrations.AddField(
            model_name='cartposition',
            name='seat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='pretixbase.Seat'),
        ),
        migrations.AddField(
            model_name='event',
            name='seating_plan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='events',
                                    to='pretixbase.SeatingPlan'),
        ),
        migrations.AddField(
            model_name='orderposition',
            name='seat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='pretixbase.Seat'),
        ),
        migrations.AddField(
            model_name='subevent',
            name='seating_plan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='subevents',
                                    to='pretixbase.SeatingPlan'),
        ),
        migrations.AddField(
            model_name='voucher',
            name='show_hidden_items',
            field=models.BooleanField(default=True),
        ),
        migrations.RunPython(
            code=set_show_hidden_items,
            reverse_code=django.db.migrations.operations.special.RunPython.noop,
        ),
        migrations.AddField(
            model_name='item',
            name='show_quota_left',
            field=models.NullBooleanField(),
        ),
        migrations.RenameField(
            model_name='question',
            old_name='dependency_value',
            new_name='dependency_values',
        ),
        migrations.AlterField(
            model_name='question',
            name='dependency_values',
            field=pretix.base.models.fields.MultiStringField(default=['']),
        ),
        migrations.AddField(
            model_name='quota',
            name='close_when_sold_out',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='quota',
            name='closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='item',
            name='hidden_if_available',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pretixbase.Quota'),
        ),
        migrations.AddField(
            model_name='seat',
            name='row_name',
            field=models.CharField(default='', max_length=190),
        ),
        migrations.AddField(
            model_name='seat',
            name='seat_number',
            field=models.CharField(default='', max_length=190),
        ),
        migrations.AddField(
            model_name='seat',
            name='zone_name',
            field=models.CharField(default='', max_length=190),
        ),
        migrations.AddField(
            model_name='item',
            name='allow_waitinglist',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='invoice_to_state',
            field=models.CharField(max_length=190, null=True),
        ),
        migrations.AddField(
            model_name='invoiceaddress',
            name='state',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='print_on_invoice',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='WebAuthnDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('confirmed', models.BooleanField(default=True)),
                ('credential_id', models.CharField(max_length=255, null=True)),
                ('rp_id', models.CharField(max_length=255, null=True)),
                ('icon_url', models.CharField(max_length=255, null=True)),
                ('ukey', models.TextField(null=True)),
                ('pub_key', models.TextField(null=True)),
                ('sign_count', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunPython(
            code=mail_migrator,
            reverse_code=django.db.migrations.operations.special.RunPython.noop,
        ),
        migrations.AddField(
            model_name='checkin',
            name='auto_checked_in',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='checkinlist',
            name='auto_checkin_sales_channels',
            field=pretix.base.models.fields.MultiStringField(default=[]),
        ),
        migrations.AddField(
            model_name='user',
            name='auth_backend',
            field=models.CharField(default='native', max_length=255),
        ),
        migrations.CreateModel(
            name='GiftCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('issuance', models.DateTimeField(auto_now_add=True)),
                ('secret', models.CharField(db_index=True, default=pretix.base.models.giftcards.gen_giftcard_secret,
                                            max_length=190)),
                ('currency', models.CharField(max_length=10)),
                ('issued_in', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT,
                                                related_name='issued_gift_cards', to='pretixbase.OrderPosition')),
                ('issuer',
                 models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='issued_gift_cards',
                                   to='pretixbase.Organizer')),
                ('testmode', models.BooleanField(default=False)),
            ],
            options={
                'unique_together': {('secret', 'issuer')},
            },
            bases=(models.Model, pretix.base.models.base.LoggingMixin),
        ),
        migrations.AddField(
            model_name='item',
            name='issue_giftcard',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='team',
            name='can_manage_gift_cards',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='question',
            name='dependency_values',
            field=pretix.base.models.fields.MultiStringField(default=[]),
        ),
        migrations.AlterField(
            model_name='voucher',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vouchers',
                                    to='pretixbase.Item'),
        ),
        migrations.AlterField(
            model_name='voucher',
            name='quota',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vouchers',
                                    to='pretixbase.Quota'),
        ),
        migrations.AlterField(
            model_name='voucher',
            name='variation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vouchers',
                                    to='pretixbase.ItemVariation'),
        ),
        migrations.CreateModel(
            name='GiftCardTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transactions',
                                           to='pretixbase.GiftCard')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT,
                                            related_name='gift_card_transactions', to='pretixbase.Order')),
                ('payment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT,
                                              related_name='gift_card_transactions', to='pretixbase.OrderPayment')),
                ('refund', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT,
                                             related_name='gift_card_transactions', to='pretixbase.OrderRefund')),
            ],
            options={
                'ordering': ('datetime',),
            },
        ),
        migrations.CreateModel(
            name='GiftCardAcceptance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('collector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                related_name='gift_card_issuer_acceptance', to='pretixbase.Organizer')),
                ('issuer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                             related_name='gift_card_collector_acceptance', to='pretixbase.Organizer')),
            ],
        ),
        migrations.RunPython(
            code=fwd,
            reverse_code=django.db.migrations.operations.special.RunPython.noop,
        ),
        migrations.AddField(
            model_name='event',
            name='geo_lat',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='geo_lon',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='subevent',
            name='geo_lat',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='subevent',
            name='geo_lon',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='voucher',
            name='seat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vouchers',
                                    to='pretixbase.Seat'),
        ),
        migrations.AddField(
            model_name='seat',
            name='sorting_rank',
            field=models.BigIntegerField(default=0),
        ),
    ]