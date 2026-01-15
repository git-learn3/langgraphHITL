"""
Central registry for all subgraphs.
This is the ONLY place orch.py should import from.
"""

from graph.place_order.graph import build_place_order_graph
from graph.track_order.graph import build_track_order_graph
from graph.cancel_order.graph import build_cancel_order_graph


def load_subgraphs(checkpointer=None):
    """
    Returns compiled subgraphs.
    Allows injecting checkpointer / config later.
    """
    return {
        "place_order": build_place_order_graph(checkpointer),
        "track_order": build_track_order_graph(checkpointer),
        "cancel_order": build_cancel_order_graph(checkpointer),
    }
