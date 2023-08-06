from gnutools.fs import load_config, parent
from pyspark.sql.utils import AnalysisException

cfg = load_config(f"{parent(__file__)}/config.yml")
__version__ = "0.1.2a0"
_DEFAULT_BACKEND_ = cfg.default_backend
_SPARK_ = cfg.spark
_DASK_ = cfg.dask
_PANDAS_ = cfg.pandas
_DASK_ENDPOINT_ = cfg.dask_endpoint
_APP_NAME_ = cfg.project

def init(_backend):
    assert _backend in [_SPARK_, _DASK_, _PANDAS_]
    global _DEFAULT_BACKEND_
    _DEFAULT_BACKEND_ = _backend
    if _DEFAULT_BACKEND_ == _DASK_:
        from bpd.dask.backend import client

        return client
    elif _DEFAULT_BACKEND_ == _SPARK_:
        from bpd.pyspark.backend import spark

        return spark

