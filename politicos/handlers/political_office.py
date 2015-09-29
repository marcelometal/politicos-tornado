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

from politicos.models.political_office import PoliticalOffice
from politicos.handlers import BaseHandler


class PoliticalOfficeHandler(BaseHandler):

    @coroutine
    def get(self, slug):
        query = self.db.query(PoliticalOffice)
        political_office = query.filter(PoliticalOffice.slug == slug).first()
        if not political_office:
            self.write_json({})
            self.set_status(404, 'Political Office not found')
            return

        result = political_office.to_dict()
        self.write_json(result)


class AllPoliticalOfficesHandler(BaseHandler):

    @coroutine
    def get(self):
        query = self.db.query(PoliticalOffice)
        political_offices = query.order_by(PoliticalOffice.name.asc()).all()

        if not political_offices:
            self.write_json([])
            self.set_status(404, 'Political Offices not found')
            return

        result = [x.to_dict() for x in political_offices]
        self.write_json(result)

    @coroutine
    def post(self):
        post_data = loads(self.request.body)

        name = post_data.get('name')

        if not name:
            self.set_status(422, 'Invalid Political Office')
            self.write_json({'message': 'Invalid Political Office'})
            return

        data = {'name': name}

        try:
            political_office = PoliticalOffice.\
                add_political_office(self.db, data)
            self.set_status(201, 'Political Office created')
            self.set_header(
                'Location', '%s' % political_office.absolute_url(self)
            )
            self.write_json(political_office.to_dict())
        except IntegrityError:
            self.set_status(409, 'Political Office already exists')
            self.write_json({'message': 'Political Office already exists'})
