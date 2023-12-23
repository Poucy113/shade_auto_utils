bl_info = {
    "name": "Weighted Normal Last & Auto Shade Smooth",
    "description": "Automatically sets weighted normal modifier last.",
    "author": "P.Cy.113",
    "version": (0, 1, 1),
    "blender": (4, 0, 2),
}

import bpy

previous_objects = None

def weighted_normal_last(scene, depsgraph):
    print('Weighted')

    # -- handling new object
    global previous_objects
    print(f'{previous_objects}')
    if previous_objects is not None:
        print('Not none')
        current_objects = set(bpy.data.objects)
        new_objects = current_objects - previous_objects
        previous_objects = current_objects
        print(f'New: {new_objects}')
        
        if new_objects:
            bpy.ops.object.shade_smooth(use_auto_smooth=True)
            return
    
    print('Still weighted')
    # -- handling weighted normal modifier
    if not bpy.context.object:
        return
    object = bpy.context.object
    print('Object: '+str(object))

    if not object.modifiers:
        return
    modifiers = object.modifiers
    print('Modifiers: '+str(modifiers))

    for i in range(len(modifiers)):
        modifier = modifiers[i]
        print('Modifier: '+str(modifier))
        if isinstance(modifier, bpy.types.WeightedNormalModifier) and 'fixed' not in modifier.name.lower():
            object.modifiers.move(i, len(modifiers)-1)
            return

@bpy.app.handlers.persistent
def load_post_auto_shade_smooth(file):
    print('Loading data.objects')
    global previous_objects

    if bpy.data.objects:
        previous_objects = set(bpy.data.objects)
    
    if not weighted_normal_last in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(weighted_normal_last)

def register():
    bpy.app.handlers.depsgraph_update_post.append(weighted_normal_last)
    bpy.app.handlers.load_post.append(load_post_auto_shade_smooth)
    bpy.app.handlers.load_factory_startup_post.append(load_post_auto_shade_smooth)
    # bpy.app.handlers.depsgraph_update_post.append(auto_shade_smooth)


def unregister():
    if weighted_normal_last in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(weighted_normal_last)
    #if auto_shade_smooth in bpy.app.handlers.depsgraph_update_post:
    #    bpy.app.handlers.depsgraph_update_post.remove(auto_shade_smooth)
    if load_post_auto_shade_smooth in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(load_post_auto_shade_smooth)
    if load_post_auto_shade_smooth in bpy.app.handlers.load_factory_startup_post:
        bpy.app.handlers.load_factory_startup_post.remove(load_post_auto_shade_smooth)
