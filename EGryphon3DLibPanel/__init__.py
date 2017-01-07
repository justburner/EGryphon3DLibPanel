bl_info = {
    "name": "Gryphon 3D Engine Library Mesh2String",
    "author": "JustBurner",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "Properties > Object",
    "description": "Enable to export mesh data into the library as string.",
    "warning": "",
    "wiki_url": "",
    "category": "Pico-8",
}

import bpy

class Converter:
    object_name = ""
    faces_str = ""
    vertices_str = ""

    def _gf(face):
        return "%02x" % (int(face) & 255)

    def _gv(vert):
        return "%04x" % (int(vert * 256) & 65535)

    @classmethod
    def clear_data(self):
        self.faces_str = ""
        self.vertices_str = ""

    @classmethod
    def update_mesh(self):
        context = bpy.context
        pdata = context.scene.EGryphon3DLibPanel
        # Sanity checks
        obj = context.object
        if obj.type != "MESH":
            return False
        mesh = obj.data
        if len(mesh.vertices) >= 256:
            return False
        # Calculate tessellation
        mesh.update(calc_tessface=True)
        object_name = obj.name
        self.faces_str = ""
        self.vertices_str = ""
        # Work with faces first
        for f in mesh.tessfaces:
            numvertices = len(f.vertices)
            if numvertices == 3:    # Triangles
                f0 = f.vertices[0]+1
                f1 = f.vertices[1]+1
                f2 = f.vertices[2]+1
                self.faces_str += self._gf(f0) + self._gf(f1) + self._gf(f2)
            elif numvertices == 4:  # Quads
                f0 = f.vertices[0]+1
                f1 = f.vertices[1]+1
                f2 = f.vertices[2]+1
                f3 = f.vertices[3]+1
                self.faces_str += self._gf(f0) + self._gf(f1) + self._gf(f2)
                self.faces_str += self._gf(f0) + self._gf(f2) + self._gf(f3)
        # Work with vertices
        for f in obj.data.vertices:
            vert = f.co
            if pdata.transform:
                vert = obj.matrix_world * vert
            self.vertices_str += self._gv(vert.x) + self._gv(vert.z) + self._gv(-vert.y)
        return True

def faces_get(self):
    return Converter.faces_str

def vertices_get(self):
    return Converter.vertices_str

def null_set(self, value):
    return None

class Panel_Update(bpy.types.Operator):
    bl_label = "Update mesh data"
    bl_idname = "object.egryphon3dlib_update"
    bl_description = "Update mesh data into strings"
  
    def execute(self, context):
        Converter.update_mesh()
        return {'FINISHED'}

class Panel_ClipboardFaces(bpy.types.Operator):
    bl_label = "Faces"
    bl_idname = "object.egryphon3dlib_copyfaces"
    bl_description = "Copy faces data string to clipboard"
 
    def execute(self, context):
        context.window_manager.clipboard = Converter.faces_str
        return {'FINISHED'}

class Panel_ClipboardVertices(bpy.types.Operator):
    bl_label = "Vertices"
    bl_idname = "object.egryphon3dlib_copyvertices"
    bl_description = "Copy vertices data string to clipboard"
 
    def execute(self, context):
        context.window_manager.clipboard = Converter.vertices_str
        return {'FINISHED'}

class Panel_Settings(bpy.types.PropertyGroup):
    name="Gryphon 3D Engine Library Panel"
    """Properties"""
    enable = bpy.props.BoolProperty(
        name="Enable add-on",
        description="Enable object inspection for conversion",
        default=False
        )
    transform = bpy.props.BoolProperty(
        name="Apply transformations",
        description="Apply world matrix tranformations for each vertex",
        default=True
        )
    autoupdate = bpy.props.BoolProperty(
        name="Auto-Update",
        description="Automatically update output data",
        default=True
        )
    faces_data = bpy.props.StringProperty(
        name="Faces",
        description="Faces data to be used on your game, read-only.",
        get=faces_get,
        set=null_set
        )
    vertices_data = bpy.props.StringProperty(
        name="Vertices",
        description="Vertices data to be used on your game, read-only.",
        get=vertices_get,
        set=null_set
        )

class Panel(bpy.types.Panel):
    """Panel in the Object properties window"""
    bl_label = "Gryphon 3D Engine Library"
    bl_idname = "EGryphon3DLibPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def calc_triangles(self, polygons):
        triangles=0
        for p in polygons:
            triangles += len(p.vertices)-2
        return triangles

    def draw(self, context):
        layout = self.layout
        obj = context.object
        pdata = context.scene.EGryphon3DLibPanel

        row = layout.row()
        row.prop(pdata, "enable")

        if not pdata.enable:
            return

        if obj.type != "MESH":
            row = layout.row()
            row.label(text="Select a mesh!", icon='ERROR')
            return

        mesh = obj.data
        numtriangles = self.calc_triangles(mesh.polygons)

        row = layout.row()
        row.label(text="Triangles: %i" % numtriangles, icon='FACESEL_HLT')
        row = layout.row()
        row.label(text="Vertices: %i / 255" % len(mesh.vertices), icon='EDITMODE_HLT')

        row = layout.row()
        row.prop(pdata, "transform")
        row = layout.row()
        row.prop(pdata, "autoupdate")

        if len(mesh.vertices) >= 256:
            row = layout.row()
            row.label(text="Too many vertices! Must be < 256", icon='ERROR')
        else:
            if obj.name != Converter.object_name:
                Converter.clear_data()
                Converter.object_name = obj.name
                Converter.update_mesh()
            row = layout.row()
            row.label(text="Faces / Vertices output:")
            row = layout.row()
            row.prop(pdata, "faces_data")
            row = layout.row()
            row.prop(pdata, "vertices_data")
            if not pdata.autoupdate:
                row = layout.row()
                row.operator(Panel_Update.bl_idname)

            row = layout.row()
            row.label(text="Copy to clipboard:")
            row = layout.row()
            row.operator(Panel_ClipboardFaces.bl_idname)
            row.operator(Panel_ClipboardVertices.bl_idname)
            if pdata.autoupdate:
                Converter.update_mesh()

def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.EGryphon3DLibPanel = bpy.props.PointerProperty(type=Panel_Settings)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
