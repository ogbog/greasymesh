# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "greasymesh",
    "author" : "Oscar Baechler",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}


import bpy








def main(context):

###START



#-----------Create curves, hide Grease Pencil stuff, clean the curves, make the mesh. It assumes there is only one layer on the GP object, and that the GP object is selected
   
    gp = bpy.context.selected_objects[0]
    lname = gp.data.layers[0].info    

#TO DO: Convert the GP stroke point size to the bezier size
    pressures = []
    strokes = gp.data.layers[0].frames[0].strokes 
    for stroke in strokes:
        points = stroke.points #maybe make layer 0
        for i in points:
            pressures.append (i.pressure)


    bpy.ops.gpencil.convert(type='CURVE', timing_mode='LINEAR', use_timing_data=False)
    gp.hide_viewport=True

    cu = bpy.data.objects[lname]
    
    splines = cu.data.splines
    bezpoints = []
    ptcount = 0
    counter = 0

    for spl in splines:
        points = spl.bezier_points 
        for point in points:
            point.radius=pressures[counter]*100
            counter += 1        

    print(counter)
    print (len(pressures))
    print (len(points))


#    cu.name='clayCurves'
    cu.data.fill_mode='FULL'
    cu.data.bevel_depth=0.01
    cu.data.bevel_resolution=2
    cu.data.resolution_u=1


#Next to put these values into the curve point values

#data.splines[0].bezier_points[0].radius



#hide the old GP strokes and make the new curves the active object

    bpy.ops.object.select_all(action='DESELECT')
    cu.select_set(True)
    bpy.context.view_layer.objects.active=cu


    bpy.ops.object.convert(target='MESH')
    bpy.ops.object.editmode_toggle()
#   
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')

    bpy.ops.mesh.select_all(action='TOGGLE')
    bpy.ops.mesh.fill_holes()

    bpy.ops.object.editmode_toggle()
    bpy.context.object.data.remesh_voxel_size = 0.1

    bpy.ops.object.voxel_remesh()
    

####END 


class Greasymesh(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.greasymesh"
    bl_label = "Greasy Mesh"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(Greasymesh)


def unregister():
    bpy.utils.unregister_class(Greasymesh)


if __name__ == "__main__":
    register()










