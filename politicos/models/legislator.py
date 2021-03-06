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

from politicos.models import Base
from politicos.utils import date_to_timestamp, timestamp_to_date


class Legislator(Base):
    __tablename__ = 'legislator'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column('name', sa.Unicode(200), nullable=False)
    picture = sa.Column('picture', sa.Unicode(2048), nullable=True)
    website = sa.Column('website', sa.Unicode(2048), nullable=True)
    email = sa.Column('email', sa.Unicode(2048), nullable=True)
    gender = sa.Column('gender', sa.Unicode(1), nullable=True)
    date_of_birth = sa.Column('date_of_birth', sa.Date, nullable=True)
    about = sa.Column('about', sa.UnicodeText(), nullable=True)

    def __str__(self):
        return unicode('%s' % self.name).encode('utf-8')

    def __repr__(self):
        return str(self)

    def to_dict(self):
        date_of_birth = None
        if self.date_of_birth:
            date_of_birth = date_to_timestamp(self.date_of_birth)

        return {
            'name': self.name,
            'picture': self.picture,
            'website': self.website,
            'email': self.email,
            'gender': self.gender,
            'date_of_birth': date_of_birth,
            'about': self.about,
        }

    @classmethod
    def add_legislator(self, db, data):
        date_of_birth = None
        if data.get('date_of_birth'):
            date_of_birth = timestamp_to_date(data.get('date_of_birth'))

        legislator = Legislator(
            name=data.get('name'),
            picture=data.get('picture'),
            website=data.get('website'),
            email=data.get('email'),
            gender=data.get('gender'),
            date_of_birth=date_of_birth,
            about=data.get('about'),
        )

        db.add(legislator)
        db.flush()

        logging.debug(u'Added legislator: "%s"', str(legislator))

        return legislator
