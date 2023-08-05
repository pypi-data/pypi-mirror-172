# mysql/mysqldb.py
# Copyright (C) 2005-2022 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

"""

.. dialect:: mysql+mysqldb
    :name: mysqlclient (maintained fork of MySQL-Python)
    :dbapi: mysqldb
    :connectstring: mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>
    :url: https://pypi.org/project/mysqlclient/

Driver Status
-------------

The mysqlclient DBAPI is a maintained fork of the
`MySQL-Python <https://sourceforge.net/projects/mysql-python>`_ DBAPI
that is no longer maintained.  `mysqlclient`_ supports Python 2 and Python 3
and is very stable.

.. _mysqlclient: https://github.com/PyMySQL/mysqlclient-python

.. _mysqldb_unicode:

Unicode
-------

Please see :ref:`mysql_unicode` for current recommendations on unicode
handling.

.. _mysqldb_ssl:

SSL Connections
----------------

The mysqlclient and PyMySQL DBAPIs accept an additional dictionary under the
key "ssl", which may be specified using the
:paramref:`_sa.create_engine.connect_args` dictionary::

    engine = create_engine(
        "mysql+mysqldb://scott:tiger@192.168.0.134/test",
        connect_args={
            "ssl": {
                "ssl_ca": "/home/gord/client-ssl/ca.pem",
                "ssl_cert": "/home/gord/client-ssl/client-cert.pem",
                "ssl_key": "/home/gord/client-ssl/client-key.pem"
            }
        }
    )

For convenience, the following keys may also be specified inline within the URL
where they will be interpreted into the "ssl" dictionary automatically:
"ssl_ca", "ssl_cert", "ssl_key", "ssl_capath", "ssl_cipher",
"ssl_check_hostname". An example is as follows::

    connection_uri = (
        "mysql+mysqldb://scott:tiger@192.168.0.134/test"
        "?ssl_ca=/home/gord/client-ssl/ca.pem"
        "&ssl_cert=/home/gord/client-ssl/client-cert.pem"
        "&ssl_key=/home/gord/client-ssl/client-key.pem"
    )

If the server uses an automatically-generated certificate that is self-signed
or does not match the host name (as seen from the client), it may also be
necessary to indicate ``ssl_check_hostname=false``::

    connection_uri = (
        "mysql+pymysql://scott:tiger@192.168.0.134/test"
        "?ssl_ca=/home/gord/client-ssl/ca.pem"
        "&ssl_cert=/home/gord/client-ssl/client-cert.pem"
        "&ssl_key=/home/gord/client-ssl/client-key.pem"
        "&ssl_check_hostname=false"
    )


.. seealso::

    :ref:`pymysql_ssl` in the PyMySQL dialect


Using MySQLdb with Google Cloud SQL
-----------------------------------

Google Cloud SQL now recommends use of the MySQLdb dialect.  Connect
using a URL like the following::

    mysql+mysqldb://root@/<dbname>?unix_socket=/cloudsql/<projectid>:<instancename>

Server Side Cursors
-------------------

The mysqldb dialect supports server-side cursors. See :ref:`mysql_ss_cursors`.

"""

import re

from .base import MySQLCompiler
from .base import MySQLDialect
from .base import MySQLExecutionContext
from .base import MySQLIdentifierPreparer
from .base import TEXT
from ... import sql
from ... import util


class MySQLExecutionContext_mysqldb(MySQLExecutionContext):
    @property
    def rowcount(self):
        if hasattr(self, "_rowcount"):
            return self._rowcount
        else:
            return self.cursor.rowcount


class MySQLCompiler_mysqldb(MySQLCompiler):
    pass


class MySQLDialect_mysqldb(MySQLDialect):
    driver = "mysqldb"
    supports_statement_cache = True
    supports_unicode_statements = True
    supports_sane_rowcount = True
    supports_sane_multi_rowcount = True

    supports_native_decimal = True

    default_paramstyle = "format"
    execution_ctx_cls = MySQLExecutionContext_mysqldb
    statement_compiler = MySQLCompiler_mysqldb
    preparer = MySQLIdentifierPreparer

    def __init__(self, **kwargs):
        super(MySQLDialect_mysqldb, self).__init__(**kwargs)
        self._mysql_dbapi_version = (
            self._parse_dbapi_version(self.dbapi.__version__)
            if self.dbapi is not None and hasattr(self.dbapi, "__version__")
            else (0, 0, 0)
        )

    def _parse_dbapi_version(self, version):
        m = re.match(r"(\d+)\.(\d+)(?:\.(\d+))?", version)
        if m:
            return tuple(int(x) for x in m.group(1, 2, 3) if x is not None)
        else:
            return (0, 0, 0)

    @util.langhelpers.memoized_property
    def supports_server_side_cursors(self):
        try:
            cursors = __import__("MySQLdb.cursors").cursors
            self._sscursor = cursors.SSCursor
            return True
        except (ImportError, AttributeError):
            return False

    @classmethod
    def dbapi(cls):
        return __import__("MySQLdb")

    def on_connect(self):
        super_ = super(MySQLDialect_mysqldb, self).on_connect()

        def on_connect(conn):
            if super_ is not None:
                super_(conn)

            charset_name = conn.character_set_name()

            if charset_name is not None:
                cursor = conn.cursor()
                cursor.execute("SET NAMES %s" % charset_name)
                cursor.close()

        return on_connect

    def do_ping(self, dbapi_connection):
        try:
            dbapi_connection.ping(False)
        except self.dbapi.Error as err:
            if self.is_disconnect(err, dbapi_connection, None):
                return False
            else:
                raise
        else:
            return True

    def do_executemany(self, cursor, statement, parameters, context=None):
        rowcount = cursor.executemany(statement, parameters)
        if context is not None:
            context._rowcount = rowcount

    def _check_unicode_returns(self, connection):
        # work around issue fixed in
        # https://github.com/farcepest/MySQLdb1/commit/cd44524fef63bd3fcb71947392326e9742d520e8
        # specific issue w/ the utf8mb4_bin collation and unicode returns

        collation = connection.exec_driver_sql(
            "show collation where %s = 'utf8mb4' and %s = 'utf8mb4_bin'"
            % (
                self.identifier_preparer.quote("Charset"),
                self.identifier_preparer.quote("Collation"),
            )
        ).scalar()
        has_utf8mb4_bin = self.server_version_info > (5,) and collation
        if has_utf8mb4_bin:
            additional_tests = [
                sql.collate(
                    sql.cast(
                        sql.literal_column("'test collated returns'"),
                        TEXT(charset="utf8mb4"),
                    ),
                    "utf8mb4_bin",
                )
            ]
        else:
            additional_tests = []
        return super(MySQLDialect_mysqldb, self)._check_unicode_returns(
            connection, additional_tests
        )

    def create_connect_args(self, url, _translate_args=None):
        if _translate_args is None:
            _translate_args = dict(
                database="db", username="user", password="passwd"
            )

        opts = url.translate_connect_args(**_translate_args)
        opts.update(url.query)

        util.coerce_kw_type(opts, "compress", bool)
        util.coerce_kw_type(opts, "connect_timeout", int)
        util.coerce_kw_type(opts, "read_timeout", int)
        util.coerce_kw_type(opts, "write_timeout", int)
        util.coerce_kw_type(opts, "client_flag", int)
        util.coerce_kw_type(opts, "local_infile", int)
        # Note: using either of the below will cause all strings to be
        # returned as Unicode, both in raw SQL operations and with column
        # types like String and MSString.
        util.coerce_kw_type(opts, "use_unicode", bool)
        util.coerce_kw_type(opts, "charset", str)

        # Rich values 'cursorclass' and 'conv' are not supported via
        # query string.

        ssl = {}
        keys = [
            ("ssl_ca", str),
            ("ssl_key", str),
            ("ssl_cert", str),
            ("ssl_capath", str),
            ("ssl_cipher", str),
            ("ssl_check_hostname", bool),
        ]
        for key, kw_type in keys:
            if key in opts:
                ssl[key[4:]] = opts[key]
                util.coerce_kw_type(ssl, key[4:], kw_type)
                del opts[key]
        if ssl:
            opts["ssl"] = ssl

        # FOUND_ROWS must be set in CLIENT_FLAGS to enable
        # supports_sane_rowcount.
        client_flag = opts.get("client_flag", 0)

        client_flag_found_rows = self._found_rows_client_flag()
        if client_flag_found_rows is not None:
            client_flag |= client_flag_found_rows
            opts["client_flag"] = client_flag
        return [[], opts]

    def _found_rows_client_flag(self):
        if self.dbapi is not None:
            try:
                CLIENT_FLAGS = __import__(
                    self.dbapi.__name__ + ".constants.CLIENT"
                ).constants.CLIENT
            except (AttributeError, ImportError):
                return None
            else:
                return CLIENT_FLAGS.FOUND_ROWS
        else:
            return None

    def _extract_error_code(self, exception):
        return exception.args[0]

    def _detect_charset(self, connection):
        """Sniff out the character set in use for connection results."""

        try:
            # note: the SQL here would be
            # "SHOW VARIABLES LIKE 'character_set%%'"
            cset_name = connection.connection.character_set_name
        except AttributeError:
            util.warn(
                "No 'character_set_name' can be detected with "
                "this MySQL-Python version; "
                "please upgrade to a recent version of MySQL-Python.  "
                "Assuming latin1."
            )
            return "latin1"
        else:
            return cset_name()

    _isolation_lookup = set(
        [
            "SERIALIZABLE",
            "READ UNCOMMITTED",
            "READ COMMITTED",
            "REPEATABLE READ",
            "AUTOCOMMIT",
        ]
    )

    def _set_isolation_level(self, connection, level):
        if level == "AUTOCOMMIT":
            connection.autocommit(True)
        else:
            connection.autocommit(False)
            super(MySQLDialect_mysqldb, self)._set_isolation_level(
                connection, level
            )


dialect = MySQLDialect_mysqldb
