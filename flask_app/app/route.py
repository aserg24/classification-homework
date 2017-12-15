#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

from flask import render_template, request, redirect, url_for, session, abort

from app import app
from classification import text_clf, categories

LOG = logging.getLogger('access')


@app.route('/', methods=['GET', 'POST'])
def index():
    LOG.info('Access: %s, %s, %s' % (request.remote_addr, request.args, request.form))

    results = {}

    for k_form, v_form in request.form.items():
        text = []
        text.append(v_form)
        predicted_new = text_clf.predict(text)
        k_form = categories[predicted_new[0]]

        results[k_form] = v_form

    return render_template('index.html', results=results)
