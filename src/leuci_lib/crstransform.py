"""

RSA 25/2/23
This class handles transformations in 3d space from a plabe defined by 3 given points to the origin

"""

class CrsTransform(object):
    def __init__(self, xlen, ylen, zlen, xmap, ymap, zmap, a,b,c,alpha, beta, gamma):
        # PUBLIC INTERFACE
        self.xlen, self.ylen, self.zlen = zlen, ylen, zlen
        self.xmap, self.ymap, self.zmap = xmap, ymap, zmap
        self.a, self.b, self.c = a, b, c
        self.alpha, self.beta, self.gamma = alpha, beta, gamma
        self._create_transformation()

    ########## PUBLIC INTERFACE #############
    def crs_to_xyz(self):
        pass
    def xyz_to_crs(self):
        pass

    ########## PRIVATE INTERFACE #############
    def _create_transformation(self):
        pass

        