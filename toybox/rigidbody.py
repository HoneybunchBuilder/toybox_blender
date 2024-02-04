import bpy

class TbRigidbody(bpy.types.PropertyGroup):
    layer: bpy.props.EnumProperty(name='Layer', items=[
      ('static', 'Static', ''),
      ('moving', 'Moving', ''),
    ])
    motion: bpy.props.EnumProperty(name='Motion', items=[
      ('static', 'Static', ''),
      ('kinematic', 'Kinematic', ''),
      ('dynamic', 'Dynamic', ''),
    ])
    shape: bpy.props.EnumProperty(name='Shape', items=[
      ('box', 'Box', ''),
      ('cylinder', 'Cylinder', ''),
      ('capsule', 'Capsule', ''),
      ('sphere', 'Sphere', ''),
      ('mesh', 'Mesh', ''),
    ])
    sensor: bpy.props.BoolProperty(name='Sensor', default=False)
    
    rot_x: bpy.props.BoolProperty(name='X', default=True)
    rot_y: bpy.props.BoolProperty(name='Y', default=True)
    rot_z: bpy.props.BoolProperty(name='Z', default=True)
    
    trans_x: bpy.props.BoolProperty(name='X', default=True)
    trans_y: bpy.props.BoolProperty(name='Y', default=True)
    trans_z: bpy.props.BoolProperty(name='Z', default=True)

    half_height: bpy.props.FloatProperty(name='Half Height', default=0.5, min=0)
    radius: bpy.props.FloatProperty(name='Radius', default=0.5, min=0)
    extent: bpy.props.FloatVectorProperty(name='Extent')

class TbRigidbodyPanel(bpy.types.Panel):
    bl_parent_id = 'OBJECT_PT_tb_components_panel'
    bl_idname = 'OBJECT_PT_tb_rigidbody_panel'
    bl_label = 'Rigidbody'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'
    
    @classmethod
    def poll(self, context):
        return context.object is not None and 'rigidbody' in context.object

    def draw(self, context):
        layout = self.layout
        comp = context.object.tbrigidbody

        layout.prop(comp, 'sensor')
        layout.prop(comp, 'layer')
        layout.prop(comp, 'motion')

        layout.label(text='Allowed Rotations')
        row = layout.row()
        row.prop(comp, 'rot_x')
        row.prop(comp, 'rot_y')
        row.prop(comp, 'rot_z')
        
        layout.label(text='Allowed Translations')
        row = layout.row()
        row.prop(comp, 'trans_x')
        row.prop(comp, 'trans_y')
        row.prop(comp, 'trans_z')
        
        layout.prop(comp, 'shape')
        if comp.shape == 'capsule':
          layout.label(text='Capsule Settings')
          layout.prop(comp, 'half_height')
          layout.prop(comp, 'radius')
        if comp.shape == 'cylinder':
          layout.label(text='Cylinder Settings')
          layout.prop(comp, 'half_height')
          layout.prop(comp, 'radius')
        elif comp.shape == 'sphere':
          layout.label(text='Sphere Settings')
          layout.prop(comp, 'radius')
        elif comp.shape == 'box':
          layout.label(text='Box Settings')
          layout.prop(comp, 'extent')
        elif comp.shape == 'mesh':
          layout.label(text='Attached Mesh Used as Shape')

def register():
    bpy.types.Object.tbrigidbody = bpy.props.PointerProperty(type=TbRigidbody)