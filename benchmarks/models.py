from django.db import models
from django.db.models import Avg, Max, Min, Count, Sum, StdDev

# Import django models
from forex.models import Currency
from countries.models import Country
from holidays.models import Holiday
from django.utils.text import slugify

# Import misc models
import numpy as np
import calendar as cal
from datetime import date, datetime, timedelta
from decimal import Decimal
from pandas import DataFrame, Series, date_range

# Import Settings
import benchmarks.settings as benchmarksettings


class BenchmarkGroup(models.Model):
    """
    Represents a group of benchmarks such as Global Equity, North American Equity, etc.
    """

    name = models.CharField(max_length = 255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    is_valid = models.BooleanField(default=True)
    
    # Cached data
    num_benchmarks = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = 'Benchmark Groups'
        verbose_name = 'Benchmark Group'
        ordering = ['name', ]
    
    def __unicode__(self):
        return u'%s' % (unicode(self.name))
    
    def save(self, *args, **kwargs):
        """
        Caches some data
        """
        self.num_benchmarks = Benchmark.objects.filter(group=self).count()
        
        # Generate slug name
        self.slug=slugify(self.name)        
        
        super(BenchmarkGroup, self).save(*args, **kwargs) # Call the "real" save() method.



class Benchmark(models.Model):
    """
    Represents a benchmark, such as a stock index, risk-free-rate,
    or peer group index.
    """
    
    group = models.ForeignKey(BenchmarkGroup)
    name = models.CharField(max_length = 255, unique=True)
    slug = models.SlugField(max_length=255, editable=False, unique=True)
    description = models.TextField()
    symbol = models.CharField(max_length = 20, unique=True)
    currency = models.ForeignKey(Currency)
    associated_country = models.ForeignKey(Country, blank=True, null=True, help_text="Use this only if there is one single relevent country")
    is_calculated = models.BooleanField(default=False, help_text="Is this benchmark calculated by Valuehorizon?")
    
    BENCHMARK_STATE_CHOICES = (
        (u'AC', u'Active'),
        (u'IN', u'Inactive'),
    )
    benchmark_state = models.CharField(max_length = 2, default="AC", choices = BENCHMARK_STATE_CHOICES)
    
    BENCHMARK_TYPE_CHOICES = (
        (u'I', u'Index Benchmark'),
        (u'R', u'Rate Benchmark'),
        (u'P', u'Peer-Group Benchmark'),
    )
    benchmark_type = models.CharField(max_length = 1, choices = BENCHMARK_TYPE_CHOICES)
    
    BENCHMARK_ASSET_CLASS_CHOICES = (
        (u'C', u'Equity'),
        (u'D', u'Debt'),
        (u'F', u'Balanced'),
        (u'O', u'Other'),
    )
    benchmark_asset_class = models.CharField(max_length = 1, choices = BENCHMARK_ASSET_CLASS_CHOICES)
    
    BENCHMARK_WEIGHT_TYPE = (
        (u'P', u'Price-Weighted'),
        (u'V', u'Value-Weighted'),
        (u'E', u'Equal-Weighted'),
        (u'U', u'Unweighted'),
    )
    benchmark_weighting = models.CharField(max_length = 1, choices = BENCHMARK_WEIGHT_TYPE, blank=True, null=True)
    
    
    
    # CACHED DATA
    
    # Misc
    full_start_date = models.DateField(blank=True, null=True, editable=False)
    num_components = models.IntegerField(null=True, blank=True)
    
    # Latest Data
    latest_date = models.DateField(null=True, blank=True, editable=False)
    latest_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, editable=False)
    latest_change = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, editable=False)
    latest_52_week_change = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, editable=False)
    latest_52_week_volatility = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, editable=False)
    latest_52_week_high = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, editable=False)
    latest_52_week_low = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, editable=False)
    latest_52_week_cov = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, editable=False)
    ytd_return = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, editable=False)
    
    # Analysis
    return_volatility_3_year = models.FloatField(null=True, blank=True)
    
    # Twelve month price movement
    month_12_prior = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, editable=False)
    month_11_prior = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, editable=False)
    month_10_prior = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, editable=False)
    month_09_prior = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, editable=False)
    month_08_prior = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, editable=False)
    month_07_prior = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, editable=False)
    month_06_prior = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, editable=False)
    month_05_prior = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, editable=False)
    month_04_prior = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, editable=False)
    month_03_prior = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, editable=False)
    month_02_prior = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, editable=False)
    month_01_prior = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, editable=False)
    

    class Meta:
        verbose_name_plural = 'Benchmarks'
        verbose_name = 'Benchmark'
        ordering = ['name', ]

    def __unicode__(self):
        return u'%s' % (unicode(self.name))
    
    def get_absolute_url(self):
        return ('benchmark_profile', (), { 'benchmarkslug': self.slug})
    get_absolute_url = models.permalink(get_absolute_url)
    
    
    def effective_series_start_date(self):
        """
        Return the greater of the first point in the data series,
        or 2009-01-01
        """
        if self.full_start_date != None:
            return max(benchmarksettings.BENCHMARK_VALUE_DATA_START_DATE, self.full_start_date)
        else:
            return benchmarksettings.BENCHMARK_VALUE_DATA_START_DATE  
    
    
    def find_missing_values(self, direction=0, return_data=True, verbose=True):
        """
        This is a helper method that searches the benchmark value data and tries to find missing
        value points, excluding weekends and holidays.
        
        If direction == 0, find all value dates that SHOULD be in the db but are not. 
        eg. a regular non-holiday Thursday that is not in our db
        
        If direction ==1, find all value dates that SHOULD NOT be in the db but are.
        eg. a weekend that is in our db
        
        This is inefficient but works for now.
        
        There is an equivalent function for stocks.
        """
        
        start_date = self.effective_series_start_date()
        end_date = date.today() - timedelta(days=3)
        
        # Get benchmark dates from database
        value_points_db = BenchmarkData.objects.filter(benchmark=self, 
                                                date__gte=start_date).values_list('date', flat=True)
        
        # Get required dates (exclude weekends)
        required_dates = date_range(start_date, end_date, freq="B")
        required_dates_list = required_dates.tolist()
        required_dates_list_asdates = [i.date() for i in required_dates_list]
        
        # Remove holidays
        if self.associated_country != None:
            holidays = Holiday.objects.filter(country=self.associated_country,
                                              date__gte=start_date,
                                              date__lte=end_date).values_list('date', flat=True)
            for holiday in holidays:
                if holiday in required_dates_list_asdates:
                    required_dates_list_asdates.remove(holiday)
        
        assert direction in [0,1]
        
        
        missing_values = []
        # Find missing values
        if direction == 0:
            for required_value in required_dates_list_asdates:
                if required_value not in value_points_db:
                    missing_values.append(required_value)
                    
            print "Missing %s value points" % (str(len(missing_values)))
        
        if direction == 1:
            for value in value_points_db:
                if value not in required_dates_list_asdates:
                    missing_values.append(value)
                    
            print "Unrequired %s value  points" % (str(len(missing_values)))

        if verbose == True:
            new_list = []
            for i in missing_values:
                new_list.append((i, "      " + str(i.strftime("%A"))))
            missing_values = new_list
            
        if return_data == True:
            missing_values.sort()
            return missing_values    
    
    def generate_dataframe(self, start_date=None, end_date=None, with_change=False, fill=True):
        """
        Generate a Pandas dataframe using Benchmark data
        """
        
        benchmark_symbol = self.symbol
        
        # Set start and end dates if unspecified
        if start_date == None:
            start_date = self.effective_series_start_date()
        if end_date == None:
            end_date = date.today()
        start_date_with_timelag = start_date - timedelta(days=90)
        
        # Get Benchmark Data
        benchmark_data = BenchmarkData.objects.filter(benchmark=self, 
                                            date__gte=start_date_with_timelag, 
                                            date__lte=end_date).values_list('date', 'price')        
        
        # Get earliest and latest actual data dates
        try:
            latest_actual_date = benchmark_data.reverse()[0][0]
            earliest_actual_date = benchmark_data[0][0]
        except:
            latest_actual_date = end_date   
            earliest_actual_date = start_date
            
        # Create dataframe
        price_column_name = "PRICE:" + benchmark_symbol
        if benchmark_data.count() > 5:  # Otherwise we get lower bound errors
            # Generate numpy array form queryset data
            benchmark_data_array = np.core.records.fromrecords(benchmark_data, names=['DATE', price_column_name])
            df = DataFrame.from_records(benchmark_data_array, index='DATE')
            end_date = df.index[-1]  # Set end date from today to the actual last recorded date           
        else:
            # If there is no data, generate an empty queryset
            benchmark_data_array = np.core.records.fromrecords([(date(1900,1,1) ,0)], names=['DATE', price_column_name])            
            df = DataFrame.from_records(benchmark_data_array, index='DATE')
            return df        
        
        # Convert to float
        df = df.astype(float)
        
        # Reindex dataframe to create a datapoint for each day
        if fill == True:
            if len(benchmark_data_array) > 1:  # Use >1 and not >0, since we may have single junk data
                date_index = date_range(start_date_with_timelag, end_date)
                df = df.reindex(date_index)
            else:
                date_index = []
                df = df.reindex(date_index)
                return df
                
            # Forward Fill
            df[price_column_name] = df[price_column_name].fillna(method="pad")
            
            # Reindex to required range
            date_index = date_range(max(earliest_actual_date,start_date), end_date)
            df = df.reindex(date_index)
        else:
            date_index = [i[0] for i in benchmark_data if i[0] >= max(earliest_actual_date,start_date) and i[0] <=end_date]
            df = df.reindex(date_index)
        
        if with_change == True:
            df["CHANGE"] = df["PRICE:"+self.symbol].pct_change()          
        
        return df
        
    def generate_cached_data(self):
        """
        Generate data for the Twelve month price movement and latest benchmark price data...
        """
        # Calculate full start date
        try:
            first_point = BenchmarkData.objects.filter(benchmark=self)[0]
            self.full_start_date = first_point.date
        except:
            self.full_start_date = None
        
        # Cache volatility, high, low, and coefficient of variation
        today = date.today()
        previous_date = today - timedelta(days=365)
        data_1_year_all = BenchmarkData.objects.filter(date__gte=previous_date, date__lte=today, benchmark=self)
        if data_1_year_all.count() > 0:
            self.earliest_date = BenchmarkData.objects.filter(benchmark=self).order_by('date')[0].date
            self.latest_52_week_volatility = Decimal(str(data_1_year_all.aggregate(StdDev('price'))['price__stddev']))
            self.latest_52_week_high= Decimal(str(data_1_year_all.aggregate(Max('price'))['price__max']))
            self.latest_52_week_low = Decimal(str(data_1_year_all.aggregate(Min('price'))['price__min']))
            average_price = Decimal(str(data_1_year_all.aggregate(Avg('price'))['price__avg']))
            if self.latest_52_week_volatility != None and average_price != None and average_price != 0:
                self.latest_52_week_cov = self.latest_52_week_volatility / average_price
            else:
                self.latest_52_week_cov = None
        else:
            self.latest_52_week_volatility = None
            self.latest_52_week_high = None
            self.latest_52_week_low = None
            self.latest_52_week_cov = None
        
        # Cache price movement
        # Clear data
        self.month_12_prior = None
        self.month_11_prior = None
        self.month_10_prior = None
        self.month_09_prior = None
        self.month_08_prior = None
        self.month_07_prior = None
        self.month_06_prior = None
        self.month_05_prior = None
        self.month_04_prior = None
        self.month_03_prior = None
        self.month_02_prior = None
        self.month_01_prior = None
        
        # Generate Data
        prior_date = date(today.year -1 , today.month, 1)
        prices = BenchmarkData.objects.filter(benchmark=self, date__gte=prior_date, date__lt=today, is_monthly=True)
        for price in prices:
            price_date = price.date
            #print price_date
            month_span = ( (today.month + 12) - price_date.month ) % 12
            #print month_span
            if date(price_date.year, price_date.month, 1) != date(today.year, today.month, 1):
                if month_span == 1:
                    self.month_01_prior = price.price
                if month_span == 2:
                    self.month_02_prior = price.price
                if month_span == 3:
                    self.month_03_prior = price.price
                if month_span == 4:
                    self.month_04_prior = price.price
                if month_span == 5:
                    self.month_05_prior = price.price
                if month_span == 6:
                    self.month_06_prior = price.price
                if month_span == 7:
                    self.month_07_prior = price.price
                if month_span == 8:
                    self.month_08_prior = price.price
                if month_span == 9:
                    self.month_09_prior = price.price
                if month_span == 10:
                    self.month_10_prior = price.price
                if month_span == 11:
                    self.month_11_prior = price.price
                if month_span == 12:
                    self.month_12_prior = price.price
        
        # Now cache some other data
        try:
            latest_price = BenchmarkData.objects.filter(benchmark=self).latest()
            #print "Benchmark data found.... Caching it..."
            self.latest_date = latest_price.date
            self.latest_price = latest_price.price
            self.latest_change = latest_price.change
            self.latest_52_week_change = latest_price.change_52_week
        except BenchmarkData.DoesNotExist:
            #print "There is no recent benchmark price data"
            self.latest_date = None
            self.latest_price = None
            self.latest_change = None
            self.latest_52_week_change = None
        
        try:
            last_price_last_year = BenchmarkData.objects.filter(benchmark=self, date__year=date.today().year - 1).latest()
            current_price = BenchmarkData.objects.filter(benchmark=self).latest()
            self.ytd_return = ( (current_price.price / last_price_last_year.price ) - 1) * 100
        #except BenchmarkData.DoesNotExist: 
        except:
            self.ytd_return = None
    
    
    def calculate_return(self, start_date, end_date):
        """
        Calculate the return of this benchmark between two dates
        """
        df = self.generate_dataframe()
        try:
            start_value = df.ix[start_date]["PRICE:"+self.symbol]
            end_value = df.ix[end_date]["PRICE:"+self.symbol]
            output = ((end_value / start_value) - 1.0) * 100.0
        except:
            output = None
        
        return output
        
        
    def save(self, *args, **kwargs):
        """
        Caches some data
        """
        
        self.generate_cached_data()
        
        # Generate slug name
        self.slug=slugify(self.name)        
        
        super(Benchmark, self).save(*args, **kwargs) # Call the "real" save() method.


class BenchmarkData(models.Model):
    """
    Represents the price data for a benchmark.
    """

    benchmark = models.ForeignKey(Benchmark)
    date = models.DateField()
    
    PRICE_TYPE_CHOICES = (
        (u'QUO', u'Source Quotation'),
        (u'ADJ', u'Adjusted by ValueHorizon'),
        (u'INS', u'Requires Inspection'),
        (u'FIL', u'Forward-Filled')
    )
    price_type = models.CharField(max_length = 3, choices = PRICE_TYPE_CHOICES, default="QUO")    
    
    # Price Data:
    price = models.DecimalField(max_digits=20, decimal_places=2)
    volume = models.BigIntegerField(null=True, blank=True)
    
    # Rate Data, used only if the data is specified as a rate, and not an index. In this case,
    #   we set price to 0
    rate = models.FloatField(null=True, blank=True)
    
    # Cached data
    monthly_volume = models.BigIntegerField(null=True, blank=True)  # Stores total volume traded for the month (only if is_monthly is True)
    value = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    change = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    num_trades = models.IntegerField(null=True, blank=True)
    
    # Index Metrics
    num_components = models.IntegerField(null=True, blank=True)
    divisor = models.FloatField(null=True, blank=True, editable=False)
    
    
    # Some meta data  flags
    is_monthly = models.BooleanField(default=False, editable=False)  # This tells us if this is the last price point for the month.
    is_trading_day = models.BooleanField(default=True, editable=False)  # This tells us if this day was a trading day
    
    # Performance Metrics
    growth_of_10_k = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, editable=False)
    change_1_month = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, editable=False)
    change_52_week = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, editable=False)
    high_52_week = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, editable=False)
    low_52_week = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, editable=False)
    
    
    class Meta:
        verbose_name_plural = 'Benchmark Data'
        verbose_name = 'Benchmark Data'
        ordering = ['date']
        unique_together = ("benchmark", "date")
        get_latest_by = "date"

    def __unicode__(self):
        return u'%s %s' % (unicode(self.benchmark.name), unicode(self.date),)
    
    def daily_percentage_change(self):
        """
        Computer the price change from the previous price
        """
        try:
            previous_price = BenchmarkData.objects.filter(benchmark=self.benchmark, 
                                                          date__lt=self.date).latest()
            latest_change = ((self.price - previous_price.price) / previous_price.price) * 100
            return latest_change
        except:
            return None
        
        
    
    def is_end_of_month(self):
        """
        Returns true if this is the last data point in the month. False otherwise.
        """
        year = self.date.year
        month = self.date.month
        start_of_month = date(year, month, 1)
        end_of_month = date(year, month, cal.monthrange(year, month)[1])
        month_points = BenchmarkData.objects.filter(benchmark=self.benchmark, date__lte=end_of_month, date__gte=start_of_month)
        if month_points:
            last_point = month_points.latest()
            if last_point.date == self.date:
                return True
            else:
                return False
        else:
            return True
        
    def set_monthly(self):
        """
        Determines whether this price data point is at the end of the month and sets
        the is_monthly flag accordingly
        """
        
        # Get year and month for this price object
        year = self.date.year
        month = self.date.month
        start_of_month = date(year, month, 1)
        end_of_month = date(year, month, cal.monthrange(year, month)[1])
        
        # Sets the is_monthly flag.
        if self.is_end_of_month():
            # Set is_monthly to False for all other objects for this month 
            not_monthly = BenchmarkData.objects.filter(benchmark=self.benchmark, date__gte=start_of_month, date__lte=end_of_month, is_monthly=True).exclude(date=self.date)
            not_monthly.update(is_monthly=False)
            self.is_monthly=True
    
    def generate_statistics(self, *args, **kwargs):
        """
        Generates the statistics for this data point.
        """
        # Generate the statistics
        self.change = self.daily_percentage_change()
        
        # 1 Month data
        date_1_month_previous = self.date - timedelta(days=30)
        date_1_month_previous_data = BenchmarkData.objects.filter(benchmark=self.benchmark, date__gte=date_1_month_previous, date__lte=self.date).order_by('date')
        if date_1_month_previous_data.count() > 0:
            price_1_month_previous = date_1_month_previous_data[0]
            #self.change_1_month = ((Decimal(self.price) - Decimal(price_1_month_previous.price)) / Decimal(price_1_month_previous.price)) * 100
        
        # 52 Week data
        date_52_week_previous = self.date - timedelta(weeks=52)
        date_52_week_previous_data = BenchmarkData.objects.filter(benchmark=self.benchmark, date__gte=date_52_week_previous, date__lte=self.date).order_by('date')
        if date_52_week_previous_data.count() > 0:
            # 52 Week change
            price_52_week_previous = date_52_week_previous_data[0]
            if price_52_week_previous.price != 0:
                try:
                    self.change_52_week = ((Decimal(self.price) - Decimal(price_52_week_previous.price)) / Decimal(price_52_week_previous.price)) * 100
                except:
                    self.change_52_week = None
                #print "Successfully calculated 52 week change: " + str(self.change_52_week)
            else:
                self.change_52_week = None
        else:
            self.change_52_week = None
        
        # Growth of 10K
        try:
            previous_point = BenchmarkData.objects.filter(benchmark=self.benchmark, date__lt=self.date).latest()
            if self.change != None and previous_point.growth_of_10_k != None:
                self.growth_of_10_k = (1 + (self.change / 100) ) * previous_point.growth_of_10_k
            else:
                self.growth_of_10_k = None
        except BenchmarkData.DoesNotExist:
            self.growth_of_10_k = None
    
    def simple_save(self, *args, **kwargs):
        """
        Simple save without any computation
        """
        super(BenchmarkData, self).save(*args, **kwargs) # Call the "real" save() method.
    
    def save(self, *args, **kwargs):
        """
        Overrides the save method. 
        Computes some of the statistics.
        """
        
        if self.benchmark.benchmark_type == "R":
            if self.rate == None:
                raise AssertionError("Rate must be specified for a Rate-Type Benchmark")
            else:
                self.price = 0
        else:
            if self.rate != None:
                raise AssertionError("Rate must be NOT specified for a Non-Rate-Type Benchmark")
        
        self.set_monthly()
        self.generate_statistics()
        super(BenchmarkData, self).save(*args, **kwargs) # Call the "real" save() method.
