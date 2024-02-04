import bpy

components = [
      ('rigidbody', 'Rigidbody', ''),
      ('ocean', 'Ocean', ''),
      ('sky', 'Sky', ''),
    ]

class TbComponents(bpy.types.PropertyGroup):
  comp_sel: bpy.props.EnumProperty(name='Type', items=components)

class TbComponentAddOperator(bpy.types.Operator):
  bl_idname = 'tb.component_add'
  bl_label = 'Add Component'
  
  component: bpy.props.EnumProperty(name='Type', items=components)
  
  def execute(self, context):
    if self.component in context.object:
      print('Already have ', self.component)
    else:
      context.object[self.component] = 1
    
    return {'FINISHED'}

class TbComponentRemoveOperator(bpy.types.Operator):
  bl_idname = 'tb.component_remove'
  bl_label = 'Remove Component'
  
  component: bpy.props.EnumProperty(name='Type', items=components)
  
  def execute(self, context):
    if self.component in context.object:
      del context.object[self.component]
    
    return {'FINISHED'}

class TbComponentsPanel(bpy.types.Panel):
    bl_idname = 'OBJECT_PT_tb_components_panel'
    bl_label = 'Toybox Components'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'
    
    @classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout

        layout.prop(context.object.tb_components, 'comp_sel')
        selection = context.object.tb_components.comp_sel
        if selection in context.object:
          op = layout.operator(TbComponentRemoveOperator.bl_idname)
        else:
          op = layout.operator(TbComponentAddOperator.bl_idname)
        op.component = selection

def register():
    bpy.types.Object.tb_components = bpy.props.PointerProperty(type=TbComponents)