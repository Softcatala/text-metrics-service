#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2021 Jordi Mas i Hernandez <jmas@softcatala.org>
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
from typing import Optional
import uvicorn
from fastapi import FastAPI, Form, Request
from pydantic import BaseModel
import json
import os
import sys
import datetime
sys.path.append('../core/')


from analyzer import Analyzer
from document import Document
from syllabes import Syllabes
from wordtokenizer import WordTokenizer

class Item(BaseModel):
    name: str

app = FastAPI()

metrics_calls = 0
total_miliseconds = 0
total_words = 0

@app.post('/metrics')
def metrics_api_post(item):
    return _metrics_api(item.text)

@app.get('/metrics')
def metrics_api_get(text: str):
    return _metrics_api(text)

@app.get('/health')
def health_api_get():
    s = Syllabes.get_stats()
    ws = WordTokenizer.get_stats()
    s.update(ws)

    s['metrics_calls'] = metrics_calls
    seconds = total_miliseconds / 1000 if total_miliseconds else 0
    s['words_per_second'] =  total_words / seconds if seconds else 0
    s['average_time_per_request'] =  metrics_calls / seconds if seconds else 0
    s['process_id'] =  os.getpid()
    return s


def _metrics_api(text):
    global metrics_calls, total_miliseconds, total_words
    metrics_calls += 1
    start = datetime.datetime.now()

    document = Document(text)
    result = Analyzer(document).get_metrics()
    end = datetime.datetime.now()

    total_miliseconds += (end-start).microseconds
    total_words += document.get_count_words()
    return result

if __name__ == '__main__':
    uvicorn.run('style-service:app', host='0.0.0.0', port=5000)

