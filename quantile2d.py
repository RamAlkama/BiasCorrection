# -*- coding: latin-1 -*-

"""
Quantile-Matching Bias Correction Approach
last update: 17/03/2017
contact: ram.alkama@hotmail.fr

example of use:

python quantile2d.py -obs obs_1980_2010.nc -vobs tmp -hist sim_1980_2010.nc -vhist tas -fut sim_2070_2100.nc -vfut tas -o corrected_2070_2100.nc

"""

import numpy as N,sys,cdms2 as cdms, MV2 as MV
from scipy import stats

# ----------------
#  classical approach
# ----------------

def Quantile_Matching_classical(v_observed,v_historical,v_future):
  v_corrected=N.zeros(v_future.shape)
  for ii in range(len(v_future)):
    percentile=stats.percentileofscore(v_historical, v_future[ii])
    v_corrected[ii]=N.percentile(v_observed,percentile)
  return v_corrected

# ----------------
#  delta approach
# ----------------

def Quantile_Matching_delta(v_observed,v_historical,v_future):
  v_corrected=N.zeros(v_future.shape)
  for ii in range(len(v_future)):
    percentile=stats.percentileofscore(v_future, v_future[ii])
    v_corrected[ii]=v_future[ii]+N.percentile(v_observed,percentile)-N.percentile(v_historical,percentile)
  return v_corrected

# ----------------------
#  read NetCDF file
# ----------------------

def readf(ficin,varin):
  g = cdms.open(ficin)
  tab = g(varin,squeeze=1)
  g.close()  
  return tab

# ----------------------
#  main
# ----------------------
if __name__ ==  '__main__' :
  if len(sys.argv) == 1 :
     sys.exit("""
  Syntax 
    quantile2d.py [options]
        -obs   file of observations
    	-vobs  variable id (from the observed file)
        -hist  reference file (historical simulation)
        -vhist variable id (from historical simulation)
        -fut   reference file (future simulation)
        -vfut  variable id (from future simulation)

        optional parameters: 
        -o     name of the output file, 
               by default "biais_corrected.nc"
        -nc 4  to produce compressed NetCDF file
	    by default classic NetCDF file is produced""")
  else  :
    type = sys.argv[1::2]
    value = sys.argv[2::2]
    nc = 3
    ficout = 'biais_corrected.nc'
    for typ, val in zip(type, value) :
       if typ == "-obs"    : ficobs  = val
       if typ == "-vobs"   : varobs  = val
       if typ == "-hist"   : fichist = val
       if typ == "-vhist"  : varhist = val
       if typ == "-fut"    : ficfut  = val
       if typ == "-vfut"   : varfut  = val        
       if typ == "-o"      : ficout  = val
       if typ == "-nc"     : nc = int(val)
    try : ficobs
    except : sys.exit("""
 You must specify an observed input file by: -obs ObservedFileName
 """)
    try : varobs
    except : sys.exit("""
 You must specify the variable ID to read from the observed file by: -vobs ObservedVariableID
 """)    
    try : fichist
    except : sys.exit("""
 You must specify an historical input file by: -hist HistoricalFileName
 """)
    try : varhist
    except : sys.exit("""
 You must specify the variable ID to read from the Historical file by: -vhist HistoricalVariableID
 """)      
    try : ficfut
    except : sys.exit("""
 You must specify an future input file by: -fut FutureFileName
 """)
    try : varfut
    except : sys.exit("""
 You must specify the variable ID to read from the observed file by: -vfut FutureVariableID
 """)      

    if (ficout == fichist) or (ficout == ficobs) or (ficout == ficfut): ficout = ficfut[:-3]+"_new.nc"

  if nc != 4 :
    cdms.setNetcdfShuffleFlag(0)
    cdms.setNetcdfDeflateFlag(0)
    cdms.setNetcdfDeflateLevelFlag(0)

# -- extraction de donnees
# --------------------------

  obs = readf(ficobs,varobs)
  his = readf(fichist,varhist)
  fut = readf(ficfut,varfut)

# -- Declaration des variables
# ------------------------- 

  out_classic = N.ones(fut.shape, dtype='f')+1.e20
  out_delta   = N.ones(fut.shape, dtype='f')+1.e20

# -- Boucle sur la grille 
# ------------------------- 

  for ii in range(fut.shape[2]):
    print (ii)
    for jj in range(fut.shape[1]):
      if not (obs.mask[0,jj,ii] or his.mask[0,jj,ii] or fut.mask[0,jj,ii]) :    
        # classical approach
        out= Quantile_Matching_classical(obs[:,jj,ii],his[:,jj,ii],fut[:,jj,ii])
        out_classic[:,jj,ii]= out[:]
        # delta approach
        out = Quantile_Matching_delta(obs[:,jj,ii],his[:,jj,ii],fut[:,jj,ii])
        out_delta[:,jj,ii]  = out[:]

# -- Sauvegarde
# ------------------------- 

  out_delta = MV.masked_greater(out_delta,1e+18)
  out_delta = cdms.createVariable(out_delta,axes=fut.getAxisList(),id=fut.id+'_delta')
  out_delta.units = fut.units
  out_delta.long_name = 'Bias Corrected with delta approach'

  out_classic = MV.masked_greater(out_classic,1e+18)
  out_classic = cdms.createVariable(out_classic,axes=fut.getAxisList(),id=fut.id+'_classic')
  out_classic.units = fut.units
  out_classic.long_name = 'Bias Corrected with classic approach'

  o = cdms.open(ficout,'w')
  o.write(out_delta)
  o.write(out_classic)
  o.close()


