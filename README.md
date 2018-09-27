# py_node_graph

### Requirement:

- PyQt5
- Python 3.x

### Description

This is a naive implementation of node graph with PyQt.

Examples can be viewed in main.py

#### Pre-defined Node Type

The pre-def node types are stored in graph_util.py

The structure of node types:

```
Dict typeDict {str typeName : List attributes}
List attributes [List attributeNames, Dict attributeProperty]
Dict attributeProperty {str attributeName : Dict property}
Dict property {'hasPlug': bool, 'hasSocket': bool}
```
