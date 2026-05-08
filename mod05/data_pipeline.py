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
        rank = self._rank
        value = self._storage.pop(0)
        self._rank += 1
        return rank, value


class NumericProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, list):
            return all(isinstance(d, int | float) for d in data)
        return isinstance(data, int | float)

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
            for v in dic.values():
                if not isinstance(v, str):
                    return False
            return True
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


class ExportPlugin(typing.Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        pass


class CSVExportPlugin(ExportPlugin):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("CSV Output:")
        print(f"{','.join(d[1] for d in data)}")


class JSONExportPlugin(ExportPlugin):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("JSON Output:")
        items = []
        for rank, value in data:
            items.append(f'"item_{rank}": "{value}"')
        print("{" + ", ".join(items) + "}")


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
        print("== DataStream statisctics ==")
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

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        print(
            f"Send {nb} processed data from each processor to a "
            f"{plugin.__class__.__name__.replace('ExportPlugin', ' plugin')}:"
            )
        for processor in self._processors:
            extracted = []
            for _ in range(nb):
                if not processor._storage:
                    break
                extracted.append(processor.output())
            plugin.process_output(extracted)


def consume_elements(proc: DataProcessor, nb: int) -> None:
    for _ in range(nb):
        proc.output()


def main() -> None:
    print("=== Code Nexus - Data Pipeline ===")

    print("\nInitialize Data Stream...\n")
    np = NumericProcessor()
    tp = TextProcessor()
    lp = LogProcessor()
    ds = DataStream()
    ds.print_processors_stats()

    print("\nRegistering Processors")
    ds.register_processor(np)
    ds.register_processor(tp)
    ds.register_processor(lp)

    stream_1 = [
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

    print(f"\nSend first batch of data on stream: {stream_1}\n")
    ds.process_stream(stream_1)
    ds.print_processors_stats()
    print()

    csv = CSVExportPlugin()
    ds.output_pipeline(3, csv)
    print()

    ds.print_processors_stats()

    stream_2 = [
        21,
        [
            'I love AI',
            'LLMs are wonderful',
            'Stay healthy'
        ],
        [
            {
                'log_level': 'ERROR',
                'log_message': '500 server crash'
            },
            {
                'log_level': 'NOTICE',
                'log_message': 'Certificate expires in 10 days'
            }
        ],
        [32, 42, 64, 84, 128, 168],
        'World hello'
    ]
    print(f"\nSend another batch of data: {stream_2}\n")
    ds.process_stream(stream_2)

    ds.print_processors_stats()
    print()

    jsone = JSONExportPlugin()
    ds.output_pipeline(5, jsone)
    print()

    ds.print_processors_stats()


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(f"Unexpected error: {err}")
