# oak-build

A make-like build system written on python


## How to use

Create `oak_build.py` file in your project directory.
Every method marked with `@task` decorator can be called from CLI.

```python
from pathlib import Path

from oak_build import task


@task
def create_file():
    with open(Path("result.txt"), "w") as txt:
        txt.write("test content\n")
```

To execute `create_file` task call `oak create_file` from console.

## Task dependencies

You can link dependent tasks with `depends_on` parameter.

```python
from oak_build import task, run


@task
def unit_tests():
    run("poetry run pytest tests")


@task
def integration_tests():
    run("poetry run pytest integration_tests")


@task(
    depends_on=[
        unit_tests,
        integration_tests,
    ]
)
def tests():
    pass
```

When `oak tests` is called oak build will execute `unit_tests` and `integration_tests` tasks as well.

## Examples

For examples see [integration tests files](integration_tests/resources) and self build [oak_file.py](oak_file.py).
