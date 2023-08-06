import unittest

from gnutools.remote import gdrivezip

import bpd
from bpd import _DASK_, _SPARK_, init, cfg
from bpd.dask import DaskDataFrame
from bpd.pyspark import PySparkDataFrame


class TestBPD(unittest.TestCase):
    def test_download_gdrive_PySparkDataFrame(self):
        init(_SPARK_)
        PySparkDataFrame(gdrivezip(cfg.gdrive.diabetes)[0]).show()

    def test_download_gdrive_DaskDataFrame(self):
        init(_DASK_)
        DaskDataFrame(gdrivezip(cfg.gdrive.diabetes)[0]).display()

    def test_pipelines(self):
        from gnutools import fs
        from gnutools.remote import gdrivezip

        from bpd.dask import DataFrame
        from bpd.dask import functions as F
        from bpd.dask import udf
        from bpd.dask.pipelines import group_on, pipeline, select_cols

        # Register a user-defined function
        @udf
        def word(f):
            return fs.name(fs.parent(f))

        # Display the dataframe
        # Retrieve the first 3 filename per classe
        @udf
        def initial(classe):
            return classe[0]

        @udf
        def lists(classes):
            return list(set(classes))

        # Import a sample dataset
        gdrivezip("gdrive://1y4gwaS7LjYUhwTex1-lNHJJ71nLEh3fE")
        df = DataFrame(
            {
                "filename": fs.listfiles(
                    "/tmp/1y4gwaS7LjYUhwTex1-lNHJJ71nLEh3fE", [".wav"]
                )
            }
        )
        df.compute()
        df.run_pipelines(
            [
                {
                    select_cols: ("filename",),
                    pipeline: (
                        ("classe", word(F.col("filename"))),
                        ("name", udf(fs.name)(F.col("filename"))),
                    ),
                },
                {
                    group_on: "classe",
                    select_cols: ("name",),
                    pipeline: (("initial", initial(F.col("classe"))),),
                },
                {
                    group_on: "initial",
                    select_cols: ("classe",),
                    pipeline: (("_initial", lists(F.col("classe"))),),
                },
            ]
        ).withColumnRenamed("_initial", "initial").compute()


if __name__ == "__main__":
    unittest.main()
