from django.db.models import Q
from django.test import TestCase
from query_parser.Parser import parse_or, parse_and, Parse
from .models import Order


class TestParser(TestCase):
    fixtures = ['all.json']

    def test_all(self):
        res = Parse({})
        q=Order.objects.filter(res)
        assert q.count() == 2
        self.assertEqual(str(q.query),'SELECT "test_app_order"."id", "test_app_order"."order_date", "test_app_order"."status", "test_app_order"."ordered_by_id" FROM "test_app_order"')

    def test_basic(self):
        res = Parse({"status": "Completed"})
        q=Order.objects.filter(res)
        assert q.count() == 1
        self.assertEqual(str(q.query),'SELECT "test_app_order"."id", "test_app_order"."order_date", "test_app_order"."status", "test_app_order"."ordered_by_id" FROM "test_app_order" WHERE "test_app_order"."status" = Completed')
    def test_or(self):
        d = {"or": {
            "status": "Completed",
            "ordered_by_id": 2
        }}
        res = Parse(d)
        q=Order.objects.filter(res)
        assert q.count() == 2
        self.assertEqual(str(q.query),'SELECT "test_app_order"."id", "test_app_order"."order_date", "test_app_order"."status", "test_app_order"."ordered_by_id" FROM "test_app_order" WHERE ("test_app_order"."status" = Completed OR "test_app_order"."ordered_by_id" = 2)')

    def test_and_fail(self):
        d = {"and": {
            "status": "Completed",
            "ordered_by_id": 2
        }}
        res = Parse(d)
        q=Order.objects.filter(res)
        assert q.count() == 0
        self.assertEqual(str(q.query),'SELECT "test_app_order"."id", "test_app_order"."order_date", "test_app_order"."status", "test_app_order"."ordered_by_id" FROM "test_app_order" WHERE ("test_app_order"."status" = Completed AND "test_app_order"."ordered_by_id" = 2)')

    def test_and_success(self):
        d = {"and": {
            "status": "Completed",
            "ordered_by_id": 1
        }}
        res = Parse(d)
        q=Order.objects.filter(res)
        assert q.count() == 1
        self.assertEqual(str(q.query),
                         'SELECT "test_app_order"."id", "test_app_order"."order_date", "test_app_order"."status", "test_app_order"."ordered_by_id" FROM "test_app_order" WHERE ("test_app_order"."status" = Completed AND "test_app_order"."ordered_by_id" = 1)')

    def test_not_fail(self):
        d = {"status": "Completed", "~ordered_by_id": 1}
        res = Parse(d)
        q=Order.objects.filter(res)
        assert q.count() == 0
        self.assertEqual(str(q.query),'SELECT "test_app_order"."id", "test_app_order"."order_date", "test_app_order"."status", "test_app_order"."ordered_by_id" FROM "test_app_order" WHERE ("test_app_order"."status" = Completed AND NOT ("test_app_order"."ordered_by_id" = 1))')

    def test_not_success(self):
        d = {"status": "Completed", "~ordered_by_id": 2}
        res = Parse(d)
        q = Order.objects.filter(res)
        assert q.count() == 1
        self.assertEqual(str(q.query),
                         'SELECT "test_app_order"."id", "test_app_order"."order_date", "test_app_order"."status", "test_app_order"."ordered_by_id" FROM "test_app_order" WHERE ("test_app_order"."status" = Completed AND NOT ("test_app_order"."ordered_by_id" = 2))')

    def test_not_or_success(self):
        d = {"or":{"status": "Completed", "~ordered_by_id": 1}}
        res = Parse(d)
        q=Order.objects.filter(res)
        assert q.count() == 2
        self.assertEqual(str(q.query),'SELECT "test_app_order"."id", "test_app_order"."order_date", "test_app_order"."status", "test_app_order"."ordered_by_id" FROM "test_app_order" WHERE ("test_app_order"."status" = Completed OR NOT ("test_app_order"."ordered_by_id" = 1))')

    def test_not_and_success(self):
        d = {"and":{"status": "Completed", "~ordered_by_id": 2}}
        res = Parse(d)
        q = Order.objects.filter(res)
        assert q.count() == 1
        self.assertEqual(str(q.query),
                         'SELECT "test_app_order"."id", "test_app_order"."order_date", "test_app_order"."status", "test_app_order"."ordered_by_id" FROM "test_app_order" WHERE ("test_app_order"."status" = Completed AND NOT ("test_app_order"."ordered_by_id" = 2))')
