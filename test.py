from elastic.nodes import *
from elastic.metrics import *


def set_indexes():
    nodes = [Node(_id=str(i), owner='noam', description="test") for i in range(1, 8)]
    nodes_parents = [
        NodeParent(_id="1", parent_id="root"),
        NodeParent(_id="2", parent_id="1"),
        NodeParent(_id="3", parent_id="1"),
        NodeParent(_id="4", parent_id="1"),
        NodeParent(_id="5", parent_id="1"),
        NodeParent(_id="6", parent_id="1"),
        NodeParent(_id="7", parent_id="3"),
        NodeParent(_id="8", parent_id="2"),
    ]
    edges = [
        Edge(from_node="3", to_node="4"),
        Edge(from_node="3", to_node="5"),
        Edge(from_node="4", to_node="5"),
        Edge(from_node="4", to_node="6"),
    ]

    metrics = [
        Metric(node_id="1", name="name1", met=123),
        Metric(node_id="2", name="name1", met=234),
        Metric(node_id="3", name="name2", met=324),
        Metric(node_id="4", name="name3", met=534),
        Metric(node_id="5", name="name3", met=89),
        Metric(node_id="6", name="name4", met=234),
    ]

    for metric in metrics:
        metric.save()

    for node in nodes:
        node.save()

    for node_p in nodes_parents:
        node_p.save()

    for e in edges:
        e.save()


# set_indexes()

