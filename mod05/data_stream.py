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


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []
        self._items_per_processor: dict[DataProcessor, int] = {}

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)
        self._items_per_processor[proc] = 0

    def process_stream(self, stream: list[typing.Any]) -> None:
        def count_items(data: typing.Any) -> int:
            if isinstance(data, list):
                return len(data)
            return 1

        for element in stream:
            handled = False
            for processor in self._processors:
                if processor.validate(element):
                    handled = True
                    processor.ingest(element)
                    self._items_per_processor[processor] += (
                        count_items(element)
                    )
                    break
            if not handled:
                print(
                    "DataStream error - "
                    f"Can't process element in stream: {element}"
                    )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return
        for processor in self._processors:
            label = processor.__class__.__name__.replace(
                'Processor',
                ' Processor'
                )
            items = self._items_per_processor[processor]
            remaining = len(processor._storage)
            print(
                f"{label}: total {items} items processed, "
                f"remaining {remaining} on processor"
                )


def consume_elements(proc: DataProcessor, nb: int) -> None:
    for _ in range(nb):
        try:
            proc.output()
        except IndexError:
            print(f" No more element to consume in {proc.__class__.__name__}")
            return


def main() -> None:
    print("=== Code Nexus - Data Stream ===")

    print("\nInitialize Data Stream...")
    np = NumericProcessor()
    tp = TextProcessor()
    lp = LogProcessor()
    ds = DataStream()
    ds.print_processors_stats()

    print("\nRegistering Numeric Processor")
    ds.register_processor(np)

    stream = [
        'Hello world',
        [3.14, -1, 2.71],
        [
            {
                'log_level': 'WARNING',
                'log_message': 'Telnet access! Use ssh instead'
            },
            {
                'log_level': 'INFO',
                'log_message': 'User wil is connected'
            }
        ],
        42,
        ['Hi', 'five']
        ]

    print(f"\nSend first batch of data on stream: {stream}")
    ds.process_stream(stream)
    ds.print_processors_stats()

    print("\nRegistering other data processors")
    ds.register_processor(tp)
    ds.register_processor(lp)
    print("Send the same batch again")
    ds.process_stream(stream)
    ds.print_processors_stats()

    print(
        "\nConsume some elements from the data processors: "
        "Numeric 3, Text 2, Log 1"
        )
    consume_elements(np, 3)
    consume_elements(tp, 2)
    consume_elements(lp, 10)
    ds.print_processors_stats()


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(f"Unexpected error: {err}")
