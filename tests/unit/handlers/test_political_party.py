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

from ujson import loads, dumps
from preggy import expect
from tornado.testing import gen_test
from tornado.httpclient import HTTPError

from tests.unit.base import ApiTestCase
from tests.fixtures import PoliticalPartyFactory


class TestPoliticalPartyHandler(ApiTestCase):

    @gen_test
    def test_cannot_get_political_party_info(self):
        try:
            yield self.anonymous_fetch(
                '/political-parties/PBA',
                method='GET'
            )
        except HTTPError as e:
            expect(e).not_to_be_null()
            expect(e.code).to_equal(404)
            expect(e.response.reason).to_be_like('Political Party not found')
            expect(loads(e.response.body)).to_equal({})

    @gen_test
    def test_can_get_political_party_info(self):
        PoliticalPartyFactory.create(name=u'Partido Blah', siglum=u'PBA')

        response = yield self.anonymous_fetch(
            '/political-parties/PBA',
            method='GET'
        )
        expect(response.code).to_equal(200)
        political_party = loads(response.body)
        expect(political_party).to_length(7)
        expect(political_party.get('name')).to_equal('Partido Blah')
        expect(political_party.get('siglum')).to_equal('PBA')


class TestAllPoliticalPartyHandler(ApiTestCase):

    @gen_test
    def test_cannot_get_political_party_info(self):
        try:
            yield self.anonymous_fetch(
                '/political-parties/',
                method='GET'
            )
        except HTTPError as e:
            expect(e).not_to_be_null()
            expect(e.code).to_equal(404)
            expect(e.response.reason).to_be_like('Political Parties not found')
            expect(loads(e.response.body)).to_equal([])

    @gen_test
    def test_can_get_all_political_parties(self):
        political_parties = []
        for x in range(5):
            party = PoliticalPartyFactory.create(
                name=u'Partido %s' % x,
                siglum=u'%s' % x,
                founded_date=None,
            )
            political_parties.append(party.to_dict())

        response = yield self.anonymous_fetch(
            '/political-parties/',
            method='GET'
        )

        expect(response.code).to_equal(200)
        political_parties_loaded = loads(response.body)
        expect(political_parties_loaded).to_length(5)
        expect(political_parties_loaded).to_be_like(political_parties)

    @gen_test
    def test_can_add_political_party(self):
        response = yield self.anonymous_fetch(
            '/political-parties/',
            method='POST',
            body=dumps({'name': u'Partido Heavy Metal', 'siglum': u'PHM'})
        )
        expect(response.code).to_equal(200)
        data = loads(response.body)
        expect(data.get('siglum')).to_equal('PHM')

    @gen_test
    def test_cannot_add_political_party_twice(self):
        yield self.anonymous_fetch(
            '/political-parties/',
            method='POST',
            body=dumps({'name': u'Partido Heavy Metal', 'siglum': u'PHM'})
        )

        try:
            yield self.anonymous_fetch(
                '/political-parties/',
                method='POST',
                body=dumps({'name': u'Partido Heavy Metal', 'siglum': u'PHM'})
            )
        except HTTPError as e:
            expect(e).not_to_be_null()
            expect(e.code).to_equal(409)
            expect(e.response.reason).to_be_like(
                'Political Party already exists'
            )
            expect(loads(e.response.body)).to_equal({
                'message': 'Political Party already exists'
            })

    @gen_test
    def test_cannot_add_political_party_without_name(self):
        try:
            yield self.anonymous_fetch(
                '/political-parties/',
                method='POST',
                body=dumps({'siglum': u'PHM'})
            )
        except HTTPError as e:
            expect(e).not_to_be_null()
            expect(e.code).to_equal(422)
            expect(e.response.reason).to_be_like('Invalid Political Party')
            expect(loads(e.response.body)).to_equal({
                'message': 'Invalid Political Party'
            })

    @gen_test
    def test_cannot_add_political_party_without_siglum(self):
        try:
            yield self.anonymous_fetch(
                '/political-parties/',
                method='POST',
                body=dumps({'name': u'Partido Heavy Metal'})
            )
        except HTTPError as e:
            expect(e).not_to_be_null()
            expect(e.code).to_equal(422)
            expect(e.response.reason).to_be_like('Invalid Political Party')
            expect(loads(e.response.body)).to_equal({
                'message': 'Invalid Political Party'
            })
