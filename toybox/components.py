import bpy
import sys
import json
import subprocess

from . cmake import *
tb_components = []
tb_component_registry = []
tb_prop_groups = {}

def component_items(self, context):
  return tb_components

def comp_draw(self, context, meta):
  layout = self.layout
  for name in meta:
    layout.prop(context.object.tb_rigidbody, name)

def comp_poll(self, context, lower_name):
  return context is not None and lower_name in context.object.tb_components

class TbRefreshComponents(bpy.types.Operator):
  bl_idname = 'tb.refresh_components'
  bl_label = 'Refresh Components'

  def execute(self, context):
    output_dir = get_out_dir(context)
    exe_path = get_exe(context, output_dir)
    if(not os.path.exists(exe_path)):
      run_build(context)
    if(not os.path.exists(exe_path)):
      # Build failed?
      return {'ERROR'}
    
    # Run the project with --info
    exe = get_exe(context, output_dir)
    meta = subprocess.run(executable=exe, args=['--info'], shell=True, cwd=output_dir, stdout=subprocess.PIPE).stdout
    
    # Clear existing registries
    for key,val in tb_prop_groups.items():
      if hasattr(bpy.types.Object, key):
        delattr(bpy.types.Object, key)
        bpy.utils.unregister_class(value)
      
    for comp in tb_component_registry:
      if hasattr(bpy.types, comp):
        bpy.utils.unregister_class(comp)
    tb_component_registry.clear()
    tb_components.clear()
    
     # parse output json to a reflection dict
    meta_json = json.loads(meta)

    # Register each component type
    for comp_name in meta_json:
      comp_meta = meta_json[comp_name]
      lower_name = comp_name.lower()
      
      tb_components.append((lower_name, comp_name, ''))
      prop_class_name = 'Tb' + comp_name
      panel_class_name = prop_class_name + 'Panel'
      prop_name = 'tb_' + lower_name
      idname = 'OBJECT_PT_tb_' + lower_name
      
      poll_fn = lambda self,context: comp_poll(self, context, lower_name)
      draw_fn = lambda self,context: comp_draw(self, context, comp_meta)
      
      prop_class = type(prop_class_name, 
                        (bpy.types.PropertyGroup,),
                        {})
      for meta_name in comp_meta:
        meta_val = comp_meta[meta_name]
        meta_type = meta_val[0]
        meta_params = meta_val[0:]
        if meta_type == 'bool':
          prop_class.__annotations__[meta_name] = bpy.props.BoolProperty(name=meta_name, default=False)
        elif meta_type == 'float':
          flt_min = sys.float_info.min
          flt_max = sys.float_info.max
          if 'range' in meta_params:
            val_range = meta_params['range']
            flt_min = val_range[0]
            flt_max = val_range[1]
          prop_class.__annotations__[meta_name] = bpy.props.FloatProperty(name=meta_name, default=0.5, min=flt_min, max=flt_max)
        else:
          prop_class.__annotations__[meta_name] = bpy.props.StringProperty(name=meta_name, default='static')

      comp_class = type(panel_class_name, 
                    (bpy.types.Panel, ),
                    { 'bl_idname': idname,
                     'bl_parent_id': 'OBJECT_PT_tb_components_panel',
                     'bl_label': comp_name,
                     'bl_space_type': 'PROPERTIES',
                     'bl_region_type': 'WINDOW',
                     'bl_context': 'object', 
                     'draw': draw_fn,
                     'poll': classmethod(poll_fn),
                     }
                    )

      tb_component_registry.append(panel_class_name)
      tb_prop_groups[prop_class_name] = prop_class
      
      bpy.utils.register_class(prop_class)
      bpy.utils.register_class(comp_class)

      setattr(bpy.types.Object, prop_name, bpy.props.PointerProperty(type=prop_class))

    return {'FINISHED'}

class TbComponents(bpy.types.PropertyGroup):
  comp_sel: bpy.props.EnumProperty(name='Type', items=component_items)

class TbComponentAddOperator(bpy.types.Operator):
  bl_idname = 'tb.component_add'
  bl_label = 'Add Component'
  
  component: bpy.props.EnumProperty(name='Type', items=component_items)
  
  def execute(self, context):
    if self.component in context.object.tb_components:
      print('Already have ', self.component)
    else:
      context.object.tb_components[self.component] = 1
    
    return {'FINISHED'}

class TbComponentRemoveOperator(bpy.types.Operator):
  bl_idname = 'tb.component_remove'
  bl_label = 'Remove Component'
  
  component: bpy.props.EnumProperty(name='Type', items=component_items)
  
  def execute(self, context):
    if self.component in context.object.tb_components:
      del context.object.tb_components[self.component]
    
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
        
        if(len(tb_components) == 0):
          layout.label(text='Refresh Components to populate this panel')
          return

        layout.prop(context.object.tb_components, 'comp_sel')
        selection = context.object.tb_components.comp_sel
        if selection == '':
          return
        
        if selection in context.object.tb_components:
          op = layout.operator(TbComponentRemoveOperator.bl_idname)
        else:
          op = layout.operator(TbComponentAddOperator.bl_idname)
        op.component = selection

def register():
    bpy.types.Object.tb_components = bpy.props.PointerProperty(type=TbComponents)