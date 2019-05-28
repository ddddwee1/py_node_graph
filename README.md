# py_node_graph

I come back and remake this thing, finally.

I will re-name it once finish the first prototype.

## TO-DO

-[x] Main block window (finished on 5/27)

-[x] Nodes & Connections with naive node definition (finished on 5/27)

-[x] Serialization of node graph (finished on 5/28)

-[x] Unserialization of node graph (finished on 5/28)

-[ ] Modification of node definition

-[ ] View & edit intrinsic properties of nodes 

-[ ] Python code generator

-[ ] Modify the GUI

-[ ] Finish the prototype

### Requirement:

- PyQt5
- Python 3.x

### Description

This is a naive implementation of node graph with PyQt.

It is still in the testing process.

Program entry: 'main_test.py'

#### Pre-defined Node Type

The pre-def node types are stored in graph_util.py

The structure of node types:

```
Dict typeDict {str typeName : List attributes}
List attributes [List attributeNames, Dict attributeProperty]
Dict attributeProperty {str attributeName : Dict property}
Dict property {'hasPlug': bool, 'hasSocket': bool}
```
