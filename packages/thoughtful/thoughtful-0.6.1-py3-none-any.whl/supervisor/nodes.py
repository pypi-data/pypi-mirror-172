from __future__ import annotations

import collections
import typing as t
from abc import ABC, abstractmethod
from dataclasses import dataclass

from supervisor.manifest import Step, StepId


class Node(ABC):
    def __init__(
        self,
        uuid: str,
        children=None,
        next_uuid: t.Optional[StepId] = None,
        parent_uuid: t.Optional[StepId] = None,
    ) -> None:
        self.uuid = uuid
        self.children = children or []
        self.next_uuid = next_uuid
        self.parent_uuid = parent_uuid

    """
    Abstract base class for a Node object, exposes a common interface for all
    Node type objects, forces all subclasses to implement the `next` and
    'is_leaf' methods.

    Args:
        uuid (str): The unique identifier for this node.
        children (list, optional): A list of child nodes. Defaults to None.
        next_uuid (StepId, optional): The uuid of the next node to execute.
        parent_uuid (StepId, optional): The uuid of the parent node.

    Attributes:
        uuid (str): The unique identifier for this node.
        children (list): A list of child nodes built in sequence preserved from Manifest
        next_uuid (StepId): The uuid of the next node to execute in the graph.
        parent_uuid (StepId): The uuid of the parent node in the graph.

    """

    @property
    @abstractmethod
    def is_leaf(self) -> bool:
        """
        Abstract Method - Determine if node is a leaf node this depends on it's StepType
        """
        raise NotImplementedError("Not implemented in ABC")

    @abstractmethod
    def next(self, predicate: t.Optional[t.Any] = None) -> StepId:
        """
        Abstract method - Determine the next node to execute based on the return
        value of the previous node execution and an optional predicate
        """
        raise NotImplementedError("Not implemented in ABC")


@dataclass
class BranchNode(Node):
    def __init__(self, uuid: str, branches: t.Dict[t.Any, StepId]) -> None:
        super().__init__(uuid=uuid)
        self.branches = {str(k): v for (k, v) in branches.items()}

    """
    A node type that has branches, meaning it can jump to the designated StepIds
    as specified by the Manifest Step Type this Node is constructed with.
    """

    @property
    def is_leaf(self) -> bool:
        """
        Determine if node is a leaf - no branches or next_uuid
        """
        return not (self.branches and self.next_uuid)

    def get_keys_from_value(self, val):
        """
        Return key given a value from self.branches
        """
        return [k for k, v in self.branches.items() if v == val][0]

    def next(self, predicate: t.Optional[t.Any] = None) -> StepId:
        """
        Determine the next node to execute based on optional predicate. If
        predicate is a bool, returns corresponding StepId, otherwise returns next_uuid
        """
        if not predicate:
            return self.next_uuid
        assert (
            predicate in self.branches.values()
        ), "Result must be a key in the branches property"
        return self.get_keys_from_value(predicate)


@dataclass
class ConditionalNode(Node):
    def __init__(self, uuid: str, when_true: StepId, when_false: StepId) -> None:
        super().__init__(uuid=uuid)
        self.when_true = when_true
        self.when_false = when_false
        self.branches = {True: when_true, False: when_false}

    """
    A Conditional Node type can jump to 2 different Nodes depending on Manifest.
    If a boolean is returned from this function, it will jump to the designated Node
    """

    @property
    def is_leaf(self) -> bool:
        """
        Determine if node is a leaf - no branches or when_true, when_false attrs
        """
        return not (self.when_true or self.when_false or self.next_uuid)

    def next(self, predicate: t.Optional[t.Any] = None) -> StepId:
        """
        Determine the next node to execute based on optional predicate and
        corresponding StepId from `branches` attribute. Default returns the next_uuid
        """
        if predicate not in self.branches.keys():
            return self.next_uuid

        return str(self.branches[predicate])


@dataclass
class SequentialNode(Node):
    def __init__(self, uuid: str, next_uuid: t.Optional[StepId] = None) -> None:
        super().__init__(uuid=uuid)
        self.next_uuid = next_uuid

    """
    A Sequential Node type that will always go to next node designed by the Manifest.
    """

    @property
    def is_leaf(self) -> bool:
        """
        Determine if node is a leaf - no next_uuid
        """
        return not (self.next_uuid)

    def next(self, predicate: t.Optional[t.Any] = None) -> StepId:
        """
        Determine the next node to execute - returns next_uuid
        """
        return self.next_uuid


class NodeBuilder:
    """
    NodeBuilder - class helps creates Nodes of different types from a [step]
    object
    """

    node_cache = collections.deque()

    @classmethod
    def create_node(cls, step: Step, final_step: bool = False) -> Node:
        """
        Builder method to create a Node from a Step
        """
        new_node = cls.switch_create_node(step)
        if not cls.node_cache:
            pass

        else:
            prev_node = cls.node_cache.popleft()
            new_node.parent_uuid = prev_node.uuid
            prev_node.next_uuid = new_node.uuid
        if final_step:
            # need to drop last item in cache to maintain ability to run multiple dw
            pass
        else:
            cls.node_cache.appendleft(new_node)
        return new_node

    @classmethod
    def switch_create_node(cls, step: Step) -> Node:
        """
        Switch Case helper method to construct actual Node type
        """
        if step.step_type == "sequential":
            return SequentialNode(uuid=step.step_id)

        elif step.step_type == "conditional":
            return ConditionalNode(
                uuid=step.step_id, when_true=step.when_true, when_false=step.when_false
            )

        elif step.step_type == "branch":
            return BranchNode(uuid=step.step_id, branches=step.branches)
        else:
            raise NotImplemented("Unknown StepType detected")

    @classmethod
    def create_nodes(cls, steps: t.List[Step]) -> t.List[Node]:
        """
        Builder method to create a list of Nodes from a list of Steps
        """
        results = []
        final_step: bool = False
        for step in steps:
            # remove last item in list if final step in list (needed to preserve class methods for this class)
            if len(steps) - 1 == len(results):
                final_step = True
            results.append(cls.create_node(step, final_step))
