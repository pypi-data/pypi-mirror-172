from __future__ import annotations

import collections
import enum
from dataclasses import dataclass
from typing import Dict, List, Optional

from supervisor.manifest import Step, StepId


@dataclass
class Node:
    """
    An item in the `StateMachine`'s graph that points to other `Node`s based
    on the UUIDs.

    Attributes:
        self.uuid (StepId): The UUID for this node (and corresponding workflow
            step).
        self.default_next (Node, optional): The next sequential node.
        self.when_true(StepId, optional): If set, the next node to
            go to if the previous result was True.
        self.when_false(StepId, optional): If set, the next node to go to
            if the previous result was False.
    """

    uuid: StepId
    default_next: Optional[Node] = None
    when_true: Optional[StepId] = None
    when_false: Optional[StepId] = None

    @property
    def is_leaf(self) -> bool:
        """
        Says whether the node is a leaf in the graph/tree.

        Returns:
            bool: True if any of `self.default_next`, `self.when_true`, or
                `self.when_false`. False otherwise.
        """
        return not (self.default_next or self.when_true or self.when_false)


@dataclass
class LinkedList(collections.UserList):
    """
    A list of nodes, where each node links to the next. This class also supports
    built in methods of accessing lists, such as `len()` and `my_list[1]`.

    Attributes:
        self.data (List[Node]): The list of nodes.
    """

    data: List[Node]

    @classmethod
    def from_step(cls, step: Step) -> LinkedList:
        """
        Creates an instance of this class from one ``Step``, where each
        child ``Step`` is linked to the next child, and the parent links
        to the first child.

        Args:
            step (Step): The root (parent) step.

        Returns:
            LinkedList: A new list.
        """

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
        """
        Creates a LinkedList from a list of ``Step``s.

        Args:
            steps (List[Step]): The list of root (parent) steps.

        Returns:
            LinkedList: A new list.
        """

        final_list = cls(data=[])
        for step in steps:
            new_step_list = cls.from_step(step)

            # Link most current step in flat list to first of new items
            if final_list and new_step_list:
                final_list[-1].default_next = new_step_list[0]

            final_list.extend(new_step_list)

        return final_list


class MachineState(enum.Enum):
    """
    What state the ``StateMachine`` is in.`
    """

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
        """
        Runs through a graph of nodes based on the execution of the previous
        node, and what the return value of that execution was.

        Args:
            nodes (LinkedList): The nodes in the graph to examine.
            current_node (Node, optional): The current node that's executed.
                Defaults to None.
            state (MachineState): What state the machine is currently in.
                Defaults to `MachineState.NOT_STARTED`.

        Attributes:
            nodes (LinkedList): The nodes in the graph to move though.
            current_node (Node): The current node in the graph that's
                being executed.
            state (MachineState): The current state of this instance.
            nodes_by_id (Dict[StepId, Node): The same nodes as `self.nodes` but
                in a dictionary, where the keys are the uuid of each node,
                and the values are the nodes themselves. This can be used
                for quick lookups to retrieve the next node to run.
        """
        self.nodes = nodes
        self.current_node = current_node
        self.state = state
        self.nodes_by_id: Dict[StepId, Node] = {node.uuid: node for node in self.nodes}

    def next(self, predicate: Optional[bool] = None) -> Optional[Node]:
        """
        Determine the next node in the graph to execute, optionally based
        on the return value of the previous node execution.

        Args:
            predicate (bool, optional): The return value of the previous
                node execution, if available. Defaults to None.

        Returns:
            Node, optional: The next node in the graph, if available. If None,
                then there are no more nodes to run.
        """

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
        else:
            # This state is DONE
            return None

        # Update current node and state
        self.current_node = next_node
        if self.current_node.is_leaf:
            self.state = MachineState.DONE
        return self.current_node

    @classmethod
    def from_steps(cls, steps: List[Step]) -> StateMachine:
        """
        Creates an instance of this class from a list of steps.

        Args:
            steps (List[Step]): The root (parent) steps in a workflow.

        Returns:
            StateMachine: A new instance of this class.
        """

        # Flatten steps to point to each other as a list
        linked_list = LinkedList.from_steps(steps)
        return cls(nodes=linked_list, current_node=None)
