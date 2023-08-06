from typing import Dict, Union

from pyspark.sql import DataFrame

from karadoc.common.conf import CONNECTION_GROUP
from karadoc.common.job_core.has_spark import HasSpark


def _write_external_output_signature_check(df: DataFrame, dest: Dict) -> None:
    """We uses this empty method when to check the signature of the equivalent method defined in the POPULATE files"""
    pass


def _write_external_outputs_signature_check(df: DataFrame) -> None:
    """We uses this empty method when to check the signature of the equivalent method defined in the POPULATE files"""
    pass


class HasExternalOutputs(HasSpark):
    def __init__(self) -> None:
        super().__init__()
        # Attributes that the user may change
        self.external_outputs: Dict[str, dict] = {}

        # Attributes that the user is not supposed to change
        self.__write_external_output = None
        self.__write_external_outputs = None

    def _write_external_output_default(self, df: DataFrame, dest: Dict) -> None:
        connector = self.get_output_connector(dest)
        connector.write(df, dest)

    def _write_external_outputs_default(self, df: DataFrame) -> None:
        for _, dest in self.external_outputs.items():
            self.write_external_output(df, dest)

    def write_external_output(self, df: DataFrame, dest: Dict) -> None:
        """Writes a given DataFrame to a given external output

        :param df: The DataFrame to write
        :param dest: The alias of the external output to write to
        :return: nothing
        """
        if self.__write_external_output is None:
            return self._write_external_output_default(df, dest)
        else:
            return self.__write_external_output(df, dest)

    def write_external_outputs(self, df: DataFrame) -> None:
        """Writes a given DataFrame to all the declared external outputs

        :param df: The DataFrame to write
        :return: nothing
        """
        if self.__write_external_outputs is None:
            return self._write_external_outputs_default(df)
        else:
            return self.__write_external_outputs(df)

    def get_output_connector(self, dest: Union[str, Dict]):
        if type(dest) == str:
            dest = self.external_outputs[dest]
        from karadoc.common.connector import load_connector

        return load_connector(dest[CONNECTION_GROUP], self.spark)
