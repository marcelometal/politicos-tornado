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

from politicos.models.legislator_events_type import LegislatorEventsType
from politicos.handlers import BaseHandler


class LegislatorEventsTypeHandler(BaseHandler):

    @coroutine
    def get(self, slug):
        query = self.db.query(LegislatorEventsType)
        legislator_events_type = query \
            .filter(LegislatorEventsType.slug == slug)\
            .first()
        if not legislator_events_type:
            self.write_json({})
            self.set_status(404, 'Legislator Events Type not found')
            return

        result = legislator_events_type.to_dict()
        self.write_json(result)


class AllLegislatorEventsTypesHandler(BaseHandler):

    @coroutine
    def get(self):
        query = self.db.query(LegislatorEventsType)
        legislator_events_types = query \
            .order_by(LegislatorEventsType.name.asc()) \
            .all()

        if not legislator_events_types:
            self.set_status(404, 'Legislators Events Type not found')
            self.write_json([])
            return

        result = [x.to_dict() for x in legislator_events_types]
        self.write_json(result)

    @coroutine
    def post(self):
        post_data = loads(self.request.body)

        name = post_data.get('name')

        if not name:
            self.set_status(422, 'Invalid Legislator Events Type')
            self.write_json({'message': 'Invalid Legislator Events Type'})
            return

        data = {'name': name}

        try:
            legislator_events_type = LegislatorEventsType \
                .add_legislator_events_type(self.db, data)
            self.set_status(201, 'Legislator Events Type created')
            self.set_header(
                'Location', '%s' % legislator_events_type.absolute_url(self)
            )
            self.write_json(legislator_events_type.to_dict())
        except IntegrityError:
            self.set_status(409, 'Legislator Events Type already exists')
            self.write_json({
                'message': 'Legislator Events Type already exists'
            })
