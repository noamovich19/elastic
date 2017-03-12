from common import PicasoDocType

from datetime import datetime
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text, String
from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections


class Metric(PicasoDocType):
    node_id = String()

    class Meta:
        index = "metrics"

    def save(self, metrics=[], **kwargs):
        for metric in metrics:
            setattr(metric["metric_name"], metric["metric_value"])
        super(Metric, self).save(**kwargs)

    @staticmethod
    def get_single_metric_aggregetion(metric_name, agg_function):
        search = Metric.search()
        search.aggs.metric(agg_function, name=metric_name, field=metric_name)

    @staticmethod
    def get_metrics():
        pass

    @staticmethod
    def get_graph():
        pass
