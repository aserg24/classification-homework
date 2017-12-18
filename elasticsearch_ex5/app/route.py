#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

from flask import render_template, request, redirect, url_for, session, abort

from app import app
from index import es

LOG = logging.getLogger('access')


@app.route('/', methods=['GET', 'POST'])
def index():
    LOG.info('Access: %s, %s, %s' % (request.remote_addr, request.args, request.form))

    results = {}

    for k_form, v_form in request.form.items():
        found = es.search(index='chgk-index', doc_type='chgk', q=v_form)
        results[v_form] = [hit["_source"] for hit in found['hits']['hits']]

    return render_template('index.html', results=results)
