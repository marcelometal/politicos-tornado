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
from datetime import datetime, timedelta

import factory
import factory.alchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from slugify import slugify

from politicos.models.political_party import PoliticalParty
from politicos.models.legislator import Legislator
from politicos.models.institution import Institution
from politicos.models.political_office import PoliticalOffice
from politicos.models.legislature import Legislature
from politicos.models.mandate import Mandate
from politicos.models.mandate_events_type import MandateEventsType
from politicos.models.mandate_events import MandateEvents
from politicos.models.legislator_events_type import LegislatorEventsType
from politicos.models.legislator_events import LegislatorEvents


sqlalchemy_echo = logging.getLogger('nose').getEffectiveLevel() < logging.INFO
engine = create_engine(
    'mysql+mysqldb://root@localhost:3306/test_politicos',
    convert_unicode=True,
    pool_size=1,
    max_overflow=0,
    echo=sqlalchemy_echo
)
maker = sessionmaker(bind=engine, autoflush=True)
db = scoped_session(maker)


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = db

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        instance = \
            super(BaseFactory, cls)._create(target_class, *args, **kwargs)
        if (hasattr(cls, '_meta')
           and cls._meta is not None
           and hasattr(cls._meta, 'sqlalchemy_session')
           and cls._meta.sqlalchemy_session is not None):
            cls._meta.sqlalchemy_session.flush()
        return instance


class PoliticalPartyFactory(BaseFactory):
    class Meta:
        model = PoliticalParty

    name = factory.Sequence(lambda n: u'political party {0}'.format(n))
    siglum = factory.Sequence(lambda n: u'siglum {0}'.format(n))
    wikipedia = factory.Sequence(lambda n: u'http://wiki-{0}.com/'.format(n))
    website = factory.Sequence(lambda n: u'http://website-{0}.com/'.format(n))
    logo = factory.Sequence(lambda n: u'http://logo-{0}.com/'.format(n))
    founded_date = datetime.utcnow()


class LegislatorFactory(BaseFactory):
    class Meta:
        model = Legislator

    name = factory.Sequence(lambda n: u'Legislator {0}'.format(n))
    picture = factory.Sequence(lambda n: u'http://d.com/p{0}.png'.format(n))
    website = factory.Sequence(lambda n: u'http://d{0}.com/'.format(n))
    email = factory.Sequence(lambda n: u'name@d{0}.com'.format(n))
    gender = factory.Iterator([u'M', u'F'])
    date_of_birth = datetime.utcnow().date()
    about = factory.Sequence(lambda n: u' My About {0}'.format(n))


class InstitutionFactory(BaseFactory):
    class Meta:
        model = Institution

    siglum = factory.Sequence(lambda n: u'siglum {0}'.format(n))
    name = factory.Sequence(lambda n: u'Institution {0}'.format(n))
    logo = factory.Sequence(lambda n: u'http://i.com/p{0}.png'.format(n))


class PoliticalOfficeFactory(BaseFactory):
    class Meta:
        model = PoliticalOffice

    name = factory.Sequence(lambda n: u'name {0}'.format(n))
    slug = factory.LazyAttribute(lambda p: unicode(slugify(p.name)))


class LegislatureFactory(BaseFactory):
    class Meta:
        model = Legislature

    institution = factory.SubFactory(InstitutionFactory)
    date_start = datetime.utcnow().date()
    date_end = (datetime.utcnow() + timedelta(days=10)).date()


class MandateFactory(BaseFactory):
    class Meta:
        model = Mandate

    legislator = factory.SubFactory(LegislatorFactory)
    political_office = factory.SubFactory(PoliticalOfficeFactory)
    date_start = datetime.utcnow().date()
    date_end = (datetime.utcnow() + timedelta(days=10)).date()


class MandateEventsTypeFactory(BaseFactory):
    class Meta:
        model = MandateEventsType

    name = factory.Sequence(lambda n: u'name {0}'.format(n))
    slug = factory.LazyAttribute(lambda p: unicode(slugify(p.name)))


class MandateEventsFactory(BaseFactory):
    class Meta:
        model = MandateEvents

    mandate = factory.SubFactory(MandateFactory)
    mandate_events_type = factory.SubFactory(MandateEventsTypeFactory)
    date = datetime.utcnow().date()


class LegislatorEventsTypeFactory(BaseFactory):
    class Meta:
        model = LegislatorEventsType

    name = factory.Sequence(lambda n: u'name {0}'.format(n))
    slug = factory.LazyAttribute(lambda p: unicode(slugify(p.name)))


class LegislatorEventsFactory(BaseFactory):
    class Meta:
        model = LegislatorEvents

    legislator = factory.SubFactory(LegislatorFactory)
    legislator_events_type = factory.SubFactory(LegislatorEventsTypeFactory)
    date = datetime.utcnow().date()
