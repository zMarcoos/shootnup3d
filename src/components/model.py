import trimesh
from OpenGL.GL import *
from PIL import Image
import numpy as np
import glm

class Model:
    def __init__(self, filename):
        self.model = trimesh.load(filename, force='glb')
        self.texture_ids = {}
        self.gl_list = None
        self._bounding_box = self.model.bounding_box_oriented.bounds

    def load_texture(self, image_path):
        image = Image.open(image_path)
        image = image.convert('RGBA')
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image_data = np.array(image, dtype=np.uint8)

        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_data.shape[1], image_data.shape[0], 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        glBindTexture(GL_TEXTURE_2D, 0)
        return tex_id

    def generate(self):
        if self.gl_list is None:
            self.gl_list = glGenLists(1)
            glNewList(self.gl_list, GL_COMPILE)
            glPushAttrib(GL_CURRENT_BIT | GL_TEXTURE_BIT)
            glEnable(GL_TEXTURE_2D)
            glFrontFace(GL_CCW)

            for mesh in self.model.geometry.values():
                vertices = mesh.vertices
                faces = mesh.faces
                normals = mesh.vertex_normals
                texcoords = mesh.visual.uv
                material = mesh.visual.material

                texture_id = None
                if material and hasattr(material, 'image') and material.image is not None:
                    texture_id = self.load_texture(material.image)
                    self.texture_ids[material.name] = texture_id

                if texture_id:
                    glBindTexture(GL_TEXTURE_2D, texture_id)
                    glEnable(GL_TEXTURE_2D)
                else:
                    glDisable(GL_TEXTURE_2D)
                    if hasattr(material, 'diffuse'):
                        glColor3fv(material.diffuse)
                    else:
                        glColor3f(1.0, 1.0, 1.0)

                glBegin(GL_TRIANGLES)
                for face in faces:
                    for idx in face:
                        if texcoords is not None:
                            glTexCoord2fv(texcoords[idx])
                        if normals is not None:
                            glNormal3fv(normals[idx])
                        glVertex3fv(vertices[idx])
                glEnd()

            glDisable(GL_TEXTURE_2D)
            glPopAttrib()
            glEndList()

    def get_bounding_box(self):
        min_corner, max_corner = self._bounding_box
        return {'min': glm.vec3(min_corner[0], min_corner[1], min_corner[2]),
                'max': glm.vec3(max_corner[0], max_corner[1], max_corner[2])}

    def render(self):
        if self.gl_list is None:
            self.generate()
        glCallList(self.gl_list)

    def free(self):
        if self.gl_list:
            glDeleteLists(self.gl_list, 1)
            self.gl_list = None
        glDeleteTextures(list(self.texture_ids.values()))
