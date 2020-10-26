from django.db.models import Q
from django.test import TestCase
from query_parser.Parser import parse_or, parse_and, Parse
from .models import Order


class TestParser(TestCase):
    fixtures = ['all.json']

    def test_all(self):
        res = Parse({})
        assert Order.objects.filter(res).count() == 2

    def test_basic(self):
        res = Parse({"status": "Completed"})
        assert Order.objects.filter(res).count() == 1

    def test_or(self):
        d = {"or": {
            "status": "Completed",
            "ordered_by_id": 2
        }}
        res = Parse(d)
        assert Order.objects.filter(res).count() == 2

    def test_and_fail(self):
        d = {"and": {
            "status": "Completed",
            "ordered_by_id": 2
        }}
        res = Parse(d)
        assert Order.objects.filter(res).count() == 0

    def test_and_success(self):
        d = {"and": {
            "status": "Completed",
            "ordered_by_id": 1
        }}
        res = Parse(d)
        assert Order.objects.filter(res).count() == 1

    def test_not_fail(self):
        d = {"status": "Completed", "~ordered_by_id": 1}
        res = Parse(d)
        assert Order.objects.filter(res).count() == 0

    def test_not_success(self):
        d = {"status": "Completed", "~ordered_by_id": 2}
        res = Parse(d)
        assert Order.objects.filter(res).count() == 1
