from bpd import _DASK_, _DASK_ENDPOINT_, _DEFAULT_BACKEND_

client = None
if _DEFAULT_BACKEND_ == _DASK_:
    from distributed import Client
    client = Client(_DASK_ENDPOINT_)
