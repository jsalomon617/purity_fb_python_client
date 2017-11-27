# coding: utf-8

"""
    FlashBlade Management API

    The management APIs of FlashBlade.

    OpenAPI spec version: beta

    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

from environment import HOST, API_TOKEN
from purity_fb import *
from utils import *

class TestBladeApi(unittest.TestCase):
    """ BladeApi unit test stubs """

    def setUp(self):
        purity_fb = PurityFb(HOST)
        purity_fb.disable_verify_ssl()
        res = purity_fb.login(API_TOKEN)
        self.assertTrue(res == 200)
        self.blade = purity_fb.blade

    def tearDown(self):
        pass

    def test_list(self):
        """
        Test case for list
        """
        res = self.blade.list_blades()
        self.assertTrue(len(res.items) >= 3)
        check_is_list_of(res.items, Blade)

        names = [res.items[0].name, res.items[2].name]
        res = self.blade.list_blades(names=names)
        self.assertEquals(2, len(res.items))
        check_is_list_of(res.items, Blade)
        self.assertEquals(sorted(names), sorted(x.name for x in res.items))

    def test_list_and_sort(self):
        res = list_and_sort(self.blade.list_blades, 'raw_capacity', Blade)
        prev_raw_capacity = -1
        for blade in res.items:
            self.assertTrue(blade.raw_capacity >= prev_raw_capacity)
            prev_raw_capacity = blade.raw_capacity

    def test_list_by_filter(self):
        res = list_by_filter(self.blade.list_blades, 'raw_capacity > 0', Blade)
        for blade in res.items:
            self.assertTrue(blade.raw_capacity > 0)

    def test_list_by_limit(self):
        res = list_by_limit(self.blade.list_blades, 2, Blade)
        self.assertEquals(2, len(res.items))

    def test_list_by_token(self):
        res = list_by_limit(self.blade.list_blades, 1, Blade)
        token = res.pagination_info.continuation_token
        res = list_by_token(self.blade.list_blades, token, Blade)
        self.assertTrue(len(res.items) > 0)

if __name__ == '__main__':
    unittest.main()
