from __future__ import annotations

import abc
import collections
import enum
from functools import reduce
from math import gcd
import queue
from typing import Dict, List, Optional, Set, Callable

from utils import getInput, timeit


class Pulse(enum.Enum):
    LOW = enum.auto()
    HIGH = enum.auto()


class PowerState(enum.Enum):
    ON = enum.auto()
    OFF = enum.auto()


class Event(list):
    def __call__(self, *args, **kwargs):
        for fn in self:
            fn(*args, **kwargs)


class Module(metaclass=abc.ABCMeta):
    def __init__(self, label, input_modules: Callable[[str], Set[Module]], destination_modules: Callable[[str], Set[Module]]):
        self.label = label
        self.input_modules = input_modules
        self.destination_modules = destination_modules
        self.pulse_event = Event()
        self.received_pulse: Pulse = Pulse.LOW
        self.sent_pulse: Pulse = Pulse.LOW

    @property
    @abc.abstractmethod
    def pulse(self) -> Optional[Pulse]: pass

    @abc.abstractmethod
    def update_state(self, source: str, pulse: Pulse) -> None: pass

    def receive(self, source: str, pulse: Pulse):
        self.received_pulse = pulse
        self.update_state(source, pulse)
        p = self.pulse
        if p is not None:
            self.sent_pulse = p
            self.pulse_event(self.label, p)


class Button(Module):
    @property
    def pulse(self) -> Optional[Pulse]:
        return Pulse.LOW

    def update_state(self, source: str, pulse: Pulse) -> None: pass


class Void(Module):
    @property
    def pulse(self) -> Optional[Pulse]:
        return None

    def update_state(self, source: str, pulse: Pulse) -> None: pass


class Broadcaster(Module):

    @property
    def pulse(self) -> Optional[Pulse]:
        return self.received_pulse

    def update_state(self, source: str, pulse: Pulse) -> None: pass


class FlipFlop(Module):

    def __init__(self, *args, **kwargs):
        super(FlipFlop, self).__init__(*args, **kwargs)
        self.power_state = PowerState.OFF

    @property
    def pulse(self) -> Optional[Pulse]:
        if self.received_pulse != Pulse.HIGH:
            if self.power_state == PowerState.OFF:
                self.power_state = PowerState.ON
                return Pulse.HIGH
            else:
                self.power_state = PowerState.OFF
                return Pulse.LOW

    def update_state(self, source: str, pulse: Pulse) -> None: pass


class Conjunction(Module):

    def __init__(self, *args, **kwargs):
        super(Conjunction, self).__init__(*args, **kwargs)

    @property
    def pulse(self) -> Optional[Pulse]:
        if all(m.sent_pulse == Pulse.HIGH for m in self.input_modules(self.label)):
            return Pulse.LOW
        return Pulse.HIGH

    def update_state(self, source: str, pulse: Pulse) -> None: pass


class CommunicationRelay:
    def __init__(self):
        self.modules: Dict[str, Module] = {}
        self._input_modules: Dict[str, Set[str]] = collections.defaultdict(set)
        self._destination_modules: Dict[str, List[str]] = collections.defaultdict(list)

        self._queue = queue.Queue()
        self._pulse_counter = collections.Counter()

    def register_module(self, source: str, targets: List[str]):
        if source == "broadcaster":
            module, label = Broadcaster, source
        elif source == "button":
            module, label = Button, source
        elif source.startswith("%"):
            module, label = FlipFlop, source[1:]
        elif source.startswith("&"):
            module, label = Conjunction, source[1:]
        else:
            module, label = Void, source

        m = module(label=label, input_modules=self.input_modules, destination_modules=self.destination_modules)
        m.pulse_event.append(self.receive)
        self.modules[label] = m
        self._destination_modules[label] = targets
        for t in targets:
            self._input_modules[t].add(label)

    def input_modules(self, label: str):
        return [self.modules[i] for i in self._input_modules[label]]

    def destination_modules(self, label: str):
        dms = self._destination_modules[label]
        return [self.modules[d] for d in dms]

    @property
    def score(self):
        return self._pulse_counter[Pulse.LOW] * self._pulse_counter[Pulse.HIGH]

    def receive(self, label: str, pulse: Pulse):
        """Receives a pulse between two modules"""
        try:
            m = self.modules[label]
        except KeyError:
            raise KeyError(f"{label} not available! Exiting.")
        else:
            for dest in self.destination_modules(m.label):
                # print(f"{m.label} -> {pulse} -> {dest.label}")
                self._pulse_counter[pulse] += 1
                self._queue.put((m.label, pulse, dest.label,))

    def process_next(self):
        source, pulse, dest = self._queue.get()
        if dest in self.modules:
            self.modules[dest].receive(source, pulse)

    def button(self):
        # print()
        self._queue.put(("press", Pulse.LOW, "button"))
        while not self._queue.empty():
            self.process_next()


def lcm(*numbers):
    return reduce(
        lambda acc, v: acc * v // gcd(acc, v),
        numbers,
        1
    )


@timeit
def main(aoc: str):
    communication_relay = CommunicationRelay()
    communication_relay.register_module("button", targets=["broadcaster"])
    communication_relay.register_module("output", targets=[])

    for line in aoc.splitlines():
        source_raw, destination_modules = line.split(" -> ")
        communication_relay.register_module(source_raw, destination_modules.split(", "))

    for label in set(communication_relay._input_modules.keys()) - set(communication_relay.modules.keys()):
        communication_relay.register_module(label, targets=[])

    i = 1
    watcher_map = collections.defaultdict(list)

    def watcher(l: str, p: Pulse):
        if p == Pulse.HIGH:
            watcher_map[l].append(i)
            print(f"{i} -> {l}")

    # watch these to try and find a LCM from the logs
    for l in ("nx", "sp", "cc", "jq",):
        communication_relay.modules[l].pulse_event.append(watcher)

    while len(watcher_map.keys()) < 4:
        communication_relay.button()
        i += 1

    print(watcher_map)
    print(lcm(*[v[0] for v in watcher_map.values()]))


if __name__ == "__main__":
    # main(getInput("./input-test.txt"))
    # main(getInput("./input-test-2.txt"))
    main(getInput("./input.txt"))
