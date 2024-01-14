from typing import TypedDict, Sequence


SlotInfo = TypedDict('SlotInfo', {'attr': str, 'type': int, 'max_connections': int})  # keytype: socket or plug
NodeInfo = TypedDict('NodeInfo', {'name': str, 'text': str, 'pos': Sequence[int], 'slots': Sequence[SlotInfo]})
NodeStyle = TypedDict('NodeStyle', {'title_color': Sequence[int], 'text_color': Sequence[int]})

