from contextlib import contextmanager
from functools import wraps, cache
from time import time


class Context:
    name: str
    children: list["Context"]
    context_time: float = 0.0
    __start_time: float = time()
    __end_time: float = time()

    def __init__(self, name: str, parent: "Context | None" = None):
        self.name = name
        self.parent = parent
        self.children = []

    def enter_context(self):
        self.__start_time = time()

    def exit_context(self):
        self.__end_time = time()
        self.context_time += self.__end_time - self.__start_time

    def add_child(self, child: "Context") -> "Context":
        self.children.append(child)
        return child

    @cache
    def total_time(self):
        return self.context_time + sum(child.total_time() for child in self.children)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Context '{self.name}' context_time={self.context_time} total_time={self.total_time()}>"


_TRACING = False
_CURRENT_CONTEXT: Context | None = None


@contextmanager
def enter(name: str):
    global _CURRENT_CONTEXT
    context = _CURRENT_CONTEXT
    if context is None:
        raise RuntimeError("No context available.")
    child = context.add_child(Context(name, context))
    context.exit_context()
    child.enter_context()
    _CURRENT_CONTEXT = child
    try:
        yield child
    finally:
        child.exit_context()
        context.enter_context()
        _CURRENT_CONTEXT = context


def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not _TRACING:
            return func(*args, **kwargs)
        with enter(func.__name__):
            result = func(*args, **kwargs)
        return result

    return wrapper


def show_context_tree(context: Context):
    from itertools import count
    from dataclasses import dataclass, field

    @dataclass
    class Point:
        x: float
        y: float
        context: Context
        id: int = field(default_factory=count().__next__)

    @dataclass
    class Edge:
        start: tuple[float, float]
        end: tuple[float, float]

    points = []
    edges = []

    def dfs(context: Context, bounds: tuple[float, float], depth: int = 0) -> Point:
        num_children = len(context.children)
        point = Point((bounds[0] + bounds[1]) / 2, depth, context)
        points.append(point)
        if num_children == 0:
            return point
        child_bound_length = (bounds[1] - bounds[0]) / num_children if num_children > 0 else 0
        for i, child in enumerate(context.children):
            child_point = dfs(child, (bounds[0] + i * child_bound_length, bounds[0] + (i + 1) * child_bound_length),
                              depth - 1)
            edges.append(Edge((point.x, point.y), (child_point.x, child_point.y)))
        return point

    dfs(context, (0, 1))

    import plotly.graph_objects as go
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[coord for edge in edges for coord in (edge.start[0], edge.end[0], None)],
                             y=[coord for edge in edges for coord in (edge.start[1], edge.end[1], None)],
                             mode='lines',
                             line=dict(color='rgb(210,210,210)', width=1),
                             hoverinfo='none'
                             ))

    fig.add_trace(go.Scatter(x=[point.x for point in points],
                             y=[point.y for point in points],
                             mode='markers',
                             name='Trace',
                             marker=dict(symbol='circle-dot',
                                         size=18,
                                         color=[point.context.context_time for point in points],  # '#DB4551',
                                         line=dict(color='rgb(50,50,50)', width=1)
                                         ),
                             text=[repr(point.context) for point in points],
                             hoverinfo='text',
                             opacity=0.8
                             ))

    fig.show()


def show_context_bars(context: Context):
    import plotly.graph_objects as go
    ids = []
    parents = []
    times = []
    labels = []

    def dfs(context: Context, parent_id: str = ""):
        self_id = str(len(ids))
        ids.append(self_id)
        parents.append(parent_id)
        labels.append(context.name)
        times.append(context.total_time())
        for child in context.children:
            dfs(child, self_id)

    dfs(context)

    import plotly.graph_objects as go

    fig = go.Figure(go.Icicle(
        ids=ids,
        labels=labels,
        parents=parents,
        values=times,
        branchvalues="total",
        marker=dict(
            colorscale="RdBu",
            line=dict(width=2),
        ),
        texttemplate="%{label}<br>%{value}",
        tiling=dict(
            orientation="v",
            flip="x"
        )
    ))
    fig.show()


@contextmanager
def start_tracing(context_name: str):
    global _TRACING
    global _CURRENT_CONTEXT
    if _TRACING:
        raise RuntimeError("Tracing already started.")
    _TRACING = True
    _CURRENT_CONTEXT = Context(context_name)
    try:
        yield _CURRENT_CONTEXT
    finally:
        _CURRENT_CONTEXT = None
        _TRACING = False


@contextmanager
def no_trace():
    global _TRACING
    global _CURRENT_CONTEXT
    _TRACING = False
    try:
        yield
    finally:
        _TRACING = True
