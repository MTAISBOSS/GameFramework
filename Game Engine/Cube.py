from Vector import Vector
from Transform import Transform
from Mesh import Mesh
class Cube(Mesh):
    def __init__(self,transform = Transform()):
        self.transform = transform
        cube_vectors = []
        cube_vectors.append(Vector(1,1,1))
        cube_vectors.append(Vector(1,1,-1))
        cube_vectors.append(Vector(1,-1,1))
        cube_vectors.append(Vector(1,-1,-1))
        cube_vectors.append(Vector(-1,1,1))
        cube_vectors.append(Vector(-1,1,-1)) 
        cube_vectors.append(Vector(-1,-1,1))
        cube_vectors.append(Vector(-1,-1,-1))

        modified_cube_vectors = []
        for vector in cube_vectors:
            modified_vector = vector.vector * transform.scale.vector
            #TODO Implement Rotation
            modified_vector = vector.vector + transform.position.vector
            modified_cube_vectors.append(modified_vector)

        self.cube = modified_cube_vectors
