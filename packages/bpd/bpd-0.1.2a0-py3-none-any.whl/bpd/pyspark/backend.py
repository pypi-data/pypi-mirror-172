from bpd import _DEFAULT_BACKEND_, _SPARK_
from bpd import cfg
import os

spark = None
if _DEFAULT_BACKEND_ == _SPARK_:
    from pyspark.sql import SparkSession
    if "SPARK_MASTER" in os.environ:
        spark = SparkSession.builder.master(os.environ["SPARK_MASTER"]).getOrCreate()
    else:
        if cfg.spark_master is None:
            spark = SparkSession.builder\
                .getOrCreate()
        else:
            spark = SparkSession.builder.master(cfg.spark_master).getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")