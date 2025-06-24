from Vector import Vector
from Transform import Transform

class Ethereum:
    def __init__(self,transform = Transform()):
        self.transform = transform
        ethereum_vectors = []
        ethereum_vectors.append(Vector(1,0,1))
        ethereum_vectors.append(Vector(-1,0,1))
        ethereum_vectors.append(Vector(-1,0,-1))
        ethereum_vectors.append(Vector(1,0,-1))
        ethereum_vectors.append(Vector(0,2,0))
        ethereum_vectors.append(Vector(0,-2,0)) 

        modified_ethereum_vectors = []
        for vector in ethereum_vectors:
            modified_vector = vector.vector * transform.scale.vector
            #TODO Implement Rotation
            modified_vector = vector.vector + transform.position.vector
            modified_ethereum_vectors.append(modified_vector)

        self.ethereum = modified_ethereum_vectors

    def get_connected_points(self):
        points = [
            (0, 1),
            (0, 3),
            (0, 4),
            (0, 5),
            (1, 4),
            (1, 5),
            (2, 1),
            (2, 3),
            (2, 4),
            (2, 5),
            (3, 4),
            (3, 5)
            ]
        return points
    
    def get_faces(self):
        faces = [
            (4,0,1),
            (4,1,2),
            (4,2,3),
            (4,0,3),
            (5,0,1),
            (5,1,2),
            (5,2,3),
            (5,0,3)
            ]
        return faces
