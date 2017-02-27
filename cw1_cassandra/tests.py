#!/usr/bin/env python

import unittest
from user_event_db import EventDatabase, json_to_event, json_to_timestamp_visists


class UserEventDBTest(unittest.TestCase):

    def setUp(self):
        self.db = EventDatabase('127.0.0.1', 'csc8101', 1)
        self.db.create_keyspace()
        self.db.create_tables()

    def tearDown(self):
        self.db.drop_keyspace()

    def test_record_visit(self):
        self.db.record_visit('A', 1, 'T1', 'T1.P1')
        self.db.record_visit('A', 1, 'T1', 'T1.P2')
        self.db.record_visit('A', 1, 'T1', 'T1.P2')
        self.db.record_visit('A', 1, 'T1', 'T1.P3')
        self.db.record_visit('A', 1, 'T2', 'T2.P2')
        self.db.record_visit('B', 1, 'T2', 'T2.P1')
        self.db.record_visit('B', 1, 'T2', 'T2.P2')
        self.db.record_visit('A', 1, 'T1', 'T1.P2')
        self.db.record_visit('A', 1, 'T1', 'T1.P2')

        client_a_visits_topic_1 = self.db.query_client_page_visits('A', 1, 'T1').current_rows
        self.assertEqual(len(client_a_visits_topic_1), 3)

        client_b_visits_topic_1 = self.db.query_client_page_visits('B', 1, 'T1').current_rows
        self.assertEqual(len(client_b_visits_topic_1), 0)

    def test_timestamp_summary(self):
        self.db.record_visits_in_timestamp(1, 'T1', 'T1.P1', 7)
        self.db.record_visits_in_timestamp(1, 'T1', 'T1.P2', 2)
        self.db.record_visits_in_timestamp(1, 'T1', 'T1.P3', 4)
        self.db.record_visits_in_timestamp(1, 'T2', 'T2.P2', 3)
        self.db.record_visits_in_timestamp(2, 'T1', 'T1.P4', 2)
        self.db.record_visits_in_timestamp(2, 'T2', 'T2.P1', 1)
        self.db.record_visits_in_timestamp(2, 'T2', 'T2.P2', 3)
        self.db.record_visits_in_timestamp(3, 'T1', 'T1.P2', 7)
        self.db.record_visits_in_timestamp(3, 'T2', 'T2.P1', 4)
        self.db.record_visits_in_timestamp(3, 'T2', 'T2.P2', 2)
        self.db.record_visits_in_timestamp(3, 'T3', 'T3.P1', 2)
        self.db.record_visits_in_timestamp(3, 'T3', 'T3.P2', 1)
        self.db.record_visits_in_timestamp(4, 'T1', 'T1.P1', 1)
        self.db.record_visits_in_timestamp(4, 'T1', 'T1.P2', 2)
        self.db.record_visits_in_timestamp(4, 'T2', 'T2.P1', 4)
        self.db.record_visits_in_timestamp(4, 'T2', 'T2.P2', 2)
        self.db.record_visits_in_timestamp(4, 'T3', 'T3.P1', 3)

        top_pages_timestamp_1_topic_1 = self.db.query_top_pages_in_topic(1, 'T1', 10).current_rows
        self.assertEquals(len(top_pages_timestamp_1_topic_1), 3)
        self.assertEquals(top_pages_timestamp_1_topic_1[0].page, 'T1.P1')
        self.assertEquals(top_pages_timestamp_1_topic_1[1].page, 'T1.P3')
        self.assertEquals(top_pages_timestamp_1_topic_1[2].page, 'T1.P2')

        top_pages_timestamp_1_topic_1_limit_2 = self.db.query_top_pages_in_topic(1, 'T1', 2).current_rows
        self.assertEquals(len(top_pages_timestamp_1_topic_1_limit_2), 2)

        top_pages_timestamp_2_topic_3 = self.db.query_top_pages_in_topic(2, 'T3', 10).current_rows
        self.assertEquals(len(top_pages_timestamp_2_topic_3), 0)


if __name__ == '__main__':
    unittest.main()
