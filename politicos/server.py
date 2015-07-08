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
        siglum_regex = r'[A-Za-z0-9\.]+'
        slug_regex = r'[a-z0-9-]+'
        # numbers_regex = r'[0-9]+'

        handlers = [
            ('/institutions/?', AllInstitutionsHandler),
            ('/institutions/(%s)/?' % siglum_regex, InstitutionHandler),
            ('/political-parties/?', AllPoliticalPartyHandler),
            (
                '/political-parties/(%s)/?' % siglum_regex,
                PoliticalPartyHandler),
            ('/political-offices/?', AllPoliticalOfficesHandler),
            ('/political-offices/(%s)/?' % slug_regex, PoliticalOfficeHandler),
            ('/legislators/?', AllLegislatorsHandler),
            ('/legislator-events/?', AllLegislatorEventsHandler),
            ('/legislator-events-types/?', AllLegislatorEventsTypesHandler),
            (
                '/legislator-events-types/(%s)/?' % slug_regex,
                LegislatorEventsTypeHandler),
            ('/legislatures/?', AllLegislaturesHandler),
            ('/mandates/?', AllMandatesHandler),
            ('/mandate-events/?', AllMandateEventsHandler),
            ('/mandate-events-types/?', AllMandateEventsTypesHandler),
            (
                '/mandate-events-types/(%s)/?' % slug_regex,
                MandateEventsTypeHandler),
            ('/version/?', VersionHandler),
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
