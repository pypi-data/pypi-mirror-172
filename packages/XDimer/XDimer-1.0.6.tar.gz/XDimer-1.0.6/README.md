# xDimers

Pyhton package for simulating multi-molecular emission spectra dominated by a single effective intermolecular vibrational mode. This package will be accompanying a future publication and is available at Zenodo. 

Zenodo:

[![DOI](https://zenodo.org/badge/465952131.svg)](https://zenodo.org/badge/latestdoi/465952131)

## Table of contents
1. [Installation](#1-installation)
2. [Basic introduction](#2-basic-introduction)
* [Model and definitions](#21-model-and-defintions)
* [Basic functionality](#22-basic-functionality)
* [Fitting emission data](#23-fitting-emission-data)
* [Examples](#24-examples)
3. [API reference guide](#3-api-reference-guide)
* [xdimer](#31-xdimer)
* [semiclassical](#32-semiclassical)
* [quantummechanical](#33-quantummechanical)
* [auxiliary](#34-auxiliary)
4. [License and citation](#4-license-and-citation)

## 1. Installation
Install package from PyPi with
```
pip install XDimer
```

The latest development version is available on GitHub. To install use:
```
python -m pip install git+https://github.com/HammerSeb/xDimer.git
```

The package has been tested against the latest versions of python > 3.6 .

## 2.Basic Introduction

This package enables the quick simulation of emission spectra from Franck-Condon vibronic transitions between the vibrational levels of two harmonic oscillators with different potential strength at different temperatures. For this purpose, it provides two ways to simulate the emission, a semi-classical one for which the final state harmonic oscillator is treated as a continous function and a full quantum-mechanical approach, for which the individual Franck-Condon factors are calculated numerically. A short introduction of the underlying physical model as well as some basic defintions are given [below](#21-basic-defintions) please refere to the [related publication](#citation) for an in detail description of the physical model and the mathematical definition.

### 2.1 Model and defintions

The emission spectra are modeled by Franck-Condon transitions between two displaced harmonic oscillators described by
$$R(q) = R q^2$$

with $q$ as the generalized spatial coordinate and the
> **oscillator constant** $R$.

which is related to the 

> **vibrational energy quantum** $E_{vib}$

and the 

> **oscillator parameter** $\alpha$

via the reduced mass as

$$R = \frac{\mu}{\hbar^2}E_{vib}^2 $$

and 

$$\alpha = \frac{\mu}{\hbar^2}E_{vib} .$$

The oscillators are displaced in energy by the
> **energetic offset** $D_e$

and along the generalized spatial coordinate by the
> **spatial displacement** $q_e$

each with respect to the vertex of the ground state parabola. 

Variable names are declared throughtout the package as follows: 

> `gs_potential` : ground state oscillator constant
>
> `xs_potential` : excited state oscillator constant
>
> `gs_vib_energy` : ground state vibrational energy quantum
>
> `xs_vib_energy` : excited state vibrational energy quantum
>
> `gs_parameter` : ground state oscillator parameter
>
> `xs_parameter` : excited state oscillator parameter
>
> `q_xs` : spatial displacement along generalized coordinate
>
> `e_offset` : energetic offset of the oscillators
>
>`mass` : reduced mass of the system in atomic units u

For the quantummechanical simulation of emission spectra the energetic broadening of the underlying lineshape function is declared as
> `energetic_broadening`

### 2.2 Basic functionality

The package consists of three main parts contained in the [`xdimer`](#31-xdimer) module which is loaded by

```python
import xdimer
```

This module contains the class [`dimer_system`](#dimersystem) whicht stores the key parameters which fully define a dimer system. The functions [`semiclassical_emission`](#semiclassicalemission) and [`quantummechanical_emission`](#quantummechanicalemission) take instances of the [`dimer_system`](#dimersystem) class as an input and return the respective emission spectra. 

#### Set up a dimer system

To create a dimer system use
```python
dimer = xdimer.dimer_system(mass, gs, xs, q_xs, e_offset)
```
In the default `setup_mode` the parameters `gs` and `xs` define the ground state (gs) and excited state (xs) vibrational energy quantum (in eV). The parameters `q_xs` and `e_offset` are the spatial displacement $q_e$ (in Angstrom) and energetic offset $D_e$ (in eV). The `mass` parameter is the reduced mass $\mu$ of the dimer system in atomic units. Hence, 
```python
dimer = xdimer.dimer_system(423, 0.02, 0.025, 0.1, 1.5)
```
defines a dimer system with reduced mass **423 u**, ground and excited state vibrational energy quantums of **20 meV** and **25 meV**, respecitvely, an excited state spatial displacement of **0.1 Angstrom** and an energetic offset of **1.5 eV**. 

#### Calculating emission spectra

Emission spectra can be calculated by a semi-classical or quantum-mechanical approach. To calculate semi-classical emission spectra use
```python
spectra = xdimer.semiclassical_emission(E, temp, dimer)
```
where `E` is of `ndarray`-type and defines the energy axis over which the emission is calculated. The temperatures for which the spectra are calcualted are given by `temp` either as a `list` of several temperatures or a single temperature value as a `float`. The `dimer` is an instance of `dimer_system` (`dimer` can also be a `list`, see [API reference](#semiclassicalemission)). The function [`semiclassical_emission`](#semiclassicalemission) returns either a `dictonary`, if the temperature input was given as a list of several values, or a `ndarray` if only one temperature value was provided. The return variable is compased as follows

>**For a single temperature value:**
>`emission` is an array of the form
>
>`emission[0]` input variable `E` as energy axis
>
>`emission[i]` from i = 1,...,6. The emission spectrum of the i-th vibrational level of the excited state
>
>`emission[7]` total emission spectrum as sum over all emissions from the first 6 vibrational levels of the excited state
>
>**For a list of temperature values `temp=[T1, T2, T3, ...]`** 
>`emission` is a dictionary with keys T1, T2, T3, ... . Each entry contains an array for a single temperature value as described above. 

The quantummechanical emission is calculated by 
```python
emission = xdimer.quantummechanical_emission(E, temp, dimer)
```
where `E` is of `ndarray`-type and defines the energy axis over which the emission spectra are calculated. The temperatures are given by `temp` either as a `list` of several temperatures or a single temperature value as a `float`. The `dimer` is an instance of `dimer_system` (`dimer` can also be a `list`, see [API reference](#quantummechanicalemission)). The function [`quantummechanical_emission`](#quantummechanicalemission) returns pairs of array like return values 
```python
[spectra_full, spectra_stick] 
```
either as entrys in a dictonary keyed by multiple temperature values given in `temp`, or a single array pair if only one temperature value was given. If n vibrational levels of the excited state (0, ..., n-1) are simulated

**`spectra_stick`** is a list of `ndarrays` of length n. Each entry `i` contains the transition energies and intensities of all transitions from the i-th vibrational level of the excited state to the manifold of simulated ground state levels (default is 25). The relation between emission energy and tranisition intensity is referred to as stick spectrum of the i-th vibrational level.

> **The stick spectrum** of the i-th vibrational level is given as
>
>`spectrum_stick[i][0]` quantum number k of the vibrational level of the respective final state
>
>`spectrum_stick[i][1]` photon energy of the $\ket{i} \rightarrow \ket{k}$ transition
>
>`spectrum_stick[i][2]` Franck-Condon factor $|\braket{k|i}|^2$ transition weighted with a respective Boltzmann factor

**`spectra_full`** is a `ndarray` and contains the convolution of the stick spectra with a gaussian line shape function of energetic broadening w (specified as an optional parameter when creating a [`dimer_system`](#dimersystem) instance) resulting in smooth emission spectra. 

>**The smooth emission spectra** are returned as
>
>`spectra_full[0]`: input variable `E` as energy axis
>
>`spectra_full[i]`: from i = 1 to the last simulated vibrational level n. The emission spectrum of the i-th vibrational level of the excited state as the sum of gaussian line shapes for each transition specified in `spectra_stick[i]`.
>
>`spectra_full[n+1]`: total emission spectrum as sum over all emissions from the simulated ;eve;s vibrational levels of the excited state

The **default settings** of the function simulates the **first five vibrational levels** of the excited states.

### 2.3 Fitting emission data

To use the emission functions to fit a luminescence data set the `dimer` input can be given as a `list` containing the variables for an optimization procedure.

For `semiclassical_emission` the list needs to be of the following form:
```python
[gs_potential, xs_parameter, e_offset, q_xs, mass]
```

For `quantummechanical_emission` the list needs to be of the following form:
```python
[gs_parameter, xs_parameter, e_offset, q_xs, energetic_broadening, mass]
```

### 2.4 Examples

Two examples are provided showing how to simulate spectra and use the provided functions to fit a set of temperature dependent luminescence data. 

They can be called by

```
python -m xdimer.examples.simulating_emission
```

and 

```
python -m xdimer.examples.fitting_emission_data
```

**simulating_emission** simulates a semiclassical and quantum-mechanical emission spectrum for a temperature specified by console input when running the module. The individual vibrational contributions from the excited state are unraveled and depicted color coded with the main emission spectrum. The dimer system used in the simulation is created by
```python
dimer = xdimer.dimer_system(577.916/2, .022, .026, 0.1, 1.55, energetic_broadening=.02)
```

**fitting_emission_spectra** simulates a data set of emission data using `xdimer.quantummechanical_emission` for four different temperatures. It then performs a fit to the whole data set, including all temperatures. The fit does take a while (approx 90 seconds). The dimer system used to generate the data set is created by
```python
dimer = xdimer.dimer_system(400, .027, .023, 0.08 ,1.55, energetic_broadening= .019)
```


## 3. API reference guide
API reference guide for all classes and functions available.

### 3.1 xdimer 
Base functionality of the package containing the `dimer_system` class, the functions `semiclassical_emission` and `quantummechanical_emission` and the exception `xDimerModeError`. Import by
```python
import xdimer
```

#### dimer_system

Class defining a dimer system containing all defining physical quantities. Instances are created via
```python
dimer_system(mass, gs, xs, q_xs, e_offset, energtic_broadening, setup_mode)
```
`mass`, `q_xs` and `e_offset` are the reduced mass (in atomic units), the spatial displacement (in Angstrom) and the energetic offset (in eV), respectively. 

`gs` and `xs` define the ground and excited state potential, respectively. See `setup_mode` for details.

`energetic_broadening` defines the line width parameter as standard deviation of the gaussian linshape of each vibronic transition calculated by `quantummechanical_emission` in eV. Default is `0.02`. 

`setup_mode` defines the input mode for the defintion of the ground and exited state potential by the variables `gs` and `xs`, respectively. Accepted inputs `'vib_energy'` (default), `'osc_const'` and `'osc_para'`. 

> `'vib_energy'` (default): potentials are defined by their vibrational energy quantum $E_{vib}$ in eV. 
>
> `'osc_const'`: potentials are defined by their oscillator constant $R$ in eV/Angstrom^2.
>
> `'osc_para'`: potentials are defined by their oscillator parameter $\alpha$ in 1/Angstrom^2.

If none of the above modes is used [`xDimerModelError`](#errors-and-exceptions) is raised.

Dimer properties can be accessed by calling the respective internal variable:
>reduced mass: `dimer_system.mass`
>
>spatial offset: `dimer_system.q_xs`
>
>energetic offset: `dimer_system.e_offset`
>
>energetic broadening: `dimer_system.energetic_broadening` 

Parameters of the harmonic potentials can be returned by properties:
>Vibrational energy quantum
>
>`dimer_system.gs_vib_energy`: ground state
>
>`dimer_system.xs_vib_energy`: excited state
>
>Oscillator constant
>
>`dimer_system.gs_potential`: ground state
>
>`dimer_system.xs_potential`: excited state
>
>Oscillator parameter
>
>`dimer_system.gs_parameter`: ground state
>
>`dimer_system.xs_parameter`: excited state

#### semiclassical_emission
Calculates and returns a semiclassical emission spectrum for a dimer system at a given temperature or list a of temperatures. The first ***six*** vibrational levels of the excited state are taken into account.
```python
semiclassical_emission(E, temp, dimer)
```
***Arguments:***
> `E` (1-D ndarray): photon emission energy in eV
>
>`temp` (list/Float): either list of floats or float: List of temperature values or single temperature value in Kelvin
>
>`dimer` (instance dimer_system/list): either instance of dimer_system class or list of variables
>
>       instance dimer_system: use for simulation of emission spectra from exisiting dimer system
>
>       list: use for fitting a data set, list needs to be of the form [0: gs_potential, 1: xs_parameter, 2: e_offset, 3: q_xs, 4: mass]
COMMENT: mass should not be used as a free fit parameter but be set to the reduced mass of the dimer system

***Returns:***
> dict/ndarray:   if temp is list, dictionary (key = temp): ndarrays containing emission spectra for respective temperature temp
>
> if temp is float: ndarray containing emission spectra for respective temperature temp
>
>array structure: [8, size(E)]:  
>
>`array[0]   = E` (emission energies)
>
>`array[i+1]`: X-dimer emission spectrum from the i-th excited vibrational state (i in [0,...,5])
>
>`array[7]` : Semi-classical X-dimer emission spectrum at temperature "temp" considering the first six vibrational levels of the excited state oscillator

***Example***
```python
import numpy as np
import xdimer
# initilazises dimer system
dimer = xdimer.dimer_system(400, 0.22, 0.25, 1.5)
# Define energy axis for simulation and temperatures
E = np.linspace(1, 3, 500)
temp = [5, 50, 100, 150, 200, 250, 300]
# calculate emission spectra for given temperatures
spectra = xdimer.semiclassical_emission(E, temp, dimer)
spectrum_150K = spectra[150]
```

#### quantummechanical_emission

Calculates and returns a quantummecanical emission spectrum for a dimer system at a given temperature or list a of temperatures. Function returns stick spectra and continous spectrum as superposition of gaussian emissions with intensity and position defined by the stick spectrum
```python
quantummechanical_emission(E, temp, dimer, simulation_parameters = [5, -.5, .5, 10000, 25])
```
***Arguments:***
>`E` (ndarray): photon emission energy in eV
>
>`temp` (list/Float): either list of floats or float: List of temperature values or single temperature value in Kelvin
>
>`dimer` (instance dimer_system/list): either instance of dimer_system class or list of variables
>
>       instance dimer_system: use for simulation of emission spectra from exisiting dimer system
>       list: use for fitting a data set, list needs to be of the form [0: gs_parameter, 1: xs_parameter, 2: e_offset, 3: q_xs, 4: energetic_broadening, 5: mass]
>
>`simulation_parameters` (list, optional): specifies the simulation parameters `[n_sim, q_low, q_high, dq, n_gs]`. First entry `n_sim` sets **number of simulated vibrational levels of excited state**. Other four parameters specify numeric evaluation of Franck-Condon factors, see [`quantummechanical.franck_condon_factor`](#franckcondonfactors).  Defaults to [5 ,-.5, .5, 10000, 25].

COMMENT: mass should not be used as a free fit parameter but be set to the reduced mass of the dimer system

***Returns***
> dict/list:      if temp is list, dictionary (key = temp): each entry contains list of the form `[spectra_full, spectra_stick]`
>
>if temp is float: list of the form `[spectra_full, spectra_stick]` for respective temperature temp
>
> `spectra_full` (ndarray):     
>
>`[0] = E` (emission energies)
>
>`[1: n_sim]`: smooth emission spectrum for 0-th to (n_sim-1)-th vibrational level of excited state
>
>`[n_sim+1]`: full emission spectrum as sum over all excited state transitions from 0-th to (n_sim-1)-th
>
>`spectra_stick` (list of ndarrays):  list of length n_sim. 
>
>Each entry contains the output of quantummechanical.franck_condon_factor as ndarray `[0: final state, 1: transition energies, 2: boltzmann weighted transition intensities]` for the respective excited state level, i.e. `spectra_stick[0]` holds 0-th vibrational level, `spectra_stick[1]` holds 1-st vibrational level and so forth.

***Example***
```python
import numpy as np
import xdimer
# initilazises dimer system
dimer = xdimer.dimer_system(400, 0.22, 0.25, 1.5)
# Define energy axis for simulation and temperatures
E = np.linspace(1, 3, 500)
temp = [5, 50, 100, 150, 200, 250, 300]
# calculate emission spectra for given temperatures
spectra = xdimer.quantummechanical_emission(E, temp, dimer)
qm_150K = spectra[150]
spectra150K, stick_spectra150K = qm_150k[0], qm_150k[1]
```

#### Errors and Exceptions
```python
xDimerModeError(Exception):
```
Subclass of Exception. Raised if instance of dimer_system class is created using an unknown setup mode.

### 3.2 semiclassical
Contains the functions to calculate a semi-classical emission spectrum. Can be imported by
```python
import xdimer.semiclassical
```

#### excited_state_energy
```python
excited_state_energy(n,vib_zero_point_energy,e_offset)
```
auxiliary function for semi-classical emission spectra. Calculates excited state energy of vibrational level n with respect to ground state minimum in eV. Equation (5) in publication.

***Arguments:***
>`n `(int): vibrational level n
>
>`vib_zero_point_energy` (Float): vibrational zero point energy in eV 
>
>`e_offset` (Float): energetic offset with respect to ground state minimum in eV

***Returns:***
> Float: excited state energy of vibrational level n in eV

#### displacement_from_energy
```python
displacement_from_energy(E, n, gs_potential, vib_zero_point_energy, e_offset, q_xs):
```
auxiliary function for semi-classical emission spectra. Inverse function of the emission energy - spatial coordinate relation. Calculates spatial displacement as function of photon energy for emission from the excited state at vibrational level `n` in Angstrom. Equation (S4) in electronic supplementary information.

***Arguments:***
> `E` (ndarray): photon emission energy in eV
>
>`n` (Int): vibrational level n
>
>`gs_potential` (Float): oscillator constant $R_0$ of the ground state potential in eV/Angstrom**2
>
>`vib_zero_point_energy` (Float): vibrational zero point energy in eV
>
>`e_offset` (Float): energetic offset with respect to ground state minimum in eV
>
>`q_xs` (Float): spatial displacement of excited state with respect to the ground state minimum in Angstrom

***Returns:***
>ndarray: spatial displacement in Angstrom

#### xdimer_sc_emission
There six numbered functions from i= [0 to 5] which calculate the semi-classical emission spectrum from the i-th vibrational level of the excited state (c.f. equations (S7)-(S12) in electronic supplementary information). The emission from the ground state is disccused here exemplarily. 
```python
xdimer_sc_emission_0(E, gs_potential, xs_parameter ,vib_zero_point_energy, e_offset, q_xs)
```
Semi-classical X-dimer emission spectrum from the vibrational ground state

***Arguments:***
>`E` (ndarray): photon emission energy in eV
>
>`gs_potential` (Float): oscillator constant $R_0$ of the ground state potential in eV/Angstrom**2
>
>`xs_parameter` (Float): oscillator parameter of excited state quantum-mechanical oscillator in 1/Angstrom**2 (alpha in manuscript)
>
>`vib_zero_point_energy` (Float): vibrational zero point energy in eV
>
>`e_offset` (Float): energetic offset with respect to ground state minimum in eV
>
>`q_xs` (Float): spatial displacement of excited state with respect to the ground state minimum in Angstrom

***Returns:***
>ndarray: size: size(E). emission intensity with respect to values of E. **nan-values resulting from E-values greater than singularity are set to 0 to ensure down the line usability.**

For higher vibrational levels use `xdimer_sc_emission_1`, `xdimer_sc_emission_2`, `xdimer_sc_emission_3`, `xdimer_sc_emission_4` and `xdimer_sc_emission_5`.

#### xdimer_sc_total_emission
```python 
xdimer_sc_total_emission(E, gs_potential, xs_parameter ,vib_zero_point_energy, e_offset, q_xs, boltzmann_dist, temp)
```
Semi-classical X-dimer emission spectrum at temperature "temp" considering the first six vibrational levels of the excited state oscillator

***Arguments:***
>`E` (ndarray): photon emission energy in eV
>
>`gs_potential` (Float): oscillator constant $R_0$ of the ground state potential in eV/Angstrom**2
>
>`xs_parameter` (Float): oscillator parameter of excited state quantum-mechanical oscillator in 1/Angstrom**2 
>
>`vib_zero_point_energy` (Float): vibrational zero point energy in eV
>
>`e_offset` (Float): energetic offset with respect to ground state minimum in eV
>
>`q_xs` (Float): spatial displacement of excited state with respect to the ground state minimum in Angstrom
>
>`boltzmann_dist` (Dict): Boltzman distribution generated with [`auxiliary.boltzmann_distribution`](#boltzmanndistribution)
>
>`temp` (Float): Temperature in Kelvin - must be key in dictionary boltzmann_dist

***Returns:***
>ndarray: size(E). emission intensity with respect to values of E. **nan-values resulting from E-values greater than singularity are set to 0 to ensure down the line usability.**

### 3.3 quantummechanical
Contains the functions to calculate a quantum-mechanical emission spectrum. Can be imported by
```python
import xdimer.quantummechanical
```

#### harmonic_oscillator_wavefunction
```python
harmonic_oscillator_wavefunction(level, spatial_coordinate, oscillator_parameter)
```
Auxiliary function to caluclate the wave function of harmonic oscillator functions of a given vibrational level.

***Arguments:***
> `level` (Int): oscillator quantum number
>
>`spatial_coordinate` (ndarray): array of spatial coordinates (in Angstrom) for which wavefunction is calculated
>
>`oscillator_parameter` (_type_): oscillator parameter alpha in 1/Angstrom**2

#### 

***Returns:***
>ndarray: values of the wavefuncion at given spatial coordinates


#### franck_condon_factors
```python
franck_condon_factor(level, xs_parameter, gs_parameter, q_xs, e_offset, mass, q_low= -.5, q_high= .5, dq= 10000, n_gs= 25)
```

numerically calculates  emission energies and respective Franck-Condon factors for the emission from a vibrational level (given by 'level') of an excited state oscillator to the vibrational levels of a ground state harmonical oscillator

***Arguments:***
>`level` (Int): oscillator quantum number
>
>`xs_parameter` (Float): excited state oscillator parameter alpha in 1/Angstrom**2
>
>`gs_parameter` (Float): ground state oscillator parameter alpha in 1/Angstrom**2
>
>`q_xs` (Float): spatial displacement of excited state with respect to the ground state minimum in Angstrom
>
>`e_offset` (Float): energetic offset with respect to ground state minimum in eV
>`mass` (Float): mass of the dimer system in kg
> 
>*Simulation parameters - optional*
>
>`q_low` (int, optional): lower intergration boundary of spatial coordinate. Defaults to -1.
>
>`q_high` (int, optional): upper intergration boundary of spatial coordinate. Defaults to 1.
>
>`dq`(int, optional): value number between lower and upper integration boundary of spatial coordinate, determines spatial resolution during integration. Defaults to 10000.
>
>`n_gs` (int, optional): simulated levels of the ground state oscillator. Defaults to 25.

***Returns:***
>ndarray: size(3, n_GS)
>
>`[0,:]`: int:  quantum number of respective final vibratioanl state k of ground state level for the transition n --> k
>
>`[1,:]`: Floats:         photon energy of transition n --> k
>
>`[2,:]`: Floats:         value of Frank-Condon factor of transition n --> k

### 3.4 auxiliary
Contains auxiliary functions. Can be imported by
```python
import xdimer.auxiliary
```

#### osc_para_to_vib_energy
```python
osc_para_to_vib_energy(osc_para, mass)
```
Transforms oscillator parameter to vibrational energy quantum.

***Arguments:***
>`osc_para` (float): oscillator parameter in 1/Angstrom^2
>
>`mass` (float): reduced mass in atomic units

***Returns:***
>float: vibrational energy quantum in eV

#### vib_energy_to_osc_para
```python
vib_energy_to_osc_para(vib_energy, mass)
```
Transforms vibrational energy quantum to oscillator parameter

***Arguments:***
>`vib_energy` (float): vibrational energy quantum in eV
>
>`mass` (float): reduced mass in atomic units

***Returns:***
>float: oscillator parameter in 1/Angstrom^2

#### osc_const_to_vib_energy
```python
osc_const_to_vib_energy(osc_const, mass)
```
Transforms oscillator constant to vibrational energy quantum.

***Arguments:***
>`osc_const` (float): oscillator constant in eV/Angstrom^2
>
>`mass` (float): reduced mass in atomic units

***Returns:***
>float: vibrational energy quantum in eV

#### vib_energy_to_osc_const
```python
vib_energy_to_osc_const(vib_energy, mass)
```
Transforms vibrational energy quantum to oscillator constant

***Arguments:***
>`vib_energy` (float): vibrational energy quantum in eV
>
>`mass` (float): reduced mass in atomic units

***Returns:***
>float: oscillator constant in eV/Angstrom^2

#### boltzmann_distribution
```python
boltzmann_distribution(Temp_list, vib_zero_point_energy, no_of_states= 50)
```
Generates a Boltzmann probability distribution for a quantum-mechanical harmonic oscillator with zero point energy "vib_zero_point_energy"

***Arguments:***
> `Temp_list` (list of Floates): list of temperature values in Kelvin 
>
>`vib_zero_point_energy` (_type_): vibrational zero point energy in eV
>
>`No_of_states` (int, optional): number of simulated excited states for canocial partion sum. Defaults to 50.

***Returns:***
> dictionary: 
>
>key (Float): entries of Temp_list; 
>
>values (ndarray): (2 x no_of_states); [0]: vibrational level, [1]: corresponding occupation probability

#### gauss_lineshape
```python
gauss_lineshape(x, A, w, xc):
```
gauss function as line shape function
$$
L(x) = \frac{A}{\sqrt{2\pi\sigma}}\exp\left( - \frac{(x-x_c)^2}{2\sigma^2} \right)
$$
***Arguments:***
>`x` (ndarray): x-values
>
>`A` (Float): area under the curve
>
>`w` (Float): standard deviation
>
>`xc` (Float): x center

***Returns:***
>nadarry: function values at x-values

## 4. License and citation

### License

Package distributed under MIT license. Copyright (c) 2022 Sebastian Hammer.

### Citation

If you use this package or its contents for apublication please consider citing the zenodo archive [![DOI](https://zenodo.org/badge/465952131.svg)](https://zenodo.org/badge/latestdoi/465952131) or the corresponding publication.
