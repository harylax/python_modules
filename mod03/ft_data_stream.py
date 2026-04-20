import random
import typing


def gen_event() -> typing.Generator[tuple[str, str], None, None]:
    while True:
        name = random.choice(['alice', 'bob', 'charlie', 'dylan'])
        action = random.choice([
            'run', 'eat', 'sleep',
            'grab', 'move', 'climb',
            'swim', 'release', 'use'
        ])
        yield (name, action)


def consume_event(events: list[tuple[str, str]]) -> typing.Generator[
    tuple[str, str],
    None,
    None
]:
    while events:
        event = random.choice(events)
        events.remove(event)
        yield event


def game_data_stream_processor() -> None:
    print("=== Game Data Stream Processor ===")
    gen = gen_event()
    for i in range(100):
        event = next(gen)
        print(f"Event {i}: Player {event[0]} did action {event[1]}")
    events = []
    for i in range(10):
        event = next(gen)
        events.append(event)
    print(f"Build list of 10 events: {events}")
    for event in consume_event(events):
        print(f"Got event from list: {event}")
        print(f"Remains in list: {events}")


if __name__ == "__main__":
    try:
        game_data_stream_processor()
    except Exception as err:
        print(f"Error: {err}")
