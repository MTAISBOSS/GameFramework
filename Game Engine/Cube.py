from Vector import Vector
from Transform import Transform
from Mesh import Mesh
class Cube(Mesh):
    def __init__(self,transform = Transform()):
        super().transform = transform
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

        super().points = modified_cube_vectors

    def get_connected_points(self):
        points = [
            (0, 1),
            (0, 2), 
            (0, 4),
            (1, 3), 
            (1, 5),
            (2, 3), 
            (2, 6),
            (3, 7),
            (4, 5), 
            (4, 6),
            (5, 7),
            (6, 7)
        ]
        return points

    
    def get_faces(self):
        faces = [
            # front
            (0, 2, 4),
            (2, 6, 4),

            # back
            (1, 3, 5),
            (3, 7, 5),

            # right
            (0, 1, 2),
            (1, 3, 2),

            # left
            (4, 5, 6),
            (5, 7, 6),

            # top
            (0, 1, 4),
            (1, 5, 4),

            # bottom
            (2, 3, 6),
            (3, 7, 6)
        ]
        return faces
