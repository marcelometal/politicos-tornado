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

import logging

import sqlalchemy as sa
from slugify import slugify

from politicos.models import Base


class MandateEventsType(Base):
    __tablename__ = 'mandate_events_type'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column('name', sa.Unicode(100), unique=True, nullable=False)
    slug = sa.Column('slug', sa.Unicode(255), unique=True, nullable=False)

    def __str__(self):
        return unicode('%s' % self.name).encode('utf-8')

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            'name': self.name,
            'slug': self.slug,
        }

    @classmethod
    def add_mandate_events_type(self, db, data):
        mandate_events_type = MandateEventsType(
            name=data.get('name'),
            slug=unicode(slugify(data.get('name'))),
        )

        db.add(mandate_events_type)
        db.flush()

        logging.debug(
            u'Added mandate events type: "%s"', str(mandate_events_type)
        )

        return mandate_events_type
