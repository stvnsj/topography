

class MasterPointSet:
    """Encapsulates the master set of points"""
    
    def __init__ (self, filename):
        self.pointSet = set()
    
    def __init_data__ (self, filename):
        """Initialize the master point set."""
        pointSet = set()
        self.matrix = np.genfromtxt(filename, delimiter=',', skip_header=0, usecols=(0))   
    
    def contains (self, point) :
        """Returns True if MasterPointSet contains the queried point.
        The input is a dm in string form like '13.000' """
        return (point in self.pointSet)
    

