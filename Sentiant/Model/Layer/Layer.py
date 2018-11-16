from numpy import array
from Sentiant.Model import Entity


class Layer(array):

    LastId = 0

    def __init__(self, w, h):
        super().__init__(self, (w, h), type=Entity)



    def Append(self, entity, x, y):
        """Append an entity (entity) on this Layer in position (x, y)"""
        self[x, y] = entity

    def ToList(self):
        """Get a list of all the entities on the layer"""
        return [it for it in self if it]

    def Remove(self, ref):
        """Remove an entity by reference (ref)"""
        pass

    def Pop(self, ref):
        """Pop an entity out of the layer by ref"""
        return None

    def GetXYByRef(self, ref):
        """ Get position of an entity by reference (ref)"""
        return

    def Count(self):
        """Get the number of entity on layer"""
        return len(self.ToList())

    def __iter__(self):
        """Get an iterator of this layer"""
        for i in range(self.width):
            for j in range(self.height):
                yield self[i, j]

    def ForEach(self, f):
        """Apply a function (f) to all entities of this layer"""
        for e in self:
            f(e)

    @staticmethod
    def GetNewId():
        """Get new id of entity for this layer"""
        Layer.LastId += 1
        return Layer.LastId