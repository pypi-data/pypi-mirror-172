from __future__ import annotations

import typing as t

from supervisor.manifest import Step, StepId
from supervisor.workflow.nodes import Node, NodeBuilder


class NaryTree:
    def __init__(self, root: Node = None, current_node: StepId = None):
        self.root = root
        self.current_node = current_node

    """
    Nary Tree Class provides graph structure and interface for traversal
    depending on Node type and Node predicates passed. Favors pre-order
    traversal in the current interface

    Args:
        root - Node: root node of the tree
        current_node - StepId: current node in the tree

    Attributes:
        children - list: list of NaryTree objects
        has_children - bool: True if tree has children
        last_node_uuid - StepId: last node in the tree

    """

    @property
    def children(self) -> t.List[NaryTree]:
        return self.root.children

    @property
    def has_children(self) -> bool:
        return True if self.children else False

    @property
    def last_node_uuid(self) -> StepId:
        """
        Returns the last Tree Node uuid in Tree - this should be the last "step"
        in Manifest
        """
        node_uuids = self.preorder_step_ids()
        assert node_uuids, "Must have a non empty Tree to get the last node uuid"
        return node_uuids[-1]

    def preorder_step_ids(self, ans: list = None) -> t.List[str]:
        """
        Returns a list of Step Ids from Tree Nodes Tree - uses pre-order
        traversal order
        """
        if not self.root:
            return ans
        if ans == None:
            ans = []
        ans.append(self.root.uuid)
        for child in self.root.children:
            child.preorder_step_ids(ans)
        return ans

    @classmethod
    def from_step(cls, step: Step, last_step: bool = False) -> NaryTree:
        """
        Recursively creates a NaryTree from a Step

        Args:
            step - Step: a Step object from manifest
            last_step - bool: if this is the last step in the tree

        Returns:
            NaryTree: A new instance of this class.
        """

        final_step: bool = False
        if last_step and not step.has_children:
            final_step = True
        next_node = NodeBuilder.create_node(step, final_step)
        items = []

        # Recursively build the nodes from the children of root
        for sub_step in step.steps:
            if len(items) - 1 == len(step.steps):
                final_step = True
            new_trie = cls.from_step(sub_step, final_step)
            items.append(new_trie)

        # add children == list
        next_node.children = items
        return cls(root=next_node)

    @classmethod
    def from_steps(cls, steps: t.List[Step]) -> NaryTree:
        """
        Recursively creates a NaryTree from a List of Steps

        Args:
            steps - List[Step]: a List of Step objects from manifest

        Returns:
            NaryTree: A new instance of this class.
        """

        final_tree = cls.from_step(steps.pop(0))
        root_children = []
        last_step: bool = False
        for step in steps:
            if len(steps) - 1 == len(root_children):
                last_step = True
            new_step_tree = cls.from_step(step, last_step)
            root_children.append(new_step_tree)

        final_tree.root.children.extend(root_children)
        return final_tree

    def __len__(self):
        """
        Returns the length of the tree -> total number of nodes in all subtrees
        """
        return len(self.preorder_step_ids())

    def search(self, node_uuid: StepId) -> t.Union[Node, None]:
        """
        Recursively searches for a Node in Tree from a StepId

        Args:
            node_uuid - StepId: a StepId str

        Returns:
            Node: found instance of this class or None
        """
        current = self.root
        if current.uuid == node_uuid:
            return current
        for n in current.children:
            node = n.search(node_uuid)
            if node:
                return node
        return None

    def preorder_step_ids(self, ans: t.List = None) -> t.List[int]:
        """
        Returns a list of StepIds in preorder traversal
        """
        if not self.root:
            return ans
        if ans == None:
            ans = []
        ans.append(self.root.uuid)
        for child in self.root.children:
            child.preorder_step_ids(ans)
        return ans

    def depth(self, node_uuid: StepId = None) -> int:
        """
        Returns depth of Tree from StepId, if no StepId is passed, returns depth of root
        """
        if not node_uuid:
            node_uuid = self.root.uuid
        node = self.search(node_uuid)
        if not node:
            raise Exception("No Node was found with this StepId")
        return self.max_depth(node)

    def max_depth(self, node: Node) -> int:
        """
        Return the Max Depth of TreeNode
        """
        if not node.children:
            return 0
        children_max_depth = []
        for child in node.children:
            children_max_depth.append(self.max_depth(child.root))
        return 1 + max(children_max_depth)

    def next_node(self, predicate: t.Optional[t.Any] = None) -> StepId:
        """
        Return the next node in the tree
        """
        return self.root.next(predicate)

    def __iter__(self) -> t.Union[NaryTree, StopIteration]:
        """
        Returns iterator for NaryTree
        """
        yield self
        for child in self.root.children:
            for node in child:
                yield node
