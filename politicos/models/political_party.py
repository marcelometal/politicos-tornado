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


class PoliticalParty(Base):
    __tablename__ = 'political_party'

    id = sa.Column(sa.Integer, primary_key=True)
    siglum = sa.Column('siglum', sa.Unicode(15), unique=True, nullable=False)
    name = sa.Column('name', sa.Unicode(255), unique=True, nullable=False)
    wikipedia = sa.Column('wikipedia', sa.Unicode(2048), nullable=True)
    website = sa.Column('website', sa.Unicode(2048), nullable=True)
    founded_date = sa.Column('founded_date', sa.DateTime, nullable=True)
    logo = sa.Column('logo', sa.Unicode(2048), nullable=True)
    tse_number = sa.Column(sa.Integer, index=True, nullable=True)

    def __str__(self):
        return unicode('%s (%s)' % (self.siglum, self.name)).encode('utf-8')

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            'siglum': self.siglum,
            'name': self.name,
            'wikipedia': self.wikipedia,
            'website': self.website,
            'founded_date': self.founded_date,
            'logo': self.logo,
            'tse_number': self.tse_number,
        }

    def absolute_url(self, handler):
        return handler.reverse_url('political-party', self.siglum)

    @classmethod
    def add_political_party(self, db, data):
        political_party = PoliticalParty(
            name=data.get('name'),
            siglum=data.get('siglum'),
            wikipedia=data.get('wikipedia'),
            website=data.get('website'),
            founded_date=data.get('founded_date'),
            logo=data.get('logo'),
            tse_number=data.get('tse_number'),
        )

        db.add(political_party)
        db.flush()

        logging.debug(u'Added political party: "%s"', str(political_party))

        return political_party
