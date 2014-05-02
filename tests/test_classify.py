from nose.tools import *

from corenlp_sentiment import StanfordNLPSentimentClient
import unittest
import os


class TestStanfordNLPSentiment(unittest.TestCase):

    def setUp(self):
        self.client = StanfordNLPSentimentClient('http://localhost:8080')

    def tearDown(self):
        pass

    def test_classify(self):
        result = self.client.classify("What a wonderful test!")
        assert_equal(result, 'Very positive')