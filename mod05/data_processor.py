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


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===")

    print("\nTesting Numeric Processor...")
    print(
        " Trying to validate input '42': "
        f"{NumericProcessor().validate(42)}"
        )
    print(
        " Trying to validate input 'Hello': "
        f"{NumericProcessor().validate('Hello')}"
        )
    print(" Test invalid ingestion of string 'foo' without prior validation:")
    try:
        NumericProcessor().ingest('foo')  # type: ignore
    except Exception as err:
        print(f" Got exception: {err}")
    numeric_data: list[int | float] = [1, 2, 3, 4, 5]
    print(f" Processing data: {numeric_data}")
    print(" Extracting 3 values...")
    np = NumericProcessor()
    np.ingest(numeric_data)
    for i in range(3):
        rank, value = np.output()
        print(f" Numeric value {rank}: {value}")

    print("\nTesting Text Processor...")
    print(
        " Trying to validate input 'Hello': "
        f"{TextProcessor().validate('Hello')}"
    )
    print(
        " Trying to validate input '42': "
        f"{TextProcessor().validate(42)}"
    )
    print(" Test invalid ingestion of integer '45' without prior validation:")
    try:
        TextProcessor().ingest(45)  # type: ignore
    except Exception as err:
        print(f" Got exception: {err}")
    text_data = ['Hello', 'Nexus', 'World']
    print(f" Processing data: {text_data}")
    print(" Extracting 1 value...")
    tp = TextProcessor()
    tp.ingest(text_data)
    rank, value = tp.output()
    print(f" Text value {rank}: {value}")

    print("\nTesting Log Processor...")
    log_data = [{
        'log_level': 'WARNING',
        'log_message': 'Telnet access! Use ssh instead'
        }]
    print(
        f" Trying to validate input '{log_data}': "
        f"{LogProcessor().validate(log_data)}"
    )
    print(
        f" Trying to validate input 'Hello': "
        f"{LogProcessor().validate('Hello')}"
    )
    print(" Test invalid ingestion of integer '42' without prior validation:")
    try:
        LogProcessor().ingest(42)  # type: ignore
    except Exception as err:
        print(f" Got exception: {err}")
    log_data = [
        {'log_level': 'NOTICE', 'log_message': 'Connection to server'},
        {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}
        ]
    print(f" Processing data: {log_data}")
    print(" Extracting 2 values...")
    lp = LogProcessor()
    lp.ingest(log_data)
    for i in range(2):
        rank, value = lp.output()
        print(f" Log entry {rank}: {value}")
