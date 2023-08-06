#!/usr/bin/env python3

import datetime
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Iterator, Iterable, List, Optional


@dataclass
class LabelledEvent:
    start: datetime.datetime
    end: Optional[datetime.datetime]
    label: Optional[str]


class Timeline(object):
    def __init__(
            self,
            events: Optional[Iterable[LabelledEvent]],
    ):
        self.events = set()
        self.event_labels = set()
        for event in events:
            self.add_event(event)

    def add_event(self, event: LabelledEvent):
        label = event.label
        if label in self.event_labels:
            raise ValueError(f'Duplicate event detected: {label}')
        self.event_labels.add(label)
        self.events.add(event)

    def events_at_time(point: datetime.datetime) -> List[LabelledEvent]:
        pass

    def __len__(self) -> int:
        return len(self.events)

    def __format__(self) -> str:
        pass

    def __iter__(self) -> LabelledEvent:

        def _next_or_none(i: Iterator) -> Optional[Any]:
            try:
                return i.next()
            except StopIteration:
                return None

        starts = iter(self.starts)
        ends = iter(self.ends)
        while True:
            start = _next_or_none(starts)
            end = _next_or_none(ends)

            if start is None and end is not None:
                yield end
                end = _next_or_none(end)
            elif end is None and start is not None:
                yield start
                start = _next_or_none(start)
            elif start and end:
                if start <= end:
                    yield start
                    start = _next_or_none(start)
                else:
                    yield end
                    end = _next_or_none(end)
            else:
                assert not start and not end
                raise StopIteration

    def __repr__() -> str:
        pass
