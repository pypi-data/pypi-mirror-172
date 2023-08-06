from pyspark.sql import DataFrame
from pyspark.sql.streaming import DataStreamWriter

from karadoc.common.job_core.has_output import HasOutput
from karadoc.spark.conf import (
    get_stream_default_output_format,
    get_write_options_for_format,
)


class HasStreamOutput(HasOutput):
    def __init__(self) -> None:
        super().__init__()
        self.output_format = get_stream_default_output_format()

    def write_table(self, df: DataFrame):
        return self._write_stream_table(
            stream_df=df,
            path=self.hdfs_output(),
            output_format=self.output_format,
            output_options=self.output_options,
            partitions=self.dynamic_partitions(),
        )

    @staticmethod
    def _write_stream_table(
        stream_df: DataFrame, path: str, output_format: str, output_options=None, partitions=None
    ) -> DataStreamWriter:
        if output_options is None:
            output_options = {}
        if partitions is None:
            partitions = []

        write_options = get_write_options_for_format(output_format)
        options = {**write_options, **output_options}

        return (
            stream_df.writeStream.partitionBy(partitions).option("path", path).options(**options).format(output_format)
        )
