#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-
'''Class for generating the db'''

import broker

broker = broker.Broker()
broker.create_tables()


broker.add_user('admin', 'admin', 'admin')