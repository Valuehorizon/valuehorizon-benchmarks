# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forex', '__first__'),
        ('countries', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Benchmark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', models.SlugField(unique=True, max_length=255, editable=False)),
                ('description', models.TextField()),
                ('symbol', models.CharField(unique=True, max_length=20)),
                ('is_calculated', models.BooleanField(default=False, help_text=b'Is this benchmark calculated by Valuehorizon?')),
                ('benchmark_state', models.CharField(default=b'AC', max_length=2, choices=[('AC', 'Active'), ('IN', 'Inactive')])),
                ('benchmark_type', models.CharField(max_length=1, choices=[('I', 'Index Benchmark'), ('R', 'Rate Benchmark'), ('P', 'Peer-Group Benchmark')])),
                ('benchmark_asset_class', models.CharField(max_length=1, choices=[('C', 'Equity'), ('D', 'Debt'), ('F', 'Balanced'), ('O', 'Other')])),
                ('benchmark_weighting', models.CharField(blank=True, max_length=1, null=True, choices=[('P', 'Price-Weighted'), ('V', 'Value-Weighted'), ('E', 'Equal-Weighted'), ('U', 'Unweighted')])),
                ('full_start_date', models.DateField(null=True, editable=False, blank=True)),
                ('num_components', models.IntegerField(null=True, blank=True)),
                ('latest_date', models.DateField(null=True, editable=False, blank=True)),
                ('latest_price', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
                ('latest_change', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
                ('latest_52_week_change', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
                ('latest_52_week_volatility', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
                ('latest_52_week_high', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
                ('latest_52_week_low', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
                ('latest_52_week_cov', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
                ('ytd_return', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
                ('return_volatility_3_year', models.FloatField(null=True, blank=True)),
                ('month_12_prior', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
                ('month_11_prior', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
                ('month_10_prior', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
                ('month_09_prior', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
                ('month_08_prior', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
                ('month_07_prior', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
                ('month_06_prior', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
                ('month_05_prior', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
                ('month_04_prior', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
                ('month_03_prior', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
                ('month_02_prior', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
                ('month_01_prior', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
                ('associated_country', models.ForeignKey(blank=True, to='countries.Country', help_text=b'Use this only if there is one single relevent country', null=True)),
                ('currency', models.ForeignKey(to='forex.Currency')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Benchmark',
                'verbose_name_plural': 'Benchmarks',
            },
        ),
        migrations.CreateModel(
            name='BenchmarkData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('price_type', models.CharField(default=b'QUO', max_length=3, choices=[('QUO', 'Source Quotation'), ('ADJ', 'Adjusted by ValueHorizon'), ('INS', 'Requires Inspection'), ('FIL', 'Forward-Filled')])),
                ('price', models.DecimalField(max_digits=20, decimal_places=2)),
                ('volume', models.BigIntegerField(null=True, blank=True)),
                ('rate', models.FloatField(null=True, blank=True)),
                ('monthly_volume', models.BigIntegerField(null=True, blank=True)),
                ('value', models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True)),
                ('change', models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True)),
                ('num_trades', models.IntegerField(null=True, blank=True)),
                ('num_components', models.IntegerField(null=True, blank=True)),
                ('divisor', models.FloatField(null=True, editable=False, blank=True)),
                ('is_monthly', models.BooleanField(default=False, editable=False)),
                ('is_trading_day', models.BooleanField(default=True, editable=False)),
                ('growth_of_10_k', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
                ('change_1_month', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
                ('change_52_week', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
                ('high_52_week', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
                ('low_52_week', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
                ('benchmark', models.ForeignKey(to='benchmarks.Benchmark')),
            ],
            options={
                'ordering': ['date'],
                'get_latest_by': 'date',
                'verbose_name': 'Benchmark Data',
                'verbose_name_plural': 'Benchmark Data',
            },
        ),
        migrations.CreateModel(
            name='BenchmarkGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', models.SlugField(unique=True, max_length=255)),
                ('description', models.TextField()),
                ('is_valid', models.BooleanField(default=True)),
                ('num_benchmarks', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Benchmark Group',
                'verbose_name_plural': 'Benchmark Groups',
            },
        ),
        migrations.AddField(
            model_name='benchmark',
            name='group',
            field=models.ForeignKey(to='benchmarks.BenchmarkGroup'),
        ),
        migrations.AlterUniqueTogether(
            name='benchmarkdata',
            unique_together=set([('benchmark', 'date')]),
        ),
    ]
