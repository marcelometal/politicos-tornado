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

from politicos.models.mandate_events_type import MandateEventsType
from politicos.handlers import BaseHandler


class MandateEventsTypeHandler(BaseHandler):

    @coroutine
    def get(self, slug):
        query = self.db.query(MandateEventsType)
        mandate_events_type = query \
            .filter(MandateEventsType.slug == slug)\
            .first()
        if not mandate_events_type:
            self.write_json({})
            self.set_status(404, 'Mandate Events Type not found')
            return

        result = mandate_events_type.to_dict()
        self.write_json(result)


class AllMandateEventsTypesHandler(BaseHandler):

    @coroutine
    def get(self):
        query = self.db.query(MandateEventsType)
        mandate_events_types = query \
            .order_by(MandateEventsType.name.asc()) \
            .all()

        if not mandate_events_types:
            self.write_json([])
            self.set_status(404, 'Mandate Events Types not found')
            return

        result = [x.to_dict() for x in mandate_events_types]
        self.write_json(result)

    @coroutine
    def post(self):
        post_data = loads(self.request.body)

        name = post_data.get('name')

        if not name:
            self.set_status(422, 'Invalid Mandate Events Type')
            self.write_json({'message': 'Invalid Mandate Events Type'})
            return

        data = {'name': name}

        try:
            mandate_events_type = MandateEventsType.\
                add_mandate_events_type(self.db, data)
            self.set_status(201, 'Mandate Events Type created')
            self.set_header(
                'Location', '%s' % mandate_events_type.absolute_url(self)
            )
            self.write_json(mandate_events_type.to_dict())
        except IntegrityError:
            self.set_status(409, 'Mandate Events Type already exists')
            self.write_json({'message': 'Mandate Events Type already exists'})
