from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._storage: list[str] = []
        self._rank_counter: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._storage:
            raise IndexError("No stored data")
        rank = self._rank_counter
        oldest_data = self._storage.pop(0)
        self._rank_counter += 1
        return rank, oldest_data

    @abstractmethod
    def name(self) -> str:
        pass


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            for d in data:
                if not isinstance(d, int | float):
                    return False
        else:
            if not isinstance(data, int | float):
                return False
        return True

    def ingest(self, data: list[int | float] | int | float) -> None:
        if not self.validate(data):
            raise Exception("Improper numeric data")
        if isinstance(data, list):
            for d in data:
                self._storage.append(str(d))
        else:
            self._storage.append(str(data))

    def name(self) -> str:
        return "Numeric Processor"


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            for d in data:
                if not isinstance(d, str):
                    return False
        else:
            if not isinstance(data, str):
                return False
        return True

    def ingest(self, data: list[str] | str) -> None:
        if not self.validate(data):
            raise Exception("Improper text data")
        if isinstance(data, list):
            for d in data:
                self._storage.append(d)
        else:
            self._storage.append(data)

    def name(self) -> str:
        return "Text Processor"


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            for d in data:
                if not isinstance(d, dict):
                    return False
                if set(d.keys()) != {'log_level', 'log_message'}:
                    return False
                for value in d.values():
                    if not isinstance(value, str):
                        return False
        else:
            if not isinstance(data, dict):
                return False
            if set(data.keys()) != {'log_level', 'log_message'}:
                return False
            for value in data.values():
                if not isinstance(value, str):
                    return False
        return True

    def ingest(self, data: list[dict[str, str]] | dict[str, str]) -> None:
        if not self.validate(data):
            raise Exception("Improper log data")
        if isinstance(data, list):
            for d in data:
                s = f"{d['log_level']}: {d['log_message']}"
                self._storage.append(s)
        else:
            s = f"{data['log_level']}: {data['log_message']}"
            self._storage.append(s)

    def name(self) -> str:
        return "Log Processor"


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []
        self._items: dict[DataProcessor, int] = {}

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)
        self._items[proc] = 0

    def process_stream(self, stream: list[Any]) -> None:
        def count_items_processed(item: Any) -> int:
            if isinstance(item, list):
                return len(item)
            else:
                return 1

        for element in stream:
            handled = False
            for proc in self._processors:
                if proc.validate(element):
                    self._items[proc] += count_items_processed(element)
                    proc.ingest(element)
                    handled = True
                    break
            if not handled:
                print(
                    "DataStream error - Can't process element in stream: "
                    f"{element}"
                    )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return
        for proc in self._processors:
            # name = proc.__class__.__name__.replace('Processor', ' Processor')
            print(
                f"{proc.name()}: total "
                f"{self._items[proc]} items processed, "
                f"remaining {len(proc._storage)} on processor"
                )


def main() -> None:
    print("=== Code Nexus - Data Stream ===")

    print("\nInitialize Data Stream...")
    ds = DataStream()
    ds.print_processors_stats()

    print("\nRegistering Numeric Processor")
    np = NumericProcessor()
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
    proc = [TextProcessor(), LogProcessor()]
    print("Send the same batch again")
    for p in proc:
        ds.register_processor(p)
    ds.process_stream(stream)
    ds.print_processors_stats()

    print(
        "\nConsume some elements from the data processors: "
        "Numeric 3, Text 2, Log 1"
        )
    for i in range(3):
        np.output()
    for i in range(2):
        proc[0].output()
    proc[1].output()
    ds.print_processors_stats()


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(f"Unexpected error: {err}")
