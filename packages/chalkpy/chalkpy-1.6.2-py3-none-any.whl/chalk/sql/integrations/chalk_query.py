import logging
import time
from collections import defaultdict
from enum import Enum
from typing import Any, Dict, List, Mapping, Optional, Union

import numpy as np
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine.row import Row

from chalk.features import Feature
from chalk.features.feature import FeatureSetBase
from chalk.sql.base.protocols import (
    BaseSQLSourceProtocol,
    ChalkQueryProtocol,
    DBSessionProtocol,
    IncrementalSettings,
    StringChalkQueryProtocol,
)
from chalk.utils.collections import get_unique_item


class Finalizer(str, Enum):
    OneOrNone = "OneOrNone"
    One = "One"
    First = "First"
    All = "All"


_logger = logging.getLogger(__name__)


def _construct_features(cols: Union[List[Feature], Dict[str, Feature]], tuples: Optional[Row]):
    root_ns = get_unique_item(
        (f.root_namespace for f in (cols.values() if isinstance(cols, dict) else cols)), "root ns"
    )
    features_cls = FeatureSetBase.registry[root_ns]
    kwargs = {}

    if isinstance(cols, dict):
        row = dict(tuples) if tuples is not None else {}
        for k, feature in cols.items():
            assert feature.attribute_name is not None
            kwargs[feature.attribute_name] = row[k]
    else:
        assert tuples is not None
        assert len(tuples) == len(cols)
        for feature, val in zip(cols, tuples):
            assert feature.attribute_name is not None
            kwargs[feature.attribute_name] = val  # row[feature.name]
    return features_cls(**kwargs)


class StringChalkQuery(StringChalkQueryProtocol):
    def __init__(
        self,
        session: DBSessionProtocol,
        source: BaseSQLSourceProtocol,
        query: str,
        fields: Mapping[str, Union[Feature, str]],
        args: Optional[Mapping[str, str]],
    ):
        self._finalizer: Optional[Finalizer] = None
        self._session = session
        self._source = source
        self._query = text(query)
        self._fields = fields
        self._incremental_settings: Optional[Union[IncrementalSettings, bool]] = None
        if args is not None:
            self._query = self._query.bindparams(**args)

    def one_or_none(self):
        self._finalizer = Finalizer.OneOrNone
        return self

    def one(self):
        self._finalizer = Finalizer.One
        return self

    def all(self, incremental: Union[bool, IncrementalSettings] = False):
        self._finalizer = Finalizer.All
        if isinstance(incremental, bool) and incremental:
            self._incremental_settings = IncrementalSettings(lookback_period=None)
        elif isinstance(incremental, IncrementalSettings):
            self._incremental_settings = incremental
        return self

    def execute(self):
        tuples = self._session.execute(self._query)
        cols = {k: Feature.from_root_fqn(v) if isinstance(v, str) else v for (k, v) in self._fields.items()}
        self._finalizer = self._finalizer or Finalizer.All

        if self._finalizer == Finalizer.All:
            data = [list(tup[field] for (field, _) in self._fields.items()) for tup in tuples]
            df = pd.DataFrame(
                data=data,
                columns=list(cols.values()),
            )
            df.replace({np.nan: None}, inplace=True)
            from chalk.df.ChalkDataFrameImpl import ChalkDataFrameImpl

            return ChalkDataFrameImpl(df)

        tups = list(tuples)
        tup = None
        if self._finalizer == Finalizer.One:
            if len(tups) == 1:
                tup = tups[0]
            else:
                raise ValueError("Expected exactly one result")

        if self._finalizer == Finalizer.First:
            if len(tups) > 1:
                tup = tups[0]
            else:
                raise ValueError("Expected at least one result")

        if self._finalizer == Finalizer.OneOrNone and len(tups) > 0:
            tup = tups[0]

        return _construct_features(cols, tup)


class ChalkQuery(ChalkQueryProtocol):
    _session: DBSessionProtocol
    _source: BaseSQLSourceProtocol
    _features: List[Feature]
    _finalizer: Optional[Finalizer]
    _incremental_settings: Optional[Union[IncrementalSettings, bool]]

    def __init__(
        self,
        features: List[Feature],
        session: DBSessionProtocol,
        source: BaseSQLSourceProtocol,
        raw_session: Optional[Any] = None,
    ):
        self._session = session
        self._raw_session = raw_session or session
        self._features = features
        self._finalizer = None
        self._source = source
        self._incremental_settings = None

    def first(self):
        self._session.update_query(lambda x: x.limit(1))
        self._finalizer = Finalizer.First
        return self

    def one_or_none(self):
        self._session.update_query(lambda x: x.limit(1))
        self._finalizer = Finalizer.OneOrNone
        return self

    def one(self):
        self._session.update_query(lambda x: x.limit(1))
        self._finalizer = Finalizer.One
        return self

    def all(self, incremental: Union[bool, IncrementalSettings] = False):
        self._finalizer = Finalizer.All
        if isinstance(incremental, bool) and incremental:
            self._incremental_settings = IncrementalSettings(lookback_period=None)
        elif isinstance(incremental, IncrementalSettings):
            self._incremental_settings = incremental
        return self

    def filter_by(self, **kwargs):
        self._session.update_query(lambda x: x.filter_by(**kwargs))
        return self

    def filter(self, *criterion):
        self._session.update_query(lambda x: x.filter(*criterion))
        return self

    def limit(self, *limits):
        self._session.update_query(lambda x: x.limit(*limits))
        return self

    def order_by(self, *clauses):
        self._session.update_query(lambda x: x.order_by(*clauses))
        return self

    def group_by(self, *clauses):
        self._session.update_query(lambda x: x.group_by(*clauses))
        return self

    def having(self, criterion):
        self._session.update_query(lambda x: x.having(*criterion))
        return self

    def union(self, *q):
        self._session.update_query(lambda x: x.union(*q))
        return self

    def union_all(self, *q):
        self._session.update_query(lambda x: x.union_all(*q))
        return self

    def intersect(self, *q):
        self._session.update_query(lambda x: x.intersect(*q))
        return self

    def intersect_all(self, *q):
        self._session.update_query(lambda x: x.intersect_all(*q))
        return self

    def join(self, target, *props, **kwargs):
        self._session.update_query(lambda x: x.join(target, *props, **kwargs))
        return self

    def outerjoin(self, target, *props, **kwargs):
        self._session.update_query(lambda x: x.outerjoin(target, *props, **kwargs))
        return self

    def select_from(self, *from_obj):
        self._session.update_query(lambda x: x.select_from(*from_obj))
        return self

    @staticmethod
    def _get_finalizer_fn(f: Optional[Finalizer]):
        if f == Finalizer.First:
            return lambda x: x.first()
        if f == Finalizer.All:
            return lambda x: x.all()
        if f == Finalizer.One:
            return lambda x: x.one()
        if f == Finalizer.OneOrNone:
            return lambda x: x.one_or_none()
        if f is None:
            return lambda x: x.all()
        raise ValueError(f"Unknown finalizer {f}")

    def execute(self):
        from chalk.serialization.codec import FeatureCodec

        codec = FeatureCodec()
        start = time.perf_counter()
        try:
            column_descriptions = self._session._session.column_descriptions
            self._session.update_query(self._get_finalizer_fn(self._finalizer))
            tuples = self._session.result()
            self._raw_session.close()
            fqn_to_feature = {f.fqn: f for f in self._features}
            cols = [fqn_to_feature[value["name"]] for value in column_descriptions if value["name"] in fqn_to_feature]

            if isinstance(tuples, list):
                lists = defaultdict(list)

                for tuple in tuples:
                    for col_i, x in enumerate(tuple):
                        if isinstance(x, Enum):
                            x = x.value
                        lists[col_i].append(x)

                df = pd.DataFrame(
                    {col: pd.Series(lists[i], dtype=codec.get_pandas_dtype(fqn=col.fqn)) for i, col in enumerate(cols)}
                )

                df.replace({np.nan: None, pd.NaT: None}, inplace=True)
                from chalk.df.ChalkDataFrameImpl import ChalkDataFrameImpl

                return ChalkDataFrameImpl(df)
            return _construct_features(cols, tuples)
        finally:
            _logger.debug(f"query.execute: {time.perf_counter() - start}")
