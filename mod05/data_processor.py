#!/usr/bin/env python3

import typing
import abc


class DataProcessor(abc.ABC):
    def __init__(self) -> None:
        self._storage: list[str] = []
        self._rank: int = 0

    @abc.abstractmethod
    def validate(self, data: typing.Any) -> bool:
        pass

    @abc.abstractmethod
    def ingest(self, data: typing.Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._storage:
            raise IndexError("No data in storage")
        rank = self._rank
        value = self._storage.pop(0)
        self._rank += 1
        return rank, value


class NumericProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
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
    def validate(self, data: typing.Any) -> bool:
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
    def validate(self, data: typing.Any) -> bool:
        def valid_dict(dic: typing.Any) -> bool:
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


def test_validate(proc: DataProcessor, data: typing.Any) -> None:
    print(f" Trying to validate input '{data}': {proc.validate(data)}")


def test_ingest(proc: DataProcessor, data: typing.Any) -> None:
    type_name = str(type(data).__name__)
    if type_name == 'str':
        type_name = 'string'
    if type_name == 'int':
        type_name = 'integer'
    if type_name == 'dict':
        type_name = 'dictionary'
    print(
        f" Test invalid ingestion of {type_name} "
        f"'{data}' without prior validation:"
        )
    try:
        proc.ingest(data)
    except Exception as e:
        print(f" Got exception: {e}")


def data_type(data: typing.Any) -> str:
    def get_type(data: typing.Any) -> str:
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
        data: typing.Any,
        proc: DataProcessor,
        nb_extract: int
        ) -> None:
    if not proc.validate(data):
        test_ingest(proc, data)
        return
    print(f" Processing data: {data}")
    proc.ingest(data)
    label = "value" if nb_extract == 1 else "values"
    print(f" Extracting {nb_extract} {label}...")
    for _ in range(nb_extract):
        rank, value = proc.output()
        print(f" {data_type(data)} {rank}: {value}")


def test_proc(
        proc: DataProcessor,
        valid: typing.Any,
        invalid: typing.Any,
        improper: typing.Any,
        data: typing.Any,
        extracting: int
        ) -> None:
    print(
        "\nTesting "
        f"{proc.__class__.__name__.replace('Processor', ' Processor')}..."
        )
    test_validate(proc, valid)
    test_validate(proc, invalid)
    test_ingest(proc, improper)
    process_data(data, proc, extracting)


def main() -> None:
    print("=== Code Nexus - Data Processor ===")
    np = NumericProcessor()
    tp = TextProcessor()
    lp = LogProcessor()
    test_proc(np, 42, 'Hello', 'foo', [1, 2, 3, 4, 5], 3)
    test_proc(tp, 'Hello', -42, 42, ['Hello', 'Nexus', 'World'], 1)
    test_proc(
        lp,
        {'log_level': 'NOTICE', 'log_message': 'Connection to server'},
        {'hello': 'world', 'nexus': 'here'},
        ['log_level', 'NOTICE', 'log_message', 'Connection to server'],
        [
            {'log_level': 'NOTICE', 'log_message': 'Connection to server'},
            {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}
        ],
        2
        )


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(f" Unexpected error: {err}")
