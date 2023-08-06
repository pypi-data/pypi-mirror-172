"""
Module qepy_mod


Defined at qepy_mod.fpp lines 5-402

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging

_arrays = {}
_objs = {}

def qepy_get_rho(rhor, gather=None):
    """
    qepy_get_rho(rhor[, gather])
    
    
    Defined at qepy_mod.fpp lines 78-106
    
    Parameters
    ----------
    rhor : float array
    gather : bool
    
    """
    _qepy.f90wrap_qepy_get_rho(rhor=rhor, gather=gather)

def qepy_set_rho(rhor, gather=None):
    """
    qepy_set_rho(rhor[, gather])
    
    
    Defined at qepy_mod.fpp lines 108-139
    
    Parameters
    ----------
    rhor : float array
    gather : bool
    
    """
    _qepy.f90wrap_qepy_set_rho(rhor=rhor, gather=gather)

def qepy_get_rho_core(rhoc, gather=None):
    """
    qepy_get_rho_core(rhoc[, gather])
    
    
    Defined at qepy_mod.fpp lines 141-160
    
    Parameters
    ----------
    rhoc : float array
    gather : bool
    
    """
    _qepy.f90wrap_qepy_get_rho_core(rhoc=rhoc, gather=gather)

def qepy_set_rho_core(rhoc, gather=None):
    """
    qepy_set_rho_core(rhoc[, gather])
    
    
    Defined at qepy_mod.fpp lines 162-182
    
    Parameters
    ----------
    rhoc : float array
    gather : bool
    
    """
    _qepy.f90wrap_qepy_set_rho_core(rhoc=rhoc, gather=gather)

def qepy_set_extpot(self, vin, gather=None):
    """
    qepy_set_extpot(self, vin[, gather])
    
    
    Defined at qepy_mod.fpp lines 184-221
    
    Parameters
    ----------
    embed : Embed_Base
    vin : float array
    gather : bool
    
    """
    _qepy.f90wrap_qepy_set_extpot(embed=self._handle, vin=vin, gather=gather)

def qepy_get_grid(nr=None, gather=None):
    """
    nrw = qepy_get_grid([nr, gather])
    
    
    Defined at qepy_mod.fpp lines 223-240
    
    Parameters
    ----------
    nr : int array
    gather : bool
    
    Returns
    -------
    nrw : int array
    
    """
    nrw = _qepy.f90wrap_qepy_get_grid(nr=nr, gather=gather)
    return nrw

def qepy_get_grid_smooth(nr=None, gather=None):
    """
    nrw = qepy_get_grid_smooth([nr, gather])
    
    
    Defined at qepy_mod.fpp lines 265-282
    
    Parameters
    ----------
    nr : int array
    gather : bool
    
    Returns
    -------
    nrw : int array
    
    """
    nrw = _qepy.f90wrap_qepy_get_grid_smooth(nr=nr, gather=gather)
    return nrw

def qepy_set_stdout(fname=None, uni=None, append=None):
    """
    qepy_set_stdout([fname, uni, append])
    
    
    Defined at qepy_mod.fpp lines 284-309
    
    Parameters
    ----------
    fname : str
    uni : int
    append : bool
    
    """
    _qepy.f90wrap_qepy_set_stdout(fname=fname, uni=uni, append=append)

def qepy_write_stdout(fstr):
    """
    qepy_write_stdout(fstr)
    
    
    Defined at qepy_mod.fpp lines 311-317
    
    Parameters
    ----------
    fstr : str
    
    """
    _qepy.f90wrap_qepy_write_stdout(fstr=fstr)

def qepy_close_stdout(fname):
    """
    qepy_close_stdout(fname)
    
    
    Defined at qepy_mod.fpp lines 319-325
    
    Parameters
    ----------
    fname : str
    
    """
    _qepy.f90wrap_qepy_close_stdout(fname=fname)

def qepy_get_evc(ik, wfc=None):
    """
    qepy_get_evc(ik[, wfc])
    
    
    Defined at qepy_mod.fpp lines 327-341
    
    Parameters
    ----------
    ik : int
    wfc : complex array
    
    """
    _qepy.f90wrap_qepy_get_evc(ik=ik, wfc=wfc)

def qepy_get_wf(ik, ibnd, wf, gather=None):
    """
    qepy_get_wf(ik, ibnd, wf[, gather])
    
    
    Defined at qepy_mod.fpp lines 343-390
    
    Parameters
    ----------
    ik : int
    ibnd : int
    wf : complex array
    gather : bool
    
    """
    _qepy.f90wrap_qepy_get_wf(ik=ik, ibnd=ibnd, wf=wf, gather=gather)

def qepy_set_extforces(self, forces):
    """
    qepy_set_extforces(self, forces)
    
    
    Defined at qepy_mod.fpp lines 392-402
    
    Parameters
    ----------
    embed : Embed_Base
    forces : float array
    
    """
    _qepy.f90wrap_qepy_set_extforces(embed=self._handle, forces=forces)

def _mp_gather_real(fin, fout):
    """
    _mp_gather_real(fin, fout)
    
    
    Defined at qepy_mod.fpp lines 22-34
    
    Parameters
    ----------
    fin : float array
    fout : float array
    
    """
    _qepy.f90wrap_mp_gather_real(fin=fin, fout=fout)

def _mp_gather_complex(fin, fout):
    """
    _mp_gather_complex(fin, fout)
    
    
    Defined at qepy_mod.fpp lines 50-62
    
    Parameters
    ----------
    fin : complex array
    fout : complex array
    
    """
    _qepy.f90wrap_mp_gather_complex(fin=fin, fout=fout)

def mp_gather(*args, **kwargs):
    """
    mp_gather(*args, **kwargs)
    
    
    Defined at qepy_mod.fpp lines 13-14
    
    Overloaded interface containing the following procedures:
      _mp_gather_real
      _mp_gather_complex
    
    """
    for proc in [_mp_gather_real, _mp_gather_complex]:
        try:
            return proc(*args, **kwargs)
        except TypeError:
            continue

def _mp_scatter_real(fin, fout):
    """
    _mp_scatter_real(fin, fout)
    
    
    Defined at qepy_mod.fpp lines 36-48
    
    Parameters
    ----------
    fin : float array
    fout : float array
    
    """
    _qepy.f90wrap_mp_scatter_real(fin=fin, fout=fout)

def _mp_scatter_complex(fin, fout):
    """
    _mp_scatter_complex(fin, fout)
    
    
    Defined at qepy_mod.fpp lines 64-76
    
    Parameters
    ----------
    fin : complex array
    fout : complex array
    
    """
    _qepy.f90wrap_mp_scatter_complex(fin=fin, fout=fout)

def mp_scatter(*args, **kwargs):
    """
    mp_scatter(*args, **kwargs)
    
    
    Defined at qepy_mod.fpp lines 17-18
    
    Overloaded interface containing the following procedures:
      _mp_scatter_real
      _mp_scatter_complex
    
    """
    for proc in [_mp_scatter_real, _mp_scatter_complex]:
        try:
            return proc(*args, **kwargs)
        except TypeError:
            continue


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "qepy_mod".')

for func in _dt_array_initialisers:
    func()
