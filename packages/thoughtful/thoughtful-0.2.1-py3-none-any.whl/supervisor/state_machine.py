from __future__ import annotations

import collections
import enum
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional

from supervisor.manifest import Step, StepId


@dataclass
class Node:
    uuid: StepId
    default_next: Optional[Node] = None
    when_true: Optional[StepId] = None
    when_false: Optional[StepId] = None

    @property
    def is_leaf(self) -> bool:
        return not (self.default_next or self.when_true or self.when_false)


@dataclass
class LinkedList(collections.UserList):
    data: List[Node]

    @classmethod
    def from_step(cls, step: Step) -> LinkedList:
        first_node = Node(
            uuid=step.step_id,
            default_next=None,
            when_true=step.when_true,
            when_false=step.when_false,
        )
        items = [first_node]

        # Recursively build the flat list of nodes from the children

        for sub_step in step.steps:
            new_list = LinkedList.from_step(sub_step)
            # Link the last node in the current list to the first of the new
            # list
            items[-1].default_next = new_list[0]
            # Merge the lists together
            items.extend(new_list)

        return cls(data=items)

    @classmethod
    def from_steps(cls, steps: List[Step]) -> LinkedList:
        final_list = cls(data=[])
        for step in steps:
            new_step_list = cls.from_step(step)

            # Link most current step in flat list to first of new items
            if final_list and new_step_list:
                final_list[-1].default_next = new_step_list[0]

            final_list.extend(new_step_list)

        return final_list


class MachineState(enum.Enum):
    NOT_STARTED = "not_started"
    RUNNING = "running"
    DONE = "done"


@dataclass
class StateMachine:
    def __init__(
        self,
        nodes: LinkedList,
        current_node: Optional[Node] = None,
        state: MachineState = MachineState.NOT_STARTED,
    ) -> None:
        self.nodes = nodes
        self.current_node = current_node
        self.state = state
        self.nodes_by_id: Dict[StepId, Node] = {node.uuid: node for node in self.nodes}

    def next(self, predicate: Optional[bool] = None) -> Optional[Node]:
        if self.state == MachineState.NOT_STARTED:
            # Start up: begin with first node
            next_node = self.nodes[0]
            self.state = MachineState.RUNNING
        elif self.state == MachineState.RUNNING:
            # Find the next node
            # Check for a conditional step
            if predicate is not None:
                # Fork based on the predicate value
                next_id = (
                    self.current_node.when_true
                    if predicate
                    else self.current_node.when_false
                )
                next_node = self.nodes_by_id[next_id]
            else:
                # Otherwise, move on in order
                next_node = (
                    self.current_node.default_next
                    if self.current_node.default_next
                    else None
                )
        elif self.state == MachineState.DONE:
            # If we're already done, return no next step
            return None
        else:
            raise ValueError(f"Unknown machine state: {self.state}")

        # Update current node and state
        self.current_node = next_node
        if self.current_node.is_leaf:
            self.state = MachineState.DONE
        return self.current_node

    @classmethod
    def from_steps(cls, steps: List[Step]) -> StateMachine:
        """Convenience constructor"""
        # Flatten steps to point to each other as a list
        linked_list = LinkedList.from_steps(steps)
        return cls(nodes=linked_list, current_node=None)
