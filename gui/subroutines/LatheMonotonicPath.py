import math
from abc import ABCMeta, abstractmethod
from GCoder import *
import copy

class LatheTool:
    """
        Abstract class
    """
    __metaclass__ = ABCMeta
    @abstractmethod
    def tipDisplacement(self, t):
        """
            Returns the displacement vector from the virtual tip
            to the point of the tool tangent to the unitary vector t,
            that is the tangent vector of the path.
            The virtual tip is the point of intersection of the lines
            where the tool touches the x and z constant lines.
        """
        pass

class LatheToolCircularRightExternal(LatheTool):
    def __init__(self, rc):
        self.rc = float(rc) # tip radius

    def tipDisplacement(self, t):
        return ([self.rc * (1.0+t[1]),self.rc * (1.0-t[0])])

class LatheToolCircularLeftExternal(LatheTool):
    def __init__(self, rc):
        self.rc = float(rc) # tip radius

    def tipDisplacement(self, t):
        return ([self.rc * (-1.0+t[1]),self.rc * (1.0-t[0])])

class LatheToolCircularLeftInternal(LatheTool):
    def __init__(self, rc):
        self.rc = float(rc) # tip radius

    def tipDisplacement(self, t):
        return ([self.rc * (1.0-t[1]),self.rc * (1.0-t[0])])

def getDisplacements(path):
    """
        Returns dpath_k = path_k - path_{k-1}
    """
    dpath = []
    for i in range(1,len(path)):
        dpath.append([path[i][0]-path[i-1][0],path[i][1]-path[i-1][1]])
    return dpath

def getTangentUnitaryVector(path):
    """
        Returns the unitary vector tangent to the path
    """
    dpath = getDisplacements(path)
    t = []
    for i in range(0, len(dpath)):
        dz = dpath[i][0]
        dx = dpath[i][1]
        ds = math.sqrt(dx*dx+dz*dz)
        t.append([dz/ds,dx/ds])
    return t


def isRadiusMonotonicallyDecreasing(path):
    """
        Returns True if the the radius decreases monotonically with increasing z. Otherwise, returns False.
    """
    dpath = getDisplacements(path)
    N=len(dpath)
    for i in range(0,N):
        dz = dpath[i][0]
        dx = dpath[i][1]
        if ( dx > 1E-10 or dz < -1E-10 ):
            return False
    return True

def isRadiusMonotonicallyIncreasing(path):
    """
        Returns True if the the radius increases monotonically with increasing z. Otherwise, returns False.
    """
    dpath = getDisplacements(path)
    N=len(dpath)
    for i in range(0,N):
        dz = dpath[i][0]
        dx = dpath[i][1]
        if ( dx < -1E-10 or dz < -1E-10 ):
            return False
    return True

def getToolPath(path, tool):
    """
        Returns the tool path R of a desired path r
        based on tool characteristics
    """
    # Calculating dpath_k = path_k-path_{k-1} 
    dpath = getDisplacements(path)
    # Calculating the unitary tangent vectors to path
    tv = getTangentUnitaryVector(path)
    # Calculating the displacement of the virtual tip to the real tip
    # The virtual tip is the point where the tool touches the z and the x axis of a cylinder
    T = []
    for t in tv:
        T.append(tool.tipDisplacement(t))
        
    # Getting the number of points
    N=len(path)

    R = [] # tool path
    for k in range(1,N-1):
        dz1 = dpath[k-1][0]
        dx1 = dpath[k-1][1]
        tz1 = T[k-1][0]
        tx1 = T[k-1][1]

        dz2 = dpath[k][0]
        dx2 = dpath[k][1]
        tz2 = T[k][0]
        tx2 = T[k][1]

        z0 = path[k-1][0]
        x0 = path[k-1][1]

        z1 = path[k][0]
        x1 = path[k][1]

        bz = tz1-tz2+dz1
        bx = tx1-tx2+dx1

        delta = dx1*dz2-dx2*dz1

        if ( math.fabs(delta) > 1E-7 ):
            csi=(bx*dz2-bz*dx2)/delta
            #eta=(bx*dz1-bz*dx1)/delta

            Rz = dz1 * csi + z0 - tz1
            Rx = dx1 * csi + x0 - tx1
        else:
            Rz = z1-tz1
            Rx = x1-tx1
        R.append([Rz,Rx])
    return R

def createPathOffset(path, offsetModule, offsetDirection):
    """
        Creates a new path with offset offsetModule with respect to path.
        offsetDirection = vector toward the offset (does not need to be normalized)
    """
    pathNew = []
    norm = math.sqrt(offsetDirection[0]*offsetDirection[0]+offsetDirection[1]*offsetDirection[1])
    offsetX = offsetModule * offsetDirection[1] / norm
    offsetZ = offsetModule * offsetDirection[0] / norm 
    for p in path:
        pathNew.append([p[0]+offsetZ,p[1]+offsetX])
    return pathNew

def interpolZ(r, path):
    """
        Interpolates z(r) along the path
    """
    N = len(path)
    for k in range(1,N):
        z0,r0 = path[k-1]
        z1,r1 = path[k]
        if r1 < r0:
            z0,r0 = path[k]
            z1,r1 = path[k-1]
        if r0 <= r and r <= r1:
            if math.fabs(r1-r0) < 1E-7:
                return z0
            else:
                return (z1-z0)/(r1-r0)*(r-r0)+z0
    return None

def slicePath(zi, rsafe, directionR, stepR, path, feedrateR, feedrateZ):
    """
        Slices the path from an initial z (zi) coordinate

        zi        = initial z
        rsafe     = r for safe motion
        diretionR = -1.0 (external to internal), 1.0 (internal to external)
        stepR     = slice hight
        path      = points of the path
        feedrateR = feedrate for r direction
        feedrateZ = feedrate for z direction
    """
    ri = path[0][1] 
    rf = path[-1][1]

    if directionR < 0.0:
        if ri < rf:
            tmp = rf
            rf = ri
            ri = tmp
                
        stepR = -math.fabs(stepR)
        def stopCondition(r,rf):
            return r < rf
    else:
        if ri > rf:
            tmp = rf
            rf = ri
            ri = tmp
        stepR = math.fabs(stepR)
        def stopCondition(r,rf):
            return r > rf
    gcode = []
    gcode.append(G0+x(rsafe))
    gcode.append(G0+z(zi))
    r = ri
    while True:
        zf = interpolZ(r,path)
        if zf is None:
            return ["; fail to interpolate path"]
        gcode.append(G1+x(r)+f(feedrateR))
        gcode.append(G1+z(zf)+f(feedrateZ))
        gcode.append(G0+x(r-stepR))
        gcode.append(G0+z(zi))
        r = r + stepR
        if stopCondition(r,rf):
            break
    return gcode

def isTurnExternalProfileRightToLeftFeasible(zi, rsafe, rc, path):
    """
        The operation is feasible if the list of error is empty
    """
    listOfErrors = []

    if len(path) < 2:
        listOfErrors.append("Sao necessarios, pelo menos, dois pontos para definir o contorno")

    if not isRadiusMonotonicallyDecreasing(path):
        listOfErrors.append("X deve decrescer monotonicamente")

    zf = path[-1][0]
    if ( zf >= zi ):
        listOfErrors.append("Z do fim do contorno deve ser menor que Z do inicio da usinagem")
    rmax = path[ 0][1]

    if rsafe < rmax:
        listOfErrors.append("X seguro deve ser maior que o maior X do contorno")

    dpath = getDisplacements(path)
    for dp in dpath:
        ds = math.sqrt(dp[0]*dp[0]+dp[1]*dp[1])
        if ds < rc:
            listOfErrors.append("Os segmentos do contorno devem ser maiores que o raio da ferramenta")
    return listOfErrors


def isTurnExternalProfileLeftToRightFeasible(zi, rsafe, rc, path):
    """
        The operation is feasible if the list of error is empty
    """
    listOfErrors = []

    if len(path) < 2:
        listOfErrors.append("Sao necessarios, pelo menos, dois pontos para definir o contorno")

    if not isRadiusMonotonicallyIncreasing(path):
        listOfErrors.append("X deve crescer monotonicamente")

    zb = path[0][0]
    if ( zb <= zi ):
        listOfErrors.append("Z do inicio do contorno deve ser maior que Z do inicio da usinagem")
    
    rmax = path[-1][1]
    if rsafe < rmax:
        listOfErrors.append("X seguro deve ser maior que o maior X do contorno")

    dpath = getDisplacements(path)
    for dp in dpath:
        ds = math.sqrt(dp[0]*dp[0]+dp[1]*dp[1])
        if ds < rc:
            listOfErrors.append("Os segmentos do contorno devem ser maiores que o raio da ferramenta")

    return listOfErrors

def isTurnInternalProfileRightToLeftFeasible(zi, rsafe, rc, path):
    """
        The operation is feasible if the list of error is empty
    """
    listOfErrors = []

    if len(path) < 2:
        listOfErrors.append("Sao necessarios, pelo menos, dois pontos para definir o contorno")

    if not isRadiusMonotonicallyIncreasing(path):
        listOfErrors.append("X deve crescer monotonicamente")

    zf = path[-1][0]
    if ( zf >= zi ):
        listOfErrors.append("Z do fim do contorno deve ser menor que Z do inicio da usinagem")
    rmin = path[ 0][1]

    if rsafe >= rmin:
        listOfErrors.append("X seguro deve ser menor que o menor X do contorno")
    
        dpath = getDisplacements(path)

    for dp in dpath:
        ds = math.sqrt(dp[0]*dp[0]+dp[1]*dp[1])
        if ds < rc:
            listOfErrors.append("Os segmentos do contorno devem ser maiores que o raio da ferramenta")

    return listOfErrors

def turnExternalProfileRightToLeft(zi, rsafe, rc, bci, bcf, path, dsfinishing, Nfinishing, stepR, feedrateR, feedrateZ, feedrateFinishing):
    """
        zi = initial z (right)
        rsafe = safe radius
        rc = radius of the tool tip
        bci = initial boundary condition. 0 = line continuation along z; 1 = line continuation along r
        bcf = final boundary condition. 0 = line continuation along z; 1 = line continuation along r
        path = vector (z_k, r_k) (uses radius mode)
        dsfinishing = finishing offset
        Nfinishing = number of finishing passes
        stepR = step size toward the radial direction
        feedrateR = feedrate in the radial direction
        feedrateZ = feedrate in the longitudinal direction
        feedrateFinishing = feedrate for finishing
    """
    
    gcode = []

    # Checking feasibility
    listOfErrors = isTurnExternalProfileRightToLeftFeasible(zi, rsafe, rc, path)

    if len(listOfErrors) > 0:
        for err in listOfErrors:
            gcode.append(";"+str(err)+"\n")
        return gcode  

    # Creating the tool with tip radius rc
    tool = LatheToolCircularRightExternal(rc)

    # Adding the initial boundary condition
    p1 = copy.deepcopy(path[0])
    if  bci == 0 : 
        p1[0] = p1[0]-rc
    else:
        p1[1] = p1[1]+rc
    path.insert(0,p1)

    # Adding the final boundary condition
    p2 = copy.deepcopy(path[-1])
    if  bcf == 0 : 
        p2[0] = p2[0]+rc
    else:
        p2[1] = p2[1]-rc
    path.append(p2)

    # Setting mode to radius
    gcode.append("G8")

    # Moving to safe position
    gcode.append(G0 + x(rsafe))
    gcode.append(G0 + z(zi))

    # Adding the coarsest offset
    pathCoarse = getToolPath(createPathOffset(path, float(Nfinishing)*dsfinishing, [1.0,1.0]),tool)

    # Slicing the coarsest path
    directionR = -1.0 # Out to in
    gcode = gcode + slicePath(zi, rsafe, directionR, stepR, pathCoarse, feedrateR, feedrateZ)

    for i in reversed(range(0,Nfinishing+1)):
        
        pathFinishing = getToolPath(createPathOffset(path, float(i)*dsfinishing, [1.0,1.0]),tool)
        initialR = pathFinishing[0][1]+stepR
        finalR   = pathFinishing[-1][1]
        if initialR > rsafe:
            initialR = rsafe
        gcode.append(G0 + x(initialR))
        gcode.append(G0 + z(zi))
        gcode.append(G0 + x(finalR))
        for p in reversed(pathFinishing):
            gcode.append(G1+x(p[1])+z(p[0])+f(feedrateFinishing))

    gcode.append(G0 + x(rsafe))
    gcode.append(G0 + z(zi))
    return gcode


def turnExternalProfileLeftToRight(zi, rsafe, rc, bci, bcf, path, dsfinishing, Nfinishing, stepR, feedrateR, feedrateZ, feedrateFinishing):
    """
        zi = initial z (right)
        rsafe = safe radius
        rc = radius of the tool tip
        bci = initial boundary condition. 0 = line continuation along z; 1 = line continuation along r
        bcf = final boundary condition. 0 = line continuation along z; 1 = line continuation along r
        path = vector (z_k, r_k) (uses radius mode)
        dsfinishing = finishing offset
        Nfinishing = number of finishing passes
        stepR = step size toward the radial direction
        feedrateR = feedrate in the radial direction
        feedrateZ = feedrate in the longitudinal direction
        feedrateFinishing = feedrate for finishing
    """
    
    gcode = []

    # Checking feasibility
    listOfErrors = isTurnExternalProfileLeftToRightFeasible(zi, rsafe, rc, path)

    if len(listOfErrors) > 0:
        for err in listOfErrors:
            gcode.append(";"+str(err)+"\n")
        return gcode  

    # Creating the tool with tip radius rc
    tool = LatheToolCircularLeftExternal(rc)

    # Adding the initial boundary condition
    p1 = copy.deepcopy(path[0])
    if  bci == 0 : 
        p1[0] = p1[0]-rc
    else:
        p1[1] = p1[1]-rc
    path.insert(0,p1)

    # Adding the final boundary condition
    p2 = copy.deepcopy(path[-1])
    if  bcf == 0 : 
        p2[0] = p2[0]+rc
    else:
        p2[1] = p2[1]+rc
    path.append(p2)

    # Setting mode to radius
    gcode.append("G8")

    # Moving to safe position
    gcode.append(G0 + x(rsafe))
    gcode.append(G0 + z(zi))

    # Adding the coarsest offset
    pathCoarse = getToolPath(createPathOffset(path, float(Nfinishing)*dsfinishing, [-1.0,1.0]),tool)

    # Slicing the coarsest path
    directionR = -1.0 # Out to in
    gcode = gcode + slicePath(zi, rsafe, directionR, stepR, pathCoarse, feedrateR, feedrateZ)

    for i in reversed(range(0,Nfinishing+1)):
        
        pathFinishing = getToolPath(createPathOffset(path, float(i)*dsfinishing, [-1.0,1.0]),tool)
        
        initialR = pathFinishing[-1][1]+stepR
        finalR   = pathFinishing[0][1]
        if initialR > rsafe:
            initialR = rsafe
        gcode.append(G0 + x(initialR))
        gcode.append(G0 + z(zi))
        gcode.append(G0 + x(finalR))
        for p in pathFinishing:
            gcode.append(G1+x(p[1])+z(p[0])+f(feedrateFinishing))

    gcode.append(G0 + x(rsafe))
    gcode.append(G0 + z(zi))
    return gcode


def turnInternalProfileRightToLeft(zi, rsafe, rc, bci, bcf, path, dsfinishing, Nfinishing, stepR, feedrateR, feedrateZ, feedrateFinishing):
    """
        zi = initial z (right)
        rsafe = safe radius
        rc = radius of the tool tip
        bci = initial boundary condition. 0 = line continuation along z; 1 = line continuation along r
        bcf = final boundary condition. 0 = line continuation along z; 1 = line continuation along r
        path = vector (z_k, r_k) (uses radius mode)
        dsfinishing = finishing offset
        Nfinishing = number of finishing passes
        stepR = step size toward the radial direction
        feedrateR = feedrate in the radial direction
        feedrateZ = feedrate in the longitudinal direction
        feedrateFinishing = feedrate for finishing
    """
    
    gcode = []

    # Checking feasibility
    listOfErrors = isTurnInternalProfileRightToLeftFeasible(zi, rsafe, rc, path)

    if len(listOfErrors) > 0:
        for err in listOfErrors:
            gcode.append(";"+str(err)+"\n")
        return gcode  

    # Creating the tool with tip radius rc
    tool = LatheToolCircularLeftInternal(rc)

    # Adding the initial boundary condition
    p1 = copy.deepcopy(path[0])
    if  bci == 0 : 
        p1[0] = p1[0]-rc
    else:
        p1[1] = p1[1]-rc
    path.insert(0,p1)

    # Adding the final boundary condition
    p2 = copy.deepcopy(path[-1])
    if  bcf == 0 : 
        p2[0] = p2[0]+rc
    else:
        p2[1] = p2[1]+rc
    path.append(p2)

    # Setting mode to radius
    gcode.append("G8")

    # Moving to safe position
    gcode.append(G0 + x(rsafe))
    gcode.append(G0 + z(zi))

    # Adding the coarsest offset
    pathCoarse = getToolPath(createPathOffset(path, float(Nfinishing)*dsfinishing, [1.0,-1.0]),tool)

    # Slicing the coarsest path
    directionR = 1.0 # In to out
    gcode = gcode + slicePath(zi, rsafe, directionR, stepR, pathCoarse, feedrateR, feedrateZ)

    for i in reversed(range(0,Nfinishing+1)):
        
        pathFinishing = getToolPath(createPathOffset(path, float(i)*dsfinishing, [1.0,-1.0]),tool)
        initialR = pathFinishing[0][1]-stepR
        finalR   = pathFinishing[-1][1]
        if initialR < rsafe:
            initialR = rsafe
        gcode.append(G0 + x(initialR))
        gcode.append(G0 + z(zi))
        gcode.append(G0 + x(finalR))
        for p in reversed(pathFinishing):
            gcode.append(G1+x(p[1])+z(p[0])+f(feedrateFinishing))

    gcode.append(G0 + x(rsafe))
    gcode.append(G0 + z(zi))
    return gcode


if __name__ == "__main__":

    gc = ["G21","G8","G94","F60","M3 S1000","G18","G40","G49","G64 P0.0010","G90"]

    # External (right)
    #path = [[0,10],[10,10],[10,0]]
    #path = [[-10,10],[0,0]]
    #path = [[-5,15],[0,15],[0,10],[10,10],[15,5],[15,0]]
    
    # Internal 
    path = [[0,10],[10,20],[10,25]]

    zi=11.0
    rsafe=6.0
    rc = 1.0
    bci = 0
    bcf = 1
    dsfinishing = 0.1
    Nfinishing = 1
    stepR = 2.0
    feedrateR = 300.0
    feedrateZ = 300.0
    feedrateFinishing = 200.0

    #gc = gc +turnExternalProfileRightToLeft(zi, rsafe, rc, bci, bcf, path, dsfinishing, Nfinishing, stepR, feedrateR, feedrateZ, feedrateFinishing)
    gc = gc +turnInternalProfileRightToLeft(zi, rsafe, rc, bci, bcf, path, dsfinishing, Nfinishing, stepR, feedrateR, feedrateZ, feedrateFinishing)
    #gc = gc +turnExternalProfileLeftToRight(zi, rsafe, rc, bci, bcf, path, dsfinishing, Nfinishing, stepR, feedrateR, feedrateZ, feedrateFinishing)

    gc.append("M5")
    gc.append("M2")

    for c in gc:
        print(c)
