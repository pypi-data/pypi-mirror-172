#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
QSDsan: Quantitative Sustainable Design for sanitation and resource recovery systems

This module is developed by:
    Yalin Li <mailto.yalin.li@gmail.com>

This module is under the University of Illinois/NCSA Open Source License.
Please refer to https://github.com/QSD-Group/QSDsan/blob/main/LICENSE.txt
for license details.
'''


# %%

from warnings import warn
from math import ceil
from .. import SanUnit, Construction
from ..processes import Decay
from ..utils import ospath, load_data, data_path

__all__ = ('Lagoon',)

anaerobic_path = ospath.join(data_path, 'sanunit_data/_anaerobic_lagoon.tsv')
facultative_path = ospath.join(data_path, 'sanunit_data/_facultative_lagoon.tsv')

class Lagoon(SanUnit, Decay):
    '''
    Anaerobic and facultative lagoon treatment based on
    `Trimmer et al. <https://doi.org/10.1021/acs.est.0c03296>`_

    To enable life cycle assessment, the following impact items should be pre-constructed:
    `Plastic`, `Excavation`.

    Parameters
    ----------
    ins : WasteStream
        Waste for treatment.
    outs : WasteStream
        Treated waste, fugitive CH4, and fugitive N2O.
    design_type : str
        Can be "anaerobic" or "facultative".
    flow_rate : float
        Total flow rate through the lagoon (to calculate retention time), [m3/d].
        If not provided, will use F_vol_in.
    degraded_components : tuple
        IDs of components that will degrade (at the same removal as `COD_removal`).
    if_N2O_emission : bool
        If consider N2O emission from N degradation in the process.

    Examples
    --------
    `bwaise systems <https://github.com/QSD-Group/EXPOsan/blob/main/exposan/bwaise/systems.py>`_

    References
    ----------
    [1] Trimmer et al., Navigating Multidimensional Social–Ecological System
    Trade-Offs across Sanitation Alternatives in an Urban Informal Settlement.
    Environ. Sci. Technol. 2020, 54 (19), 12641–12653.
    https://doi.org/10.1021/acs.est.0c03296.

    See Also
    --------
    :ref:`qsdsan.processes.Decay <processes_Decay>`
    '''

    def __init__(self, ID='', ins=None, outs=(), thermo=None, init_with='WasteStream',
                 design_type='anaerobic', flow_rate=None, degraded_components=('OtherSS',),
                 if_N2O_emission=False, **kwargs):

        SanUnit.__init__(self, ID, ins, outs, thermo, init_with)
        self._tau = None
        self._P_removal = 0.
        self._anaerobic_defaults = load_data(path=anaerobic_path)
        self._facultative_defaults = load_data(path=facultative_path)
        self._design_type = None
        self.design_type = design_type
        self._flow_rate = flow_rate
        self.degraded_components = tuple(degraded_components)
        self.if_N2O_emission = if_N2O_emission

        self.construction = (
            Construction('liner', linked_unit=self, item='Plastic', quantity_unit='kg'),
            Construction('excavation', linked_unit=self, item='Excavation', quantity_unit='m3'),
            )

        for attr, value in kwargs.items():
            setattr(self, attr, value)

    _N_ins = 1
    _N_outs = 3

    def _run(self):
        waste = self.ins[0]
        treated, CH4, N2O = self.outs
        CH4.phase = N2O.phase = 'g'

        treated.copy_like(waste)
        removed_frac = self.COD_removal*self.COD_decay
        treated.imass[self.degraded_components] *= 1 - self.COD_removal

        _COD = waste._COD or waste.COD
        CH4.imass['CH4'] = removed_frac*_COD*waste.F_vol/1e3 * \
            self.MCF_decay*self.max_CH4_emission

        if self.if_N2O_emission:
            N_loss = self.first_order_decay(k=self.decay_k_N,
                                            t=self.tau/365,
                                            max_decay=self.N_max_decay)
            N_loss_tot = N_loss*waste.TN/1e3*waste.F_vol
            NH3_rmd, NonNH3_rmd = \
                self.allocate_N_removal(N_loss_tot, waste.imass['NH3'])
            treated.imass ['NH3'] -=  NH3_rmd
            treated.imass['NonNH3'] -= NonNH3_rmd
            N2O.imass['N2O'] = N_loss_tot*self.N2O_EF_decay*44/28
        else:
            N2O.empty()

        treated.imass['P'] *= 1 - self.P_removal
        treated._COD = _COD*waste.F_vol*(1-self.COD_removal)/treated.F_vol

    _units = {
        'Single lagoon volume': 'm3',
        'Lagoon length': 'm',
        'Lagoon width': 'm',
        'Lagoon depth': 'm'
        }

    def _design(self):
        design = self.design_results
        design['Lagoon number'] = N = self.N_lagoon
        design['Single lagoon volume'] = V = self.lagoon_V
        design['Lagoon length'] = L = self.lagoon_L
        design['Lagoon width'] = W = self.lagoon_W
        design['Lagoon depth'] = depth = V / (L*W)

        liner = (L*W + 2*depth*(L+W)) * N * self.liner_unit_mass
        constr = self.construction
        constr[0].quantity = liner
        constr[1].quantity = N * V # excavation

        self.add_construction(add_cost=False)

    @property
    def design_type(self):
        '''[str] Lagoon type, can be either "anaerobic" or "facultative".'''
        return self._design_type
    @design_type.setter
    def design_type(self, i):
        if i == self._design_type: pass
        else:
            if i == 'anaerobic':
                data = self._anaerobic_defaults
                self.line = 'Anaerobic lagoon'
            elif i == 'facultative':
                data = self._facultative_defaults
                self.line = 'Facultative lagoon'
            else:
                raise ValueError('`design_type` can only be "anaerobic" or "facultative", '
                                 f'not {i}.')
            for para in data.index:
                value = float(data.loc[para]['expected'])
                setattr(self, para, value)
        self._design_type = i

    @property
    def COD_removal(self):
        '''[float] Fraction of COD removed during treatment.'''
        return self._COD_removal
    @COD_removal.setter
    def COD_removal(self, i):
        self._COD_removal = i

    @property
    def COD_decay(self):
        '''[float] Fraction of removed COD that decays.'''
        return self._COD_decay
    @COD_decay.setter
    def COD_decay(self, i):
        self._COD_decay = i

    @property
    def P_removal(self):
        '''[float] Fraction of P removed during treatment.'''
        return self._P_removal
    @P_removal.setter
    def P_removal(self, i):
        self._P_removal = i

    @property
    def N_lagoon(self):
        '''[int] Number of lagoons, float will be converted to the smallest integer.'''
        return self._N_lagoon
    @N_lagoon.setter
    def N_lagoon(self, i):
        self._N_lagoon = ceil(i)

    @property
    def flow_rate(self):
        '''
        [float] Total flow rate through the lagoon (to calculate retention time), [m3/d].
        If not provided, will calculate based on F_vol_in.
        '''
        return self._flow_rate if self._flow_rate else self.F_vol_in*24
    @flow_rate.setter
    def flow_rate(self, i):
        self._flow_rate = i

    @property
    def tau(self):
        '''[float] Residence time, [d].'''
        if self._lagoon_V:
            return self._lagoon_V*self.N_lagoon/self.flow_rate
        else:
            return self._tau
    @tau.setter
    def tau(self, i):
        if self._lagoon_V:
            msg = f'Residence time set, the original lagoon volume of {self._lagoon_V} m3 is ignored.'
            warn(msg, source=self)
            self._lagoon_V = None
        self._tau = i

    @property
    def lagoon_V(self):
        '''[float] Volume of the lagoon, [m3].'''
        if self._tau:
            return self._tau*(self.F_vol_in)*24/self.N_lagoon
        else:
            return self._lagoon_V
    @lagoon_V.setter
    def lagoon_V(self, i):
        if self._tau:
            msg = f'Lagoon volume set, the original residence time of {self._tau} d is ignored.'
            warn(msg, source=self)
            self._tau = None
        self._lagoon_V = i

    @property
    def lagoon_L(self):
        '''[float] Length of the lagoon, [m].'''
        return self._lagoon_L
    @lagoon_L.setter
    def lagoon_L(self, i):
        self._lagoon_L = i

    @property
    def lagoon_W(self):
        '''[float] Width of the lagoon, [m].'''
        return self._lagoon_W
    @lagoon_W.setter
    def lagoon_W(self, i):
        self._lagoon_W = i

    @property
    def liner_unit_mass(self):
        '''[float] Unit mass of the lagoon liner, [kg/m2].'''
        return self._liner_unit_mass
    @liner_unit_mass.setter
    def liner_unit_mass(self, i):
        self._liner_unit_mass = i