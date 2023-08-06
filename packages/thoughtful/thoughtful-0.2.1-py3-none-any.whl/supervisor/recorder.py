from enum import Enum
from typing import Optional


class Recorder:
    def __init__(self):
        self.data = []
        self.messages = []

    def record_data(
        self, log_data: any, *, label: str, description: Optional[str] = None
    ) -> any:
        """
        Record data to the data cache, which will be logged
        for the current step. You must provide a label which will be used to
        identify and label the data in the report.

        You can optionally supply a description to further clarify the data

        example:

            >>> reporter.record_data_change("Ticket#123",
                                            label="Support Ticket",
                                            description="The support ticket being used")

            workflow: [
                {
                "step_id": "1.2.3",
                "data_log": {
                    "type": "data",
                    "data": "Ticket#123",
                    "title": "Support Ticket",
                    "description": "The support ticket being used"
                }
            }
        """

        new_entry = {
            "type": RecordType.DATA,
            "data": log_data,
            "label": label,
            "description": description,
        }

        # cache the record (flushed at end of step execution)
        self.data.append(new_entry)

        # returns original data
        return log_data

    def record_data_change(
        self, before: any, after: any, *, label: str, description: Optional[str] = None
    ) -> any:
        """
        Record data change/transformations on the current step.

        example:

            >>> me = "Dave Arel"
            >>> reporter.record_data_change(me,
                                            upper(me),
                                            label="Uppercased My Name",
                                            description="Capitalizes my full name")

            workflow: [
                {
                "step_id": "1.2.3",
                "data_log": {
                    "type": "transformed",
                    "before": "Dave Arel",
                    "after": "DAVE AREL",
                    "label": "Uppercased Name",
                    "description": "Capitalizes the full name"
                }
            }

        """

        transformation = {
            "type": RecordType.TRANSFORMATION,
            "before": before,
            "after": after,
        }
        self.record_data(transformation, label=label, description=description)
        return before

    def record_message(self, message: str) -> None:
        """
        Record message to the message cache, which will be flushed into
        the message log at the end of the current step.

        example:

            >>> reporter.record_data_change("message")

            workflow: [
                {
                "step_id": "1.2.3",
                "message_log": ["message"]
            }

        """
        # cache the record (flushed at end of step execution)
        self.messages.append(message)


class RecordType(str, Enum):
    """
    Enum for the different types of manually recorded data structures.

    Data structures of these types must be serializable.

    Transformed data structures can be a string, number, object or list of
    any of the former, as long as the data is serializable. This could be as
    simple as a string being capitalized, trimmed, singularized, etc, or it
    can be as complex as a large tabular data set  cleaned up to
    remove duplicates.

    This should be used as a way to record a transformation of data within a
    step so that the data can later be consumed in different ways, such as a
    visual-diff data coming out, or debuggin to diagnose whether the problem
    was the data going in or the data going out.
    """

    #: A record that is simply recording a static data value
    DATA = "data"

    #: A record that is a step_outputs of data being transformed
    TRANSFORMATION = "transformation"
