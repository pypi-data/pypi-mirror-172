# 👷 Supervisor

[![pre-commit](https://github.com/thoughtful-automation/supervisor/workflows/pre-commit/badge.svg?event=push)](https://github.com/thoughtful-automation/supervisor/actions?query=workflow%3Apre-commit+event%3Apush)
[![test](https://github.com/thoughtful-automation/supervisor/workflows/test/badge.svg?event=push)](https://github.com/thoughtful-automation/supervisor/actions?query=workflow%3Atest+event%3Apush)

<img
  title="Supervisor"
  alt="Supervisor — Github Header"
  width="262px"
  height="179.5px"
  align="right"
  src="https://user-images.githubusercontent.com/1096881/147704110-3116d1e3-c278-45d6-b99a-209faf2b17e0.png"
/>

> 🤖 A valid digital worker must be defined and configured by a <u>manifest</u>
> and produce a <u>work report</u> at runtime as defined by
> TA's  [Department of Digital Labor](https://github.com/Thoughtful-Automation/DODL)
> specifications and documentation.<br>

Therefor, 👷 **Supervisor** is a digital worker utility that governs the
runtime and reporting of a Digital Worker by reading it's manifest config,
executing it's workflow, and producing a detailed work report at runtime.

<small>Supervisor supports `Python ≥ 3.7.5`</small>

## Table of Contents

- [Install](#install)
- [Documentation](#documentation)
  - [Setup](#setup)
  - [Rules](#rules)
  - [Conventions](#conventions)
  - [Advanced Usage](#advanced-usage)
- [Contributing](#contributing)
- [Resources](#resources)

## Install

Installation options:

1. From source:

    ```sh
    pip install https://github.com/Thoughtful-Automation/supervisor
    ```

> More, coming soon.

## Documentation

Using `Supervisor` is easy. Below is an overview of the basic components and
integration points behind `Supervisor`.

### Setup

1. **`manifest.yaml`** &mdash; a **Manifest** is required in the root of a
    digital worker.

    The manifest file contains the configuration and workflow process
    documentation. It is used as a "source of truth" to both dictate
    the runtime flow of a digital worker, and report on the details of that runtime.

    Each step should detail the implementation parameters and describe it's
    purpose, not as an abstract concept for the workflow, but as a detailed
    representation of the real workflow.

    The manifest file should only be changed to reflect the real-world workflow
    implementation and in tandem with the customer success team, the proper
    business-logic for the given task.

    > #### :warning: Note
    >
    > The `manifest.yaml` will soon be auto-generated
    > as part of `Otto` workflow.
    >
    > Until then, manifests are created manually, and
    > will be provided prior to any integration with `Supervisor`.

    For a breakdown of manifest fields, see the [Manifest Schema
    Documentation][url:manifest-schema-json]
    in the [:books: Schema Library][url:schema-lib].

    **Example Manifest:**

    ```yaml
    uid: TEST-DW1
    # ... some more fields
    # like name, description, etc
    #
    # but workflow is where you will want to focus:
    workflow:
      - step_id: 1
        title: Example Macro Step 1
        steps:
          - step_id: 1.1
            title: (The title will reflect the PDD)
            description: (The description will reflect the PDD)
            steps:
              - step_id: 1.1.1
                title: Another Title
                description: Steps can have child an infinite number of child steps
                steps: # etc
          - step_id: 1.2
            title: Title 1.2
            description: |-
              For most steps, step_id and title are the only two required params
      # and so on... (see below for more examples)
   ```

2. **`DigitalWorker` subclass**

    The digital worker must be initialized by a subclass of supervisor's
    `DigitalWorker` class.

    An empty `DigitalWorker` might look like this:

    ``` python
    from supervisor import DigitalWorker

    class TestDW(DigitalWorker):
        pass

    # Must be instantiated as part of rcc runner
    if __name__ == "__main__":
      TestDW()
    ```

3. **Steps**

    All `workflow` steps inside of the `manifest.yaml` must have an associated
    step method, tagged using the `@step(1, 1)` decorator**.

    Example Digital Worker Subclass with steps:

    ``` python
    from supervisor import DigitalWorker, Reporter, step

    class TestDW(DigitalWorker):

        @step(1):
        def example_macro_step_1(self):
            # Macro steps are the only non-required step methods.
            # However, they can be used to setup class instantiation,
            # configuration, and other common tasks for that macros set of steps.

        @step(1, 1)
        def example_step_1_1(self):
            # Notice that step ID's are separated by a comma, not a period.
            # Steps can be arbitrarily nested, so it might be @step(2, 1, 2, 3, 3)
            # which would be equivalent to `step_id: 2.1.2.3.3` in the manifest.

        @step(1, 1, 1)
        def example_sub_step(self):
          pass

        @step(1, 2)
        def example_step_2_same_macro(self):
            pass

        # etc.,  etc.

    # Must be instantiated
    if __name__ == "__main__":
      TestDW()
   ```

### Rules

- All steps must have a step method in the digital worker sub class
- All steps should be tagged using the `step` decorator.
- Implementation scripting should correlate with the step within the workflow
  (manifest workflow). This can be delegated to a sub-class, but should be

  example:

  ```python
  @step(1)
  def get_revenue_totals(self):
    self.stripe = Stripe()

  @step(1, 1, 1)
  def login_to_stripe(self):
    (user, pw) = self.stripe.login()
    return { 'user': user }
  ```

### Conventions

- Step method names are arbitrary, but by convention should be correlated to the
  step title.
- Order of steps is arbitrary, but by convention should be in sequential order
  according to the manifest (or the workflow sequence)

### Advanced Usage

Above covers the basic implementation details needed to get started. Below are some
more advanced topics that you should know while using Supervisor.

#### Step Sequence

The sequence of steps are determined by the closest relative position. You can
think of it like an array with child steps. Supervisor's workflow engine starts
at the macro-step level and begins iterating over those steps. It will execute
that step (`1`), then look for the next. Before it continues to a sibling step,
it will look for children step. The next step, if it exists, will be (`1.1`), it
will continue down the children tree until there are no more children, and then
it will execute all sibling steps, linearly across that depth (`1.1.1`, `1.1.2`,
`1.1.3`). When it reaches the final child at that step, it will go back up one
level (`1.2`), execute that step, and continue with the same process (of looking
for children, favoring stepping down over stepping across)

Example step sequence:

```python
['1', '1.1', '1.1.1', '1.1.2', '1.2', '2', '2.1', '2.2', '3', '4', '4.1', 'etc']
```

You can debug the workflow arrangement by printing the `WorkflowEngine`
instance. You can access the workflow instance inside of the `DigitalWorker`
subclass like so:

```python
print(self.supervisor.workflow)
# prints <DigitalWorkflow: Steps=(1, 1.1, 1.2, 1.2.1, 1.2.2, ....)>
```

#### Step Types

There are two major step types in a manifest, which are reflected in the
way the `DigitalWorker` steps need to be implemented.

1. **Sequential Steps**
    Most steps, by default, are sequential steps. This means, when the
    DigitalWorker is done executing that step, it simply moves on to the next
    step.

    These steps can pass data from one step to the next by returning a
    dictionary.

    For example:

    ```python
    @step(1, 1)
    def example_step_1_1(self) -> dict:
        # ... do some work
        some_data = "a string"
        return {
          'some_data': some_data,
          'some_other_data': 123
        }

    @step(1, 1, 1)
    def example_step_1_1_1(self, some_data: str, some_other_data: int):
        # because 1.1.1 is the immediate child of 1.1, this is the next
        # sequential step. If 1.1.1 is the last child (or only child in this case),
        # then the return value of this step would surface in step 1.2
        print(some_data) # prints "a string"
        print(some_other_data) # prints 123
    ```

2. **Conditional Steps**

    Conditional Steps are defined much like sequential steps, except that they
    will contain a `when_true` and/or `when_false` property. The value of these
    properties must be the ID of some step anywhere within the workflow.

    The ony implication on the implementation of this step is that it must
    return a `True` or `False` value.

    For example:

    ```yaml
    - step_id: 1.3
      title: Does this value equal that value?
      when_true: 1.3.2
      when_false: 1.3.1
    ```

    ```python
    @step(1, 3)
    def example_step_1_3(self) -> bool:
        # ... do some work
        # ask the appropriate truthy question:
        return this_value is that_value

    @step(1, 3, 1)
    def example_step_1_3_1(self): # false
        # this will run next if this_value is not that_value
        pass

    @step(1, 3, 2)
    def example_step_1_3_2(self): # true
        # this will run next if this_value is that_value
        pass
    ```

    If one of the truthy properties (`when_true` or `when_false`) are not
    provided, Supervisor will treat it as a sequential step and move to the
    next step in sequential order.

#### Reporting

The following data is reported in each step:

- **Title, Description** &mdash; from the `manifest.yaml`
- **Timestamp** &mdash; when the step started
- **Duration** &mdash; how long the step ran for
- **Status** &mdash; the execution status
- **args** &mdash; the arguments provided to a step
- **returned** &mdash; the return value of a step

You can get a feel for what is reported by the supervisor by looking at
Supervisors test suite [`__snapshots__/test_digitalworker.ambr`][git:test-dw-snapshot]

#### Additional Reporting

Often, there are other metrics, data, and details that are helpful to log within
each step. The following utilities are provided to record adhoc data for the report:

```python
test_data = 123

# Reporter() is a singleton class that contains two
# methods to record adhoc data with:

# You can pass in that data, with no arguments,
# for simple and intuitive results
Reporter().record(test_data)

# But it's encouraged to provide additional context using the
# title and description parameters:
Reporter().record(test_data,
                title="Apples",
                description="The number of apples eaten by Jack")

# If the data is transforming from one thing to another, then
# you can use the record_transformation method to call out the
# transformation before and after:
Reporter().record_transformation(before="TEST", after="test")
Reporter().record_transformation(before={"A": "Dictionary"},
                                           after={"B": "Dictionary"})
```

#### See Tests

You can see more examples and use-cases documented within the tests:

- [Test Manifest][git:test-manifest]
- [Test DigitalWorker][git:test-digitalworker]
- [Work Report Test Snapshot][git:test-dw-snapshot]

## Contributing

Contributions to Supervisor are welcomed!

To get started, see the [contributing guide](CONTRIBUTING.md).

## Resources

Links to related code, documentation, and applications.

[**:books: Schema Library**][url:schema-lib]

  > The JSON-Schema-defined documents used to validate the **Manifest** and the
  > runtime **Work Report**

[**:eagle: Department of Digital
  Labor**][url:dodl]

> Documentation and Specifications for building Digital Workers in *TA's
> ecosystem*, and **Empower**

[**🖥 Empower**][url:dwm]

> The digital Workforce Manager (*DWM*)

[**:robot: Otto**][url:otto]

> The build tool for Digital Workers.

---

<div align="center">

  Made with ❤️ by

  [![Thoughtful Automation](https://user-images.githubusercontent.com/1096881/141985289-317c2e72-3c2d-4e6b-800a-0def1a05f599.png)][url:ta]

</div>

<!--  Link References -->

[url:ta]: https://www.thoughtfulautomation.com/
[url:dwm]: https://app.thoughtfulautomation.com/
[url:otto]: https://github.com/Thoughtful-Automation/otto
[url:dodl]: https://github.com/Thoughtful-Automation/dodl
[url:schema-lib]: https://github.com/Thoughtful-Automation/schemas
[url:manifest-schema-json]:
    https://github.com/Thoughtful-Automation/schemas/blob/main/docs/manifest.schema.md
[git:test-dw-snapshot]:
    https://github.com/Thoughtful-Automation/supervisor/blob/20c5cc7632c6f429206c7471fdf28fd138994901/tests/__snapshots__/test_digitalworker.ambr#L1
[git:test-manifest]:
    https://github.com/Thoughtful-Automation/supervisor/blob/20c5cc7632c6f429206c7471fdf28fd138994901/tests/manifests/test_digitalworke
[git:test-digitalworker]:
    https://github.com/Thoughtful-Automation/supervisor/blob/20c5cc7632c6f429206c7471fdf28fd138994901/tests/test_digitalworker.py
