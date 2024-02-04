import bpy

max_waves = 8

class TbOceanWave(bpy.types.PropertyGroup):
    direction: bpy.props.FloatVectorProperty(size=2, name='Direction')
    steepness: bpy.props.FloatProperty(name='Steepness')
    wavelength: bpy.props.FloatProperty(name='Wavelength')

def update_waves(self, value):
  ocean = bpy.context.object.tbocean
  prev = []
  for wave in ocean.waves:
    prev.append(wave)
  ocean.waves.clear()

  for i in range(ocean.wave_count):
    wave = ocean.waves.add()
    if i in range(len(prev)):
      wave = prev[i]

class TbOcean(bpy.types.PropertyGroup):
    wave_count: bpy.props.IntProperty(name='Wave Count', default=0, min=1, max=max_waves, update=update_waves)
    waves: bpy.props.CollectionProperty(type=TbOceanWave)

class TbOceanPanel(bpy.types.Panel):
    bl_parent_id = 'OBJECT_PT_tb_components_panel'
    bl_idname = 'OBJECT_PT_tb_ocean_panel'
    bl_label = 'Ocean'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'
    
    @classmethod
    def poll(self, context):
        return context.object is not None and 'ocean' in context.object

    def draw(self, context):
        layout = self.layout

        wave_count = layout.prop(context.object.tbocean, 'wave_count')
        for wave in context.object.tbocean.waves:
          layout.prop(wave, 'direction')
          layout.prop(wave, 'steepness')
          layout.prop(wave, 'wavelength')

def register():
    bpy.types.Object.tbocean = bpy.props.PointerProperty(type=TbOcean)
