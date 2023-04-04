# File: sqlite_view.py
#
# Copyright (c) 2017-2022 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
import json

from django.http import HttpResponse


def display_query_results(provides, all_results, context):

    headers = []

    headers_set = set()
    for summary, action_results in all_results:
        for result in action_results:
            header_data = result.get_data()

    if header_data:
        headers += list(header_data[0].keys())

    if not headers_set:
        headers_set.update(headers)
    headers = sorted(headers_set)

    context['ajax'] = True
    if 'start' not in context['QS']:
        context['headers'] = headers
        return '/widgets/generic_table.html'

    adjusted_names = {}

    start = int(context['QS']['start'][0])
    length = int(context['QS'].get('length', ['5'])[0])
    end = start + length
    cur_pos = 0
    rows = []
    total = 0
    for summary, action_results in all_results:
        for result in action_results:
            data = result.get_data()
            total += len(data)
            for item in data:
                cur_pos += 1
                if (cur_pos - 1) < start:
                    continue
                if (cur_pos - 1) >= end:
                    break
                row = []

                for h in headers:
                    row.append({ 'value': item.get(adjusted_names.get(h, h)) })
                rows.append(row)

    content = {
        "data": rows,
        "recordsTotal": total,
        "recordsFiltered": total,
    }

    return HttpResponse(json.dumps(content), content_type='text/javascript')  # nosemgrep
