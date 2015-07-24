#!/usr/bin/python
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

from cow.server import Server
from cow.plugins.sqlalchemy_plugin import SQLAlchemyPlugin
from tornado.httpclient import AsyncHTTPClient
from tornado.web import url

from politicos import __version__
from politicos.utils import load_classes
from politicos.handlers import BaseHandler
from politicos.handlers.political_party import (
    PoliticalPartyHandler, AllPoliticalPartyHandler
)
from politicos.handlers.legislator import AllLegislatorsHandler
from politicos.handlers.legislator_events import AllLegislatorEventsHandler
from politicos.handlers.legislator_events_type import (
    LegislatorEventsTypeHandler, AllLegislatorEventsTypesHandler
)
from politicos.handlers.legislature import AllLegislaturesHandler
from politicos.handlers.mandate import AllMandatesHandler
from politicos.handlers.mandate_events import AllMandateEventsHandler
from politicos.handlers.mandate_events_type import (
    MandateEventsTypeHandler, AllMandateEventsTypesHandler
)
from politicos.handlers.institution import (
    InstitutionHandler, AllInstitutionsHandler
)
from politicos.handlers.political_office import (
    PoliticalOfficeHandler, AllPoliticalOfficesHandler
)


def main():
    AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
    PoliticosApiServer.run()


class VersionHandler(BaseHandler):
    def get(self):
        self.write(__version__)


class PoliticosApiServer(Server):
    def __init__(self, db=None, debug=None, *args, **kw):
        super(PoliticosApiServer, self).__init__(*args, **kw)
        self.force_debug = debug
        self.db = db

    def get_extra_server_parameters(self):
        return {
            'no_keep_alive': False
        }

    def initialize_app(self, *args, **kw):
        super(PoliticosApiServer, self).initialize_app(*args, **kw)
        self.application.db = None
        if self.force_debug is not None:
            self.debug = self.force_debug

    def get_handlers(self):
        handlers = [
            url(
                r'/institutions/',
                AllInstitutionsHandler,
                name='institutions'
            ),
            url(
                r'/institutions/(?P<siglum>[A-Za-z0-9\.]+)',
                InstitutionHandler,
                name='institution'
            ),
            url(
                r'/political-parties/',
                AllPoliticalPartyHandler,
                name='political-parties'
            ),
            url(
                r'/political-parties/(?P<siglum>[A-Za-z0-9\.]+)',
                PoliticalPartyHandler,
                name='political-party'
            ),
            url(
                r'/political-offices/',
                AllPoliticalOfficesHandler,
                name='political-offices'
            ),
            url(
                r'/political-offices/(?P<slug>[a-z0-9-]+)',
                PoliticalOfficeHandler,
                name='political-office'
            ),
            url(
                r'/legislators/',
                AllLegislatorsHandler,
                name='legislators'
            ),
            url(
                r'/legislator-events/',
                AllLegislatorEventsHandler,
                name='legislator-events'
            ),
            url(
                r'/legislator-events-types/',
                AllLegislatorEventsTypesHandler,
                name='legislator-events-types'
            ),
            url(
                r'/legislator-events-types/(?P<slug>[a-z0-9-]+)',
                LegislatorEventsTypeHandler,
                name='legislator-events-type'
            ),
            url(
                r'/legislatures/',
                AllLegislaturesHandler,
                name='legislatures'
            ),
            url(
                r'/mandates/',
                AllMandatesHandler,
                name='mandates'
            ),
            url(
                r'/mandate-events/',
                AllMandateEventsHandler,
                name='mandate-events'
            ),
            url(
                r'/mandate-events-types/',
                AllMandateEventsTypesHandler,
                name='mandate-events-types'
            ),
            url(
                r'/mandate-events-types/(?P<slug>[a-z0-9-]+)',
                MandateEventsTypeHandler,
                name='mandate-events-type'
            ),
            url(
                r'/version',
                VersionHandler,
                name='version'
            ),
        ]

        return tuple(handlers)

    def get_plugins(self):
        return [
            SQLAlchemyPlugin
        ]

    def after_start(self, io_loop):
        if self.db is not None:
            self.application.db = self.db
        else:
            self.application.db = self.application.get_sqlalchemy_session()

        if self.debug:
            from sqltap import sqltap
            self.sqltap = sqltap.start()

        self.application.error_handlers = []
        for handler in self._load_error_handlers():
            self.application.error_handlers.append(
                handler(self.application.config)
            )
        self.application.http_client = AsyncHTTPClient(io_loop=io_loop)

    def _load_error_handlers(self):
        return load_classes(default=self.config.ERROR_HANDLERS)

    def before_end(self, io_loop):
        self.application.db.remove()

        if self.debug and getattr(self, 'sqltap', None) is not None:
            from sqltap import sqltap
            statistics = self.sqltap.collect()
            sqltap.report(statistics, "report.html")

if __name__ == '__main__':
    main()
