from datetime import datetime
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text, String
from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections
import logging


LOGGER = logging.getLogger()


def log_search(execute_func):
    def wrapper(search_object, *args, **kwargs):
        response = execute_func(*args, **kwargs)
        LOGGER.info(
            "quering: {} "
            "timed out {} "
            "total {} "
            "took {} ".format(
                str(search_object),
                response['timed_out'],
                response['total']),
            response['took'])
        return response

    return wrapper


def check_time_out(execute_func):
    def wrapper(search_object, *args, **kwargs):
        response = execute_func(*args, **kwargs)
        if response['timed_out']:
            LOGGER.error("query {} timed out, took {}"
                         .format(str(search_object), response['took']))

    return wrapper


class ProxySearch(object):
    def __init__(self, search):
        self.search = search

    def __getattr__(self, item):
        return getattr(self.search, item)

    def __str__(self):
        return "quering index {} doc type {} query {} " \
            .format(self.index, self.doc_type, self.to_dict())

    @log_search
    @check_time_out
    def _execute(self, search_object, *args, **kwargs):
        return self.search.execute(args, **kwargs)

    def execute(self, *args, **kwargs):
        return self._execute(self.search, *args, **kwargs)


class PicasoDocType(DocType):
    def save(self, **kwargs):
        setattr(self, "_save_time", datetime.now())
        return super(PicasoDocType, self).save(**kwargs)

    @classmethod
    def search(cls, using=None, index=None):
        return ProxySearch(
            Search(
                using=using or cls._doc_type.using,
                index=index or cls._doc_type.index,
                doc_type=[cls])
        )

