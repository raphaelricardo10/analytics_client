import pandas as pd

from google.cloud import bigquery


class BigQueryResult:
    def __init__(self, rows) -> None:
        self._rows = rows
        self._current = 0

    def __iter__(self):
        return self._rows

    def __next__(self):
        self.current += 1
        if self.current < len(self._rows):
            return self.current
        raise StopIteration


class BigQueryClient:
    def __init__(self, project_id: str = None, dataset: str = None) -> None:
        self.client = bigquery.Client(project=project_id)
        self.project_id = project_id
        self.dataset = dataset

    def select(self, table: str, columns: "list[str]" = "*", limit=1000, to_df=True):
        query = f"""\
            SELECT {','.join(columns)}\
            FROM {self.dataset}.{table}\
            {f"LIMIT {limit}" if limit else ''}\
        """

        if to_df:
            return pd.read_gbq(query)

        result = BigQueryResult(self.client.query(query).result())

        return result
