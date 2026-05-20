#!/usr/bin/env python3

from typing import Any
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._storage: list[str] = []
        self._rank: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._storage:
            raise IndexError("No data in storage")
        rank = self._rank
        value = self._storage.pop(0)
        self._rank += 1
        return rank, value


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(isinstance(d, (int, float)) for d in data)
        return isinstance(data, (int, float))

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise Exception("Improper numeric data")
        if isinstance(data, list):
            for d in data:
                self._storage.append(str(d))
        else:
            self._storage.append(str(data))


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(isinstance(d, str) for d in data)
        return isinstance(data, str)

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise Exception("Improper text data")
        if isinstance(data, list):
            for d in data:
                self._storage.append(d)
        else:
            self._storage.append(data)


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        def valid_dict(dic: Any) -> bool:
            if not isinstance(dic, dict):
                return False
            if set(dic.keys()) != {'log_level', 'log_message'}:
                return False
            return all(isinstance(v, str) for v in dic.values())

        if isinstance(data, list):
            return all(valid_dict(d) for d in data)
        return valid_dict(data)

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise Exception("Improper log data")
        if isinstance(data, list):
            for d in data:
                self._storage.append(f"{d['log_level']}: {d['log_message']}")
        else:
            self._storage.append(f"{data['log_level']}: {data['log_message']}")


def test_validate(proc: DataProcessor, data: Any) -> None:
    print(f" Trying to validate input '{data}': {proc.validate(data)}")


def data_type(data: Any) -> str:
    def get_type(data: Any) -> str:
        if isinstance(data, (int, float)):
            return "Numeric value"
        elif isinstance(data, str):
            return "Text value"
        elif isinstance(data, dict):
            return "Log entry"
        else:
            raise Exception
    if isinstance(data, list):
        for d in data:
            return get_type(d)
    return get_type(data)


def process_data(
        data: Any,
        proc: DataProcessor,
        nb_extract: int
        ) -> None:
    if not proc.validate(data):
        try:
            proc.ingest(data)
        except Exception as e:
            print(f' Got exception: {e}')
            return
    print(f" Processing data: {data}")
    proc.ingest(data)
    label = "value" if nb_extract == 1 else "values"
    print(f" Extracting {nb_extract} {label}...")
    for _ in range(nb_extract):
        rank, value = proc.output()
        print(f" {data_type(data)} {rank}: {value}")


def main() -> None:
    print("=== Code Nexus - Data Processor ===")
    print("\nTesting Numeric Processor...")
    np = NumericProcessor()
    test_validate(np, 42)
    test_validate(np, 'Hello')
    print(" Test invalid ingestion of string 'foo' without prior validation:")
    try:
        np.ingest('foo')  # type: ignore
    except Exception as e:
        print(f' Got exception: {e}')
    process_data([1, 2, 3, 4, 5], np, 3)

    print("\nTesting Text Processor...")
    tp = TextProcessor()
    test_validate(tp, 'Hello')
    test_validate(tp, 42)
    print(" Test invalid ingestion of integer '-42' without prior validation:")
    try:
        tp.ingest(-42)  # type: ignore
    except Exception as e:
        print(f" Got exception: {e}")
    process_data(['Hello', 'Nexus', 'World'], tp, 1)

    print("\nTesting Log Processor...")
    lp = LogProcessor()
    test_validate(
        lp,
        {'log_level': 'NOTICE', 'log_message': 'Connection to server'}
        )
    test_validate(lp, {'hello': 'world', 'nexus': 'here'})
    print(
        " Test invalid ingestion of list of strings '['log_level', "
        "'log_message']' without prior validation:"
        )
    try:
        lp.ingest(['log_level', 'log_message'])  # type: ignore
    except Exception as e:
        print(f' Got exception: {e}')
    process_data([
            {'log_level': 'NOTICE', 'log_message': 'Connection to server'},
            {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}
            ], lp, 2)


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(f" Unexpected error: {err}")
