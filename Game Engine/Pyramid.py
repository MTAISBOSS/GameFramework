from Vector import Vector
from Transform import Transform
from Mesh import Mesh
class Pyramid(Mesh):
    def __init__(self,transform = Transform()):
        self.transform = transform
        pyramid_vectors = []
        pyramid_vectors.append(Vector(2,0,2))
        pyramid_vectors.append(Vector(-2,0,2))
        pyramid_vectors.append(Vector(-2,0,-2))
        pyramid_vectors.append(Vector(2,0,-2))
        pyramid_vectors.append(Vector(0,2,0)) 

        modified_pyramid_vectors = []
        for vector in pyramid_vectors:
            modified_vector = vector.vector * transform.scale.vector
            #TODO Implement Rotation
            modified_vector = vector.vector + transform.position.vector
            modified_pyramid_vectors.append(modified_vector)

        self.pyramid = modified_pyramid_vectors
