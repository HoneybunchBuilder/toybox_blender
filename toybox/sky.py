import bpy

class TbSky(bpy.types.PropertyGroup):
    cirrus: bpy.props.FloatProperty(name='cirrus', default=0.4, min=0, max=1)
    cumulus: bpy.props.FloatProperty(name='cumulus', default=0.8, min=0, max=1)

class TbSkyPanel(bpy.types.Panel):
    bl_parent_id = 'OBJECT_PT_tb_components_panel'
    bl_idname = 'OBJECT_PT_tb_sky_panel'
    bl_label = 'Sky'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'
    
    @classmethod
    def poll(self, context):
        return context.object is not None and 'sky' in context.object

    def draw(self, context):
        layout = self.layout
        comp = context.object.tbsky
        
        layout.prop(comp, 'cirrus')
        layout.prop(comp, 'cumulus')


def register():
    bpy.types.Object.tbsky = bpy.props.PointerProperty(type=TbSky)