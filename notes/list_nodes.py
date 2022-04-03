# macro_id = list_shader_nodes
# macro_label = List all shader node classes
# type: ignore

import bpy
# import bpy_types

from typing import Union, Tuple, Type, Set, List



def find_by_type(basetypes: Union[Type, Tuple[Type]]) -> Set[str]:
    # if the inspect is in the outer scope, it can't be found if this is used
    # as a macro. wufa?
    from inspect import isclass

    matches = set()

    for type_name in dir(bpy.types):
        t = getattr(bpy.types, type_name)

        if not isclass(t):
            continue

        try:
            if not issubclass(t, basetypes):
                continue
        except Exception:
            continue

        matches.update([t.__name__])
        print(t.__name__)
    return matches


things: List[Tuple[type, str]] = [
    (bpy.types.CompositorNode, "Compositor Nodes"),
    (bpy.types.FunctionNode, "Function Nodes"),  # wtf are these?
    (bpy.types.GeometryNode, "Geometry Nodes"),
    (bpy.types.ShaderNode, "Shader Nodes"),
    (bpy.types.TextureNode, "Texture Nodes"),
]

for thing in things:
    basetypes = thing[0]
    basename = thing[1]

    print(f"{basename}:")
    print("\n".join(find_by_type(basetypes)))
    print("\n")
