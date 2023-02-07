import bpy
import os
import subprocess


class BuildOperator(bpy.types.Operator):
    bl_idname = "tb.build"
    bl_label = "Build"

    def execute(self, context):
        abs_path = os.path.abspath(context.scene.toybox.project_path)

        subprocess.run("cmake --preset x64-windows-ninja-llvm", cwd=abs_path)
        subprocess.run(
            "cmake --build --preset debug-x64-windows-ninja-llvm", cwd=abs_path)
        return {'FINISHED'}


class RunOperator(bpy.types.Operator):
    bl_idname = "tb.run"
    bl_label = "Run"

    def execute(self, context):
        abs_path = os.path.abspath(context.scene.toybox.project_path)
        exe_path = abs_path + "/build/x64/windows/Debug"

        subprocess.Popen(os.path.join(
            exe_path, "thehighseas.exe"), cwd=exe_path)
        return {'FINISHED'}
