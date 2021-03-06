import numpy as np
import copy
import time
from mpm_imports import *

#===============================================================================
def init():
    #  Initialize Simulation
    # Result File Name
    fName = 'ex_one'
    fDir  = 'ex_one_data'
    
    # Domain Constants
    x0 = np.array([0.0,0.0])                 #  Bottom left Corner
    x1 = np.array([1.0,1.0])                 #  Top right corner
    nN = np.array([20,20])                   #  Number of cells in each direction
    dx = (x1-x0)/nN
    nG = 2                                   #  Number of ghost nodes
    thick = 0.1                              #  Domain thickness
    ppe = 2                                  #  Particles per element 

    # Material Properties
    mProps1 = {'modulus':1.0e7, 'poisson':0.3, 'density':1.0e3 }
    vw = np.sqrt( mProps1['modulus']/mProps1['density'] )   #  Wave speed
    modelName = 'planeStrainNeoHookean'
    mat1 = Material( matid=1, props=mProps1, model=modelName, exload=0)
    mats = [mat1]
    
    
    # Time Constants
    t0 = 0.0
    CFL = 0.2
    dt = min(dx) * CFL / vw
    tf = 10
    
    # Create Data Warehouse
    dw = Dw( t=0.0, idx=0, ddir=fDir )
    
    # Create Patch
    pch = Patch( x0, x1, nN, nG, t0, tf, dt, thick, dw )
    
    # Create shape function
    sh = Shape()

    # Create boundary conditions
    pch.bcs = []                           #  BC list
    
    # Create Circles
    pt1 = np.array([0.25,0.5])
    r = np.array([0.0,0.1])
    matid1 = 1
    matid2 = 2
    geomutils.fillAnnulus( pt1,r[0],r[1],ppe,pch,dw,matid1,mProps1['density'] )
    v0 = np.array([0.1, 0.0])
    
    mpm.updateMats( dw, pch, mats, sh )
    mat1.setVelocity( dw, v0 )
    
    return (dw, pch, mats, sh, fName )


#===============================================================================
def stepTime( dw, patch, mats, shape, saveName ):
    # Advance through time
    while( (patch.t < patch.tf) and patch.allInPatch(dw.px) ):
        t_out = 0.01        
        mpm.timeAdvance( dw, patch, mats, shape )
        dw.saveDataAndAdvance( patch.dt, t_out, saveName )

#===============================================================================            
def run():
    dw, pch, mats, sh, fname = init()
    stepTime( dw, pch, mats, sh, fname )
    return dw