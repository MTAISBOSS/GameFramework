from Transform import Transform

class GameObject:
    def __init__(self,name="GameObject"):
        self.components = []
        self.transform = Transform()

    def add_component(self,cls_component):
        '''
        Adds component if not exist in current game object's components
        '''
        component = cls_component(self)
        self.components.append(component)
        return component
    
    def get_component(self,cls_component):
        for component in self.components:
            if isinstance(component,cls_component):
                return component
        return None

    def update(self):
        for component in self.components:
            component.update()