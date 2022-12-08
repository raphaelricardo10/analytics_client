import pandas as pd

from google.cloud import bigquery


class BigQueryResult:
    def __init__(self, rows) -> None:
        self._rows = rows
        self._current = 0

    def __iter__(self):
        return self._rows

    def __next__(self):
        self._current += 1
        if self._current < len(self._rows):
            return self._current
        raise StopIteration


class BigQueryClient:
    def __init__(self, project_id: str = None, dataset: str = None) -> None:
        self.client = bigquery.Client(project=project_id)
        self.project_id = project_id
        self.dataset = dataset

    def select(self, table: str, columns: "list[str]" = "*", limit=10000, start_date = None, to_df=True):
        query = f"""\
            SELECT {','.join(columns)}\
            FROM {self.dataset}.{table}\
            {f"WHERE ts > '{start_date}'" if start_date else ''}\
            ORDER BY ts DESC\
            {f"LIMIT {limit}" if limit else ''}\
        """

        if to_df:
            return pd.read_gbq(query, self.project_id).sort_values(by='ts', ascending=True)

        result = BigQueryResult(self.client.query(query, project=self.project_id).result())

        return result
