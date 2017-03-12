from datetime import datetime
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text, String
from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections
from .common import PicasoDocType



class Node(PicasoDocType):
    _id = String()
    owner = String()
    description = String()

    class Meta:
        index = 'nodes'


class NodeParent(PicasoDocType):
    _id = String()
    parent_id = String()

    class Meta:
        index = 'nodes_parents'

    @staticmethod
    def get_children(node_id):
        search = NodeParent.search();
        return search.query("match", parent_id=node_id) \
            .execute()['hits']['hits']


class Edge(PicasoDocType):
    to_node = String()
    from_node = String()

    class Meta:
        index = 'edges'

    @staticmethod
    def get_connections(to_node):
        search = Edge.search()
        return search.query("match", to_node=to_node) \
            .execute()['hits']['hits']


class ElasticNodes(object):
    def get_connections(self, node_id):
        return Node.get(id=node_id)

    def get_node_children(self, node_id):
        return NodeParent.get_children()

    def get_node_connections(self, node_id):
        return Edge.get_connections(node_id)
