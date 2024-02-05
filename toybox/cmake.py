import bpy
import os
from pathlib import Path
import subprocess
import threading

def get_out_dir(context):
    abs_path = os.path.abspath(context.scene.toybox.project_path)
    config = Path(context.scene.toybox.build_config)
    preset = context.scene.toybox.build_preset
    preset_opts = preset.split('-')
    arch = Path(preset_opts[0])
    plat = ''
    if 'windows-ninja' in preset:
        plat = 'windows'
    elif 'windows-static-ninja' in preset:
        plat = 'windows-static'
    elif 'windows-vs2022' in preset:
        plat = 'windows-clangcl'
    elif 'windows-static-vs2022' in preset:
        plat = 'windows-static-clangcl'
    plat = Path(plat)
    
    return abs_path / Path('build') / arch  / plat / config
  
def get_exe(context, out_dir):
  exe = Path(context.scene.toybox.project_name + '.exe')
  return out_dir / exe

def run_build(context):
    abs_path = os.path.abspath(context.scene.toybox.project_path)
    config = context.scene.toybox.build_config
    preset = context.scene.toybox.build_preset

    subprocess.run('cmake --preset ' + preset, cwd=abs_path)
    subprocess.run(
        'cmake --build --preset ' + config + '-' + preset, cwd=abs_path)


class BuildOperator(bpy.types.Operator):
    bl_idname = 'tb.build'
    bl_label = 'Build'
    bl_options = {'INTERNAL'}

    def execute(self, context):
        context.window_manager.modal_handler_add(self)

        self.thread = threading.Thread(target=run_build, args=(context,))
        self.thread.start()

        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if self.thread.is_alive():
            return {'PASS_THROUGH'}

        self.report({'INFO'}, 'Build Complete')
        return {'FINISHED'}


class RunOperator(bpy.types.Operator):
    bl_idname = 'tb.run'
    bl_label = 'Run'

    def execute(self, context):
        output_dir = get_out_dir(context)
        exe = get_exe(context, output_dir)

        subprocess.Popen(exe, cwd=output_dir)
        return {'FINISHED'}
