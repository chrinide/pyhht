import numpy as np
from math import pi
from matplotlib.mlab import find

################################################################################
def emd(**kwargs):
    
    # Typical usecase for a HasTraits subclass
    MAXMODES     = kwargs.pop("MAXMODES",None)
    k            = kwargs.pop("k",None)
    mask         = kwargs.pop("mask",None)
    r            = kwargs.pop("r",None)
    FIXE         = kwargs.pop("FIXE",None)
    t            = kwargs.pop("t",None)
    INTERP       = kwargs.pop("INTERP",None)
    MODE_COMPLEX = kwargs.pop("MODE_COMPLEX",None)
    ndirs        = kwargs.pop("ndirs",None)
    FIXE_H       = kwargs.pop("FIXE_H",None)
    sd           = kwargs.pop("sd",None)
    sd2          = kwargs.pop("sd2",None)
    tol          = kwargs.pop("tol",None)
    
    A = stop_emd(r,MODE_COMPLEX=False)
    B = (k<MAXMODES+1 or MAXMODES==0)
    C = not np.any(mask)
    
    while not A and B and C:
        
        m = r
        mp = m.copy()
        
        if FIXE:
            stop_sift, moyenne = stop_sifting_fixe(t,m,INTERP,MODE_COMPLEX,ndirs)
        elif FIXE_H:
            stop_count = 0
            stop_sift, moyenne = stop_sifting_fixe_h(t,m,INTERP,stop_count,
                                                   FIXE_H,MODE_COMPLEX, ndirs)
        else:
            stop_sift, moyenne = stop_sifting(m,t,sd,sd2,tol,INTERP,MODE_COMPLEX,
                                              ndirs)
        

################################################################################
def stop_emd(r, MODE_COMPLEX, ndirs=4):
    
    """ Tests if there are enough extrema (3) to continue sifting. """
    
    if MODE_COMPLEX:
        ner = []
        for k in range(ndirs):
            phi = k*pi/ndirs
            indmin, indmax = extr(np.real(np.exp(1j*phi)*r))[:2]
            ner.append(len(indmin)+len(indmax))
        stop = np.any(ner<3)
    else:
        indmin, indmax = extr(r)[:2]
        ner = len(indmin) + len(indmax)
        stop = ner < 3
    return stop

################################################################################
def extr(x,t=None):
    
    """ Extracts the indices of the extrema and zero crossings. """
    
    m = len(x)
    if not t:
        t = np.arange(m)
    
    
    x1 = x[:m-1]
    x2 = x[1:m]
    indzer = find(x1*x2<0)
    if np.any(x==0):
        iz = find(x==0)
        indz = [];
        if np.any(np.diff(iz)==1):
            zer = x == 0
            dz = np.diff([0,zer,0])
            debz = find(dz == 1)
            finz = find(dz == -1)-1
            indz = np.round((debz+finz)/2)
        else:
            indz = iz
        indzer = np.sort([indzer,indz])

    d = np.diff(x)
    n = len(d)
    d1 = d[:n-1]
    d2 = d[1:n]
    indmin = set(find(d1*d2<0)).intersection(find(d1<0))
    indmin = np.array(list(indmin)) + 1
    indmax = set(find(d1*d2<0)).intersection(find(d1>0))
    indmax = np.array(list(indmax)) + 1
    
    if any(d==0):
        imax = []
        imin = []
        bad = (d==0)
        dd = np.diff([0,bad,0])
        debs = find(dd == 1)
        fins = find(dd == -1)
        if debs[0] == 1:
            if len(debs) > 1:
                debs = debs[2:]
                fins = fins[2:]
            else:
                debs = []
                fins = []
        if len(debs) > 0:
            if fins(len(fins)-1) == m:
                if len(debs)>1:
                    debs = debs[:len(debs)-1]
                    fins = fins[:len(fins)-1]
                else:
                    debs = []
                    fins = []
        lc = len(debs)
        if lc > 0:
            for k in range(lc):
                if d[debs[k]-1]>0:
                    if d[fins[k]] < 0:
                        imax = [imax,np.round((fins[k]+debs[k])/2)]
                else:
                    if d[fins[k]]>- 0 :
                        imin = [imin, np.round((fins[k]+debs[k])/2)]
        
        if len(imax)>0:
            indmax = np.sort([indmax,imax])
        if len(imin)>0:
            indmin = np.sort([indmin, imin])
    
    return indmin, indmax, indzer


################################################################################
def stop_sifting_fixe(t,m,INTERP,MODE_COMPLEX,ndirs=4):
    moyenne = mean_and_amplitude(m,t,INTERP,MODE_COMPLEX,ndirs)
    stop = 0
    return stop, moyenne

################################################################################
def mean_and_amplitude(m,t,INTERP,MODE_COMPLEX,ndirs=4):
    NBSYM = 2
    if MODE_COMPLEX:
        if MODE_COMPLEX == 1:
            for k in range(ndirs):
                phi = k*pi.ndirs
                y = np.real(np.exp(-1j*phi)*m)
                indmin, indmax, indzer = extr(y)
                






################################################################################
def stop_sifting_fixe_h():
    pass


################################################################################
def stop_sifting():
    pass
################################################################################
def main():
    pass