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

from datetime import datetime

from preggy import expect
from mock import patch, call

from politicos.models.legislator import Legislator
from politicos.utils import date_to_timestamp
from tests.unit.base import ApiTestCase
from tests.fixtures import LegislatorFactory


class TestLegislator(ApiTestCase):

    def test_can_create_legislator(self):
        date = datetime.utcnow().date()

        legislator = LegislatorFactory.create(
            name=u'Marcelo Jorge Vieira',
            picture=u'http://domain.com/picture.png',
            website=u'http://domain.com/',
            email=u'metal@alucinados.com',
            gender=u'M',
            date_of_birth=date,
            about=u'Heavy Metal',
        )

        expect(legislator.id).not_to_be_null()
        expect(legislator.name).to_equal('Marcelo Jorge Vieira')
        expect(legislator.picture).to_equal('http://domain.com/picture.png')
        expect(legislator.website).to_equal('http://domain.com/')
        expect(legislator.email).to_equal('metal@alucinados.com')
        expect(legislator.gender).to_equal('M')
        expect(legislator.date_of_birth).to_equal(date)
        expect(legislator.about).to_equal('Heavy Metal')

    def test_can_convert_to_dict(self):
        legislator = LegislatorFactory.create()
        legislator_dict = legislator.to_dict()

        expect(legislator_dict.keys()).to_length(7)

        expect(legislator_dict.keys()).to_be_like([
            'name', 'picture', 'website', 'email', 'gender',
            'date_of_birth', 'about',
        ])

        date_of_birth = date_to_timestamp(legislator.date_of_birth)

        expect(legislator_dict['name']).to_equal(legislator.name)
        expect(legislator_dict['picture']).to_equal(legislator.picture)
        expect(legislator_dict['website']).to_equal(legislator.website)
        expect(legislator_dict['email']).to_equal(legislator.email)
        expect(legislator_dict['gender']).to_equal(legislator.gender)
        expect(legislator_dict['date_of_birth']).to_equal(date_of_birth)
        expect(legislator_dict['about']).to_equal(legislator.about)

    def test_can_convert_to_dict_with_none_date_of_birth(self):
        legislator = LegislatorFactory.create()
        legislator.date_of_birth = None
        legislator_dict = legislator.to_dict()

        expect(legislator_dict['date_of_birth']).to_be_null()

    @patch('politicos.models.legislator.logging')
    def test_can_add_legislator(self, logging_mock):
        date_of_birth = date_to_timestamp(datetime.utcnow().date())
        data = {
            'name': u'Marcelo Jorge Vieira',
            'date_of_birth': date_of_birth
        }
        legislator = Legislator.add_legislator(self.db, data)

        expect(legislator.name).to_equal('Marcelo Jorge Vieira')
        expect(logging_mock.mock_calls).to_include(
            call.debug('Added legislator: "%s"', 'Marcelo Jorge Vieira')
        )
