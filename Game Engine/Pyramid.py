from Vector import Vector
from Transform import Transform
from Mesh import Mesh
class Pyramid(Mesh):
    def __init__(self,transform = Transform()):
        super().transform = transform
        pyramid_vectors = []
        pyramid_vectors.append(Vector(2,0,2))
        pyramid_vectors.append(Vector(-2,0,2))
        pyramid_vectors.append(Vector(-2,0,-2))
        pyramid_vectors.append(Vector(2,0,-2))
        pyramid_vectors.append(Vector(0,3,0)) 

        modified_pyramid_vectors = []
        for vector in pyramid_vectors:
            modified_vector = vector.vector * transform.scale.vector
            #TODO Implement Rotation
            modified_vector = vector.vector + transform.position.vector
            modified_pyramid_vectors.append(modified_vector)

        super().points = modified_pyramid_vectors

    def get_connected_points(self):
            points = [
                (0, 4),
                (1, 4),
                (2, 4),
                (3, 4),
                (0, 1),
                (1, 2),
                (2, 3),
                (3, 0),
                ]
            return points
        
    def get_faces(self):
        faces = [
            (0,1,4),
            (1,2,4),
            (2,3,4),
            (3,0,4),
            (0,1,2),
            (0,2,3)
            ]
        return faces