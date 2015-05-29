from django.contrib import admin
from benchmarks.models import Benchmark, BenchmarkData, BenchmarkGroup


class BenchmarkAdmin(admin.ModelAdmin): 
    search_fields=["name",]
    list_filter=['benchmark_type', 'benchmark_asset_class']
admin.site.register(Benchmark, BenchmarkAdmin)

admin.site.register(BenchmarkData)

class BenchmarkGroupAdmin(admin.ModelAdmin): 
    prepopulated_fields = { 'slug': ['name'] }
admin.site.register(BenchmarkGroup, BenchmarkGroupAdmin)
