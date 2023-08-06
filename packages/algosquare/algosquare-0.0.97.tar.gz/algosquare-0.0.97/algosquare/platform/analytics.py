import numpy as np
import pandas as pd
import datetime
from sklearn.preprocessing import KBinsDiscretizer

from ..base.types import Metatype

def compute_score_dependencies(X, y, X_metatypes, pred, metric, X_features = None, max_x_categories = 20):
    """
    Computes dependencies between X and y data.

    Args:
        X: DataFrame with shape (n_samples, n_features).
        y: DataFrame with shape (n_samples, n_outputs).
        X_metatypes: list of n_features Metatypes.
        pred: predictions from a model.
        metric: Metric.
        X_features: set of X columns to evaluate.
        max_x_categories: maximum number of categories in feature to consider.
    """
    output = []
    for x_name, x_metatype in zip(X, X_metatypes):
        if X_features is None or x_name in X_features:
            x_filtered = X[x_name].dropna()
            x, x_categories, x_labels = _make_x_categories(x_filtered, x_metatype, max_x_categories)
           
            y_filtered = y.loc[x_filtered.index]
            pred_filtered = pred.loc[x_filtered.index]

            data = _compute_scores(x, x_categories, y_filtered, pred_filtered, metric, x_labels)

            output.append(dict(x_series = x_name, x_metatype = Metatype(x_metatype).name.lower(), data = data))
    return output

def _compute_scores(x, x_categories, y, pred, metric, x_labels = None):
    output = []
    
    if x_labels is None:
        x_labels = [str(cat) for cat in x_categories]
    
    for cat, label in zip(x_categories, x_labels):
        y_selection = y.loc[x==cat]
        pred_selection = pred.loc[x==cat]
        score = metric.score(y_selection, pred_selection)
        output.append(dict(label = label, score = score, n = y_selection.shape[0]))
    return output

def make_dependency_graphs(X, y, X_metatypes, y_metatypes, X_features = None, max_x_categories = 20, max_y_categories = 20):
    """
    Computes dependencies between X and y data.

    Args:
        X: DataFrame with shape (n_samples, n_features).
        y: DataFrame with shape (n_samples, n_outputs).
        X_metatypes: list of n_features Metatypes.
        y_metatypes: list of n_outputs Metatypes.
        X_features: set of X columns to evaluate.
        max_x_categories: maximum number of categories in feature to consider.
        max_y_categories: maximum number of categories in target to consider.
    """
    output = []
    for x_name, x_metatype in zip(X, X_metatypes):
        if X_features is None or x_name in X_features:
            x_filtered = X[x_name].dropna()
            x, x_categories, x_labels = _make_x_categories(x_filtered, x_metatype, max_x_categories)
            data = []
            for y_name, y_metatype in zip(y, y_metatypes):
                y_filtered = y[y_name].loc[x_filtered.index]
                charts = _make_charts(x, x_categories, y_filtered, y_metatype, max_y_categories, x_labels)
                data.append(charts)

            output.append(dict(x_series = x_name, data = data))
    return output

def _make_x_categories(x, x_metatype, max_x_categories):
    unique = x.unique()
    if len(unique) <= max_x_categories:
        return (x, list(unique), None)

    if x_metatype == Metatype.DATETIME:
        x_timestamp = pd.to_datetime(x).apply(lambda x: x.timestamp())
        return _make_x_bins(x_timestamp, Metatype.TIMESTAMP, max_x_categories)
    elif x_metatype in (Metatype.NUMERICAL, Metatype.TIMESTAMP):
        return _make_x_bins(x, x_metatype, max_x_categories)
    elif x_metatype in (Metatype.BINARY, Metatype.CATEGORICAL):
        counts = x.value_counts()
        x_categories = list(counts.index[:max_x_categories])
        return (x, x_categories, None)

    raise ValueError('unsupported x_metatype')

def _make_x_bins(x, x_metatype, max_x_categories):
    n_bins = min(max(4, int(x.shape[0] / 30)), max_x_categories)
    encoder = KBinsDiscretizer(n_bins = n_bins, encode='ordinal')
    x_transform = encoder.fit_transform(x.astype(float).to_frame())
    x_labels = _make_bin_labels(encoder.bin_edges_[0], x_metatype)
    return (x_transform, list(range(encoder.n_bins_[0])), x_labels)

def _make_charts(x, x_categories, y, y_metatype, max_y_categories, x_labels = None):
    charts = []
    if x_labels is None:
        x_labels = [str(cat) for cat in x_categories]
    
    if y_metatype == Metatype.NUMERICAL:
        series = []
        for x_cat, x_label in zip(x_categories, x_labels):
            #make boxplot
            y_selection = y.loc[x==x_cat] 
            quantiles = y_selection.quantile([0,0.25,0.5,0.75,1])
            series.append(list(quantiles.values.squeeze()))
        
        charts.append(dict(chart = 'boxplot', x_categories = x_labels, series = dict(name = y.name, data = series)))
    elif y_metatype in (Metatype.BINARY, Metatype.CATEGORICAL):
        y_categories = list(y.unique())
        if len(y_categories) <= max_y_categories:
            y_categories.sort()
            series = dict()
            for x_cat, x_label in zip(x_categories, x_labels):
                y_selection = y.loc[x==x_cat]
                counts = y_selection.value_counts(sort=False)
                for y_cat in y_categories:
                    if y_cat not in series:
                        series[y_cat] = []
                    series[y_cat].append(counts.get(y_cat,0))
            charts.append(dict(chart = 'bar', x_categories = x_labels, series = [dict(name = k, data = v) for k, v in series.items()]))
        else:
            for x_cat, x_label in zip(x_categories, x_labels):
                y_selection = y.loc[x==x_cat] 
                counts = y_selection.value_counts().iloc[:max_y_categories]
                stats = [dict(name = k, y = v) for k, v in counts.items()]
                charts.append(dict(chart = 'pie', series = dict(name = x_label, data = stats)))

    else:
        raise ValueError('unsupported y_metatype')
    
    return dict(y_series = y.name, charts = charts)

def _make_bin_labels(bin_edges, x_metatype):
    if x_metatype == Metatype.TIMESTAMP:
        datetimes = [datetime.datetime.fromtimestamp(x, datetime.timezone.utc) for x in bin_edges]
        return _make_datetime_labels(datetimes)
    elif x_metatype == Metatype.NUMERICAL:
        return [f'{left:.2e}|{right:.2e}' for left, right in zip(bin_edges[:-1], bin_edges[1:])]
    raise ValueError('unsupported x_metatype')

def _make_datetime_labels(datetimes):
    labels = []
    last_date = None
    for left, right in zip(datetimes[:-1], datetimes[1:]):
        show_left_date = show_right_date = False
        if last_date is None or left.date() != last_date:
            show_left_date = True
            last_date = left.date()

        if right.date() != last_date:
            show_right_date = True
            last_date = right.date()

        timedelta = right - left

        if timedelta.days == 0:
            if timedelta.seconds > 60:
                fmt_time = '%H:%M'
            elif timedelta.seconds > 0:
                fmt_time = '%H:%M:%S'
            else:
                fmt_time = '%H:%M:%S.%f'

            fmt_left = '%Y-%m-%d ' + fmt_time if show_left_date else fmt_time
            fmt_right = '%Y-%m-%d ' + fmt_time if show_right_date else fmt_time
        else:
            fmt_left = fmt_right = '%Y-%m-%d'
        labels.append(f'{left.strftime(fmt_left)}|{right.strftime(fmt_right)}')
    return labels