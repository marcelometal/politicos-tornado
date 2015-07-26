# -*- coding: utf-8 -*-
#
# Copyright (c) 2015, Marcelo Jorge Vieira <metal@alucinados.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from tornado.gen import coroutine
from sqlalchemy.exc import IntegrityError
from ujson import loads

from politicos.models.legislator_events import LegislatorEvents
from politicos.handlers import BaseHandler


class AllLegislatorEventsHandler(BaseHandler):

    @coroutine
    def get(self):
        query = self.db.query(LegislatorEvents)
        legislator_events = query \
            .order_by(LegislatorEvents.date.asc()) \
            .all()

        if not legislator_events:
            self.set_status(404, 'Legislators Events not found')
            self.write_json([])
            return

        result = [x.to_dict() for x in legislator_events]
        self.write_json(result)

    @coroutine
    def post(self):
        post_data = loads(self.request.body)

        date = post_data.get('date')
        legislator_id = post_data.get('legislator_id')
        legislator_events_type_id = post_data.get('legislator_events_type_id')

        if not date or not legislator_events_type_id or not legislator_id:
            self.set_status(422, 'Invalid Legislator Events')
            self.write_json({'message': 'Invalid Legislator Events'})
            return

        data = {
            'date': date,
            'legislator_id': legislator_id,
            'legislator_events_type_id': legislator_events_type_id
        }

        try:
            legislator_events = LegislatorEvents \
                .add_legislator_events(self.db, data)
            self.write_json(legislator_events.to_dict())
        except IntegrityError:
            self.set_status(409, 'Legislator Events already exists')
            self.write_json({'message': 'Legislator Events already exists'})
