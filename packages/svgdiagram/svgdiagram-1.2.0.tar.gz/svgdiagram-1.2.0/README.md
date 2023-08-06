# SVG Diagram

Library for creating `*.svg` diagrams (Gantt, Network, GitBranching)
with also eports available to `*.png`, `*.eps`, `*.ps` (through `cariosvg`).

The library uses its own library for creating the `*.svg` files.

## Install

```
pip install svgdiagram
```

## Diagrams

### Gantt

The creation of a Gantt chart is controlled trough a dictionary / json file.
Executing the script

```python
from svgdiagram import Gantt

content = {
    "swimlanes": [
        {
            "name": "releases",
            "milestones": [
                {
                    "name": "candidate",
                    "due_date": "2022-09-02",
                },
                {
                    "name": "release",
                    "due_date": "2022-09-08",
                },
            ],
            "tasks": [
                {
                    "name": "bugfix",
                    "start_date": "2022-09-02",
                    "end_date": "2022-09-08",
                }
            ]
        }
    ]
}

gantt = Gantt(content)
gantt.write_svg('./readme/images/simple_gantt.svg')
```

results in the following Gantt chart:

![Simple Gantt](./readme/images/simple_gantt.svg)
