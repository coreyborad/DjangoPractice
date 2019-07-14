from django.db import models
import csv
import os
from datetime import datetime
from operator import itemgetter
from itertools import groupby
from django.db.models import Count

# Create your models here.


class Order(models.Model):
    order_id = models.CharField(max_length=20)
    customer_id = models.CharField(max_length=20)
    shipping = models.DecimalField(max_digits=4, decimal_places=0)
    created_at = models.CharField(max_length=60)

    @classmethod
    def _create(self, csv_file):

        # Clear before insert to model
        self.objects.all().delete()

        rows = csv.DictReader(csv_file, delimiter=',')
        for row in rows:
            obj = self.objects.create(
                order_id=row['order_id'],
                customer_id=row['customer_id'],
                shipping=row['shipping'],
                created_at=row['created_at'],
            )
            obj.save()
        return True

    @classmethod
    def _getShippingInfo(self):
        freeship_list = self.objects.filter(shipping=0).values()
        ship_list = self.objects.filter(shipping__gt=0).values()

        freeship_count = len(freeship_list)
        ship_count = len(ship_list)

        freeship_ratio = round(freeship_count / ship_count, 2)
        ship_ratio = 1 - freeship_ratio
        return [
            {
                'type': 'freeship',
                'ratio': freeship_ratio,
            },
            {
                'type': 'ship',
                'ratio': ship_ratio,
            },
        ]

    @classmethod
    def _getCohortInfo(self):
        result = {
            'date_list': [],
            'custom_date_list': {},
            'record': [],
            'fortable': {},
        }
        # Append record
        order_list = self.objects.all().order_by('created_at')
        for info in order_list:
            info.created_at = info.created_at.replace("上午", "AM")
            info.created_at = info.created_at.replace("下午", "PM")
            temp_datetime = datetime.strptime(
                info.created_at, '%Y/%m/%d %p %I:%M:%S')
            result['record'].append(
                {
                    'customer_id': info.customer_id,
                    'created_date': temp_datetime.strftime("%Y%m%d"),
                }
            )

        # Append date_list
        date_group = groupby(result['record'], itemgetter('created_date'))
        for key, group in date_group:
            result['date_list'].append(key)
            result['custom_date_list'][key] = []
            for g in group:
                if g['customer_id'] not in result['custom_date_list'][key]:
                    result['custom_date_list'][key].append(g['customer_id'])

        date_count = len(result['date_list'])
        # Append
        for i in range(date_count):
            this_date = result['date_list'][i]
            result['fortable'][this_date] = {}
            for j in range(i+1, date_count):
                temp_date = result['date_list'][j]
                result['fortable'][this_date][temp_date] = 0

        # Ans
        for i in range(date_count):
            this_date = result['date_list'][i]
            this_date_custom_list = result['custom_date_list'][this_date]
            this_date_custom_count = len(this_date_custom_list)
            for j in range(i+1, date_count):
                temp_date = result['date_list'][j]
                temp_date_custom_list = result['custom_date_list'][temp_date]

                s1 = set(this_date_custom_list)
                s2 = set(temp_date_custom_list)
                result['fortable'][this_date][temp_date] = str(
                    round(len(s1.intersection(s2)) / this_date_custom_count * 100, 2)) + '%'

        print(result)
        return result


class Order_item(models.Model):
    order_id = models.CharField(max_length=20)
    product_name = models.CharField(max_length=100)
    qty = models.DecimalField(max_digits=3, decimal_places=0)

    @classmethod
    def _create(self, csv_file):
        # Clear before insert to model
        self.objects.all().delete()

        rows = csv.DictReader(csv_file, delimiter=',')
        for row in rows:
            obj = self.objects.create(
                order_id=row['order_id'],
                product_name=row['product_name'],
                qty=row['qty'],
            )
            obj.save()
        return True

    @classmethod
    def _getRank(self):
        result = []
        item_count_list = self.objects.values('product_name').annotate(
            p_count=Count('product_name')).order_by('-p_count')
        # date expiration is same product?
        for i in range(3):
            result.append(
                {
                    'product_name': item_count_list[i]['product_name'],
                    'count': item_count_list[i]['p_count'],
                }
            )

        print(result)
        return result

    def __unicode__(self):
        return self.product_name
