#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2021-2022 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.


from __future__ import print_function
from flask import Flask, request, Response
from flask_cors import CORS
import json
import os
import sys
import datetime
import time
import humanize
import logging
import logging.handlers
import psutil
import uuid

sys.path.append('../core/')


from analyzer import Analyzer
from document import Document
from syllabes import Syllabes
from wordtokenizer import WordTokenizer

app = Flask(__name__)
CORS(app)

metrics_calls = 0
total_seconds = 0
total_words = 0
start_time = time.time()

def init_logging():
    LOGLEVEL = os.environ.get('LOGLEVEL', 'DEBUG').upper()
    logging.basicConfig(level=LOGLEVEL, format='%(asctime)s - %(levelname)s - %(message)s')

def json_answer(data, status = 200):
    json_data = json.dumps(data, indent=4, separators=(',', ': '))
    resp = Response(json_data, mimetype='application/json', status = status)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
   
@app.route('/metrics', methods=['POST'])
def metrics_api_post():
    return _metrics_api(request.form)

@app.route('/metrics', methods=['GET'])
def metrics_api_get():
    return _metrics_api(request.args)

@app.route('/health', methods=['GET'])
def health_api_get():
    s = Syllabes.get_stats()
    ws = WordTokenizer.get_stats()
    s.update(ws)

    rss = psutil.Process(os.getpid()).memory_info().rss // 1024 ** 2
    s['metrics_calls'] = metrics_calls
    s['words_per_second'] = total_words / total_seconds if total_seconds else 0
    s['average_time_per_request'] = total_seconds / metrics_calls if metrics_calls else 0
    s['process_id'] = os.getpid()
    s['rss'] = f"{rss} MB"
    s['up_time'] = humanize.precisedelta(time.time() - start_time, minimum_unit="seconds", format="%0.0f")
    return s
    
def _flush_logs():
    for handler in logging.getLogger().handlers:
        handler.flush()    


def _metrics_api(values):
    try:
        _uuid = str(uuid.uuid4())
        
        logging.debug(f"pid: {os.getpid()} - {_uuid}. Start")
        _flush_logs()
 
        global metrics_calls, total_seconds, total_words

        metrics_calls += 1
        start = datetime.datetime.now()

        if "text" not in values:
            result = {}
            result['error'] = "No s'ha especificat el paràmetre 'text'"
            logging.debug(f"/metrics/ {result['error']}")
            _flush_logs()
            return json_answer(result, 404)

        text = values['text']
        logging.debug(f"pid: {os.getpid()} - '{text}'") 
        document = Document(text)
        result = Analyzer(document).get_metrics()

        time_used = datetime.datetime.now() - start
        total_seconds += (time_used).total_seconds()
        total_words += document.get_count_words()
        r = json_answer(result)
        logging.debug(f"pid: {os.getpid()} - {_uuid}. Ends")
        _flush_logs()        
        return r

    except Exception as exception:
        logging.error(f"_metrics_api. pid: {os.getpid()} Error: {exception}")
        _flush_logs()        
        return json_answer({}, 200)

if __name__ == '__main__':
    app.debug = True
    init_logging()
    app.run()
else:
    init_logging()
