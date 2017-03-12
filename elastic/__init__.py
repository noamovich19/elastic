from elasticsearch_dsl.connections import connections
from .nodes import ElasticNodes

connections.create_connection(hosts=['localhost'])


