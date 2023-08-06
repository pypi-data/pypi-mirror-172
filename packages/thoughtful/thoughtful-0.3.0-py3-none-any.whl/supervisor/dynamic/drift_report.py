from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from supervisor.manifest import Manifest, StepType
from supervisor.nodes import Node
from supervisor.reporter import Report
from supervisor.state_machine import StateMachine
from supervisor.tree import NaryTree


@dataclass
class DriftReport:
    """
    A report on how the execution of a digital worker differed from its
    manifest.

    Attributes:
        step_ids_missing_from_manifest (List[str]): List of step IDs that are
            executed by the digital worker but do not exist in its manifest.
        invalid_jumps (List[str]): List of step IDs that are executed by
            the digital worker immediately following a conditional step, but
            the jump to that step is not in the manifest.
        invalid_returns (List[str]): List of conditional step IDs that return
            invalid object types for a conditional step.
    """

    step_ids_missing_from_manifest: List[str]
    invalid_jumps: List[str]
    invalid_returns: List[str]

    def __json__(self) -> Dict[str, Any]:
        return {
            "unknown_step_ids": self.step_ids_missing_from_manifest,
            "invalid_jumps": self.invalid_jumps,
            "invalid_conditional_returns": self.invalid_returns,
        }

    @classmethod
    def from_dw_run(cls, manifest: Manifest, report: Report) -> DriftReport:
        """
        Creates a new instance of this class based on a manifest and work report

        Args:
            manifest (Manifest): The manifest for the digital worker.
            report (Report): The work report of the digital worker's execution.

        Returns:
            DriftReport: A new report.
        """
        manifest_step_ids = manifest.steps_by_id.keys()
        illegal_steps = [
            step.step_id
            for step in report.workflow
            if step.step_id not in manifest_step_ids
        ]

        # Check for valid conditional return types
        invalid_returns = []
        for step_report in report.workflow:
            if step_report.step_type is StepType.CONDITIONAL:
                if type(step_report.outputs) is not bool:
                    invalid_returns.append(step_report.step_id)

        invalid_jumps = []
        state_machine = StateMachine.from_steps(manifest.workflow)
        for index, step_report in enumerate(report.workflow):
            if step_report.step_type in [StepType.CONDITIONAL, StepType.BRANCH]:
                # Determine what the next step *should* be for conditional and branch
                # steps based on the manifest
                expected_next_step_id: Optional[str]
                try:
                    # node = state_machine.nodes_by_id[step_report.step_id]
                    node = find_node_in_tree_by_id(
                        state_machine.nary_tree, step_report.step_id
                    )
                    expected_next_step_id = node.next(step_report.outputs)
                except KeyError:
                    expected_next_step_id = None

                # Find what the next step *actually* was in the work report
                actual_next_step_id: Optional[str]
                if step_report != report.workflow[-1]:
                    actual_next_step_id = report.workflow[index + 1].step_id
                else:
                    actual_next_step_id = None

                # Check if the next step was supposed to be the next step
                if not expected_next_step_id != actual_next_step_id:
                    invalid_jumps.append(step_report.step_id)

        return cls(
            step_ids_missing_from_manifest=illegal_steps,
            invalid_jumps=invalid_jumps,
            invalid_returns=invalid_returns,
        )


def find_node_in_tree_by_id(tree: NaryTree, desired_id: str) -> Node:
    """
    Search an ``NaryTree`` for a ``Node`` with a `uuid`
    equal to `desired_id`.

    Args:
        tree (NaryTree): The root tree to start the search from.
        desired_id: The UUID of the desired ``Node``.

    Returns:
        Node: The found node.

    Raises:
        KeyError: If no node was found with that UUID.
    """

    def _search(current_tree: NaryTree):
        """
        Helper function to search the tree recursively.
        """
        if current_tree.root.uuid == desired_id:
            return current_tree.root

        for child in current_tree.root.children:
            child_result = find_node_in_tree_by_id(child, desired_id)
            if child_result:
                return child_result
        return None

    result = _search(tree)
    if not result:
        raise KeyError(f"Could not find node with id: {desired_id}")
    return result
