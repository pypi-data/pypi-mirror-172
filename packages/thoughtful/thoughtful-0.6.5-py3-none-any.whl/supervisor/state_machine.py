from __future__ import annotations

import enum
import typing as t
from dataclasses import dataclass

from supervisor.deprecated_markers import DeprecatedBecauseNonDynamic
from supervisor.manifest import Step, StepId
from supervisor.nodes import Node
from supervisor.tree import NaryTree


class MachineState(enum.Enum):
    """
    What state the ``StateMachine`` is in.`
    """

    NOT_STARTED = "not_started"
    RUNNING = "running"
    DONE = "done"


@dataclass
class StateMachine(DeprecatedBecauseNonDynamic):
    def __init__(
        self,
        nary_tree: NaryTree,
        current_node: t.Optional[Node] = None,
        state: MachineState = MachineState.NOT_STARTED,
    ) -> None:
        """
        Runs through a graph of nodes based on the execution of the previous
        node, and what the return value of that execution was.

        Args:
            nary_tree (N-Ary Tree): The nodes in the graph to examine.
            current_node (Node, optional): The current node that's executed.
                Defaults to None.
            state (MachineState): What state the machine is currently in.
                Defaults to `MachineState.NOT_STARTED`.

        Attributes:
            nary_tree (N-Ary Tree): The nodes in the graph to move though.
            current_node (Node): The current node in the graph that's
                being executed.
            state (MachineState): The current state of this instance.
            nodes_by_id (Dict[StepId, Node): The same nodes as `self.nodes` but
                in a dictionary, where the keys are the uuid of each node,
                and the values are the nodes themselves. This can be used
                for quick lookups to retrieve the next node to run.
        """
        self.nary_tree = nary_tree
        self.current_node = current_node
        self.state = state

    def next(self, predicate: t.Optional[bool] = None) -> t.Optional[Node]:
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
            next_node = (
                self.nary_tree.root
            )  # this will start pre-order traversal function
            self.state = MachineState.RUNNING
        elif self.state == MachineState.RUNNING:
            next_node_id: StepId = self.current_node.next(predicate)
            next_node = self.nary_tree.search(next_node_id)

        elif self.state == MachineState.DONE:
            # If we're already done, return no next step
            return None
        else:
            raise ValueError(f"Unknown machine state: {self.state}")
            # This state should be DONE

        self.current_node = next_node
        if self.current_node.is_leaf:
            self.state = MachineState.DONE
        return self.current_node

    @classmethod
    def from_steps(cls, steps: t.List[Step]) -> StateMachine:
        """
        Creates an instance of this class from a list of steps.

        Args:
            steps (List[Step]): The root (parent) steps in a workflow.

        Returns:
            StateMachine: A new instance of this class.
        """

        # Flatten steps to point to each other as a list
        tree = NaryTree.from_steps(steps)
        return cls(nary_tree=tree)
