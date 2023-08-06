import os
import sys
from pathlib import Path
from typing import Optional

from pyspark.sql import SparkSession

from karadoc.common.conf import get_libs_folder_location


def get_spark_session(app_name: Optional[str] = None, extra_spark_conf: Optional[dict] = None) -> SparkSession:
    """Gets an existing :class:`SparkSession` or, if there is no existing one, creates a new one.

    Spark default settings can be set via the `{env}.spark.conf` in `settings.toml`, and can also be overridden
    using this method's optional argument `extra_spark_conf`.

    Example:

    In your settings.toml:

    .. code-block:: python

        # In settings.toml, this setting configures the default driver memory on all environments
        [default.spark.conf]
          spark.driver.memory="4g"

        # While this setting overrides the default driver memory in the "prod" environment
        [prod.spark.conf]
          spark.driver.memory="6g"

    # It can also be overridden via the command line for a specific job like this :
    karadoc run --spark-conf spark.driver.memory=8g ...

    :param app_name:
    :param extra_spark_conf: Spark configuration parameters to over
    :return:
    """
    # TODO: this late import is a temporary workaround for cyclic dependencies
    from karadoc.common import conf
    from karadoc.spark.conf import get_spark_conf

    if extra_spark_conf is None:
        extra_spark_conf = {}
    spark_conf = {**get_spark_conf(), **extra_spark_conf}
    builder: SparkSession.Builder = SparkSession.builder
    if conf.is_dev_env():
        builder = builder.master("local[4]")
    for k, v in spark_conf.items():
        builder = builder.config(k, v)
    if app_name is None:
        app_name = conf.APPLICATION_NAME.lower()
    spark: SparkSession = builder.appName(app_name).getOrCreate()
    _add_libs_folder_to_spark_python_path(spark)

    # As a workaround to this spark issue https://issues.apache.org/jira/browse/SPARK-38870,
    # we reset the builder options
    spark.Builder._options = {}
    return spark


def _add_libs_folder_to_spark_python_path(spark: SparkSession) -> None:
    # This simulates the first time the karadoc module is imported
    libs_folder = str(Path(get_libs_folder_location()).absolute())
    spark_env = spark.sparkContext.environment
    sys.path.extend([libs_folder])
    if "PYTHONPATH" not in spark_env:
        spark_env["PYTHONPATH"] = libs_folder
    else:
        spark_env["PYTHONPATH"] += os.pathsep + libs_folder
