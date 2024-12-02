"""Library of routines for Piotrowski-Kik contact model.

In the following code the adopted naming convention is the one of
`PEP 8 <https://www.python.org/dev/peps/pep-0008/#naming-conventions>`_
with the exception that the function and method names are mixedCase. 

.. module:: pkmodellib

.. moduleauthor:: Rostyslav Skrypnyk
"""

# Standard library imports:

# 3rd party imports:
import numpy as np
import scipy.interpolate as spi
import scipy.integrate as spint
import matplotlib.pyplot as plt
# local library specific imports:


def getProfiles(rail_path='', wheel_path=''):
    """Returns rail and wheel profiles from given paths with Z-axis upwards.

    If no path is given, returns empty array.

    Parameters
    ----------
    rail_path : string
        path to rail profile.
    wheel_path : string
        path to wheel profile.

    Returns
    -------
    2d array
        rail profile.
    2d array
        wheel profile.
    """
    rail = []
    if rail_path:
        rail = np.loadtxt(rail_path)
        rail[:,1] = - rail[:,1] # Point z-axis upwards.
    
    wheel = []
    if wheel_path:
        wheel = np.loadtxt(wheel_path, skiprows=2)
        wheel[:,1] = - wheel[:,1] # Point z-axis upwards.

    return rail, wheel
# End function getProfiles.

# 绘制两个轮廓曲线，可用于显示车轮和轨道的轮廓
def plotProfiles(profile1, profile2=[], contact_point=[]):
    """Plot profile(s).

    Parameters
    ----------
    profile1 : 2d array
         coordinates in solid blue.
    [profile2] : 2d array
         coordinates in dashed red.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.xlabel('Y [mm]')
    plt.ylabel('Z [mm]')

    ax.plot(profile1[:,0], profile1[:,1], 'b-')

    if len(profile2) != 0:
        ax.plot(profile2[:,0], profile2[:,1], 'r--')

    if len(contact_point) != 0:
        ax.plot(contact_point[0], contact_point[1], 'ko')

    plt.tight_layout() # Adjust margins to fit tick and axis labels, and titles.
    plt.show()
# End of function plotProfiles.


def equalPoints(profile1, profile2):
    """Interpolate *profile1* with same number of points as in *profile2*.

    Parameters
    ----------
    profile1 : 2d array
        coordinates to be modified.
    profile2 : 2d array
        reference coordinates.

    Returns
    -------
    2d array
        interpolated profile.
    """
    itp = spi.interp1d(profile1[:,0], profile1[:,1], kind='linear')

    return np.array([profile2[:,0], itp(profile2[:,0])]).T
# End of function equalPoints.


def separationOfProfiles(wheel, rail):
    """Compute distance between points of two profiles f(y).

    Profiles need to be defined in a common coordinate system. The top profile
    (wheel) needs to be the first one in the list of arguments.

    Parameters
    ----------
    wheel : 2d array
        coordinates of the top profile.
    rail : 2d array
        coordinates of the bottom profile.

    Returns
    -------
    1d array
        distance between points of the two profiles.
    """
    sep = wheel[:,1] - rail[:,1]

    # Correct separation if profiles overlap or do not touch:
    min_sep = min(sep)

    return sep - min_sep
# End of function separationOfProfiles.


def interpenetration(wheel, rail, delta0):
    """Compute interpenetration function.

    The interpenetration function is defined by eq. 7 in the original article.

    Parameters
    ----------
    wheel : 2d array
        coordinates of the wheel profile.
    rail : 2d array
        coordinates of the rail profile.
    delta0 : float 
        virtual penetration.

    Returns
    -------
    1d array
        values of interpenetration function.
    """
    sep = separationOfProfiles(wheel, rail)

    interp_array = delta0 - sep

    ind = 0
    for interp in interp_array:
        if interp > 0:
            interp_array[ind] = interp
        else:
            interp_array[ind] = 0
        ind += 1

    return interp_array
# End of function interpenetration.


def nonzeroRuns(a):
    """Returns (n,2) array where n is number of runs of non-zeros.

    The first column is the index of the first non-zero in each run,
    and the second is the index of the first zero element after the run.
    This indexing pattern matches, for example, how slicing works and how
    the range function works.

    Parameters
    ----------
    a : 1d array
        input.

    Returns
    -------
    2d array
        output.
    """
    # Create an array that's 1 where a isn't 0, and pad each end with an extra 0.
    notzero = np.concatenate(([0], np.not_equal(a, 0).view(np.int8), [0]))
    absdiff = np.abs(np.diff(notzero)) # Calculate a[n+1] - a[n] for all.
    # Runs start and end where absdiff is 1.
    ranges = np.where(absdiff == 1)[0].reshape(-1, 2)
    return ranges
# End of function nonzeroRuns.

# 计算每个接触区域的最大压力
def maxPressure(wheel, g_array, radius, E, nu, delta, delta0):
    """Compute maximum pressures for all contact patches.

    Each entry of the returned array is an evaluated eq. 13 in
    the original article.

    Parameters
    ----------
    wheel : 2d array
        coordinates of the wheel.
    g_array : 1d array
        interpenetration array.
    radius : float
        wheel nominal rolling radius.
    E : float
        Young's modulus.
    nu : float 
        Poisson's ratio.
    delta : float
        penetration.
    delta0 : float
        virtual penetration.

    Returns
    -------
    1d array
        array of maximum contact pressures for each contact patch.
    """
    y_array, z_array = wheel[:,0], wheel[:,1]
    coef = 0.5 * np.pi * E * delta / (1. - nu * nu)

    # Function to compute x coordinate of the front edge of the
    # interpenetration region using in situ rolling radius:
    x_front_edge = lambda ind: np.sqrt(2. * radius * g_array[ind]) # 计算了接触区域的前沿（即椭圆的半长轴）

    # 1st integrand:
    f1 = lambda x,y,ind: np.sqrt(x_front_edge(ind) ** 2 - x * x) / \
                         np.sqrt(x * x + y * y + 1.e-10)
    # 2nd integrand:
    f2 = lambda x,ind: np.sqrt(x_front_edge(ind) ** 2 - x * x)

    # Identify regions with positive interpenetration function:
    region_array = nonzeroRuns(g_array)

    pmax_array = []
    for region in region_array:
        ind_l, ind_u = region[0], region[1]
        int2_f1 = 0
        int2_f2 = 0
        for ind in range(ind_l, ind_u):
            x_f = x_front_edge(ind)
            int2_f1 += spint.quad(lambda x: f1(x,y_array[ind],ind),
                                  - x_f, x_f,
                                  limit=100)[0]
            int2_f2 += spint.quad(lambda x: f2(x,ind),
                                  - x_f, x_f)[0]

        load = coef / int2_f1 * int2_f2
        pmax = load * np.sqrt(2. * radius * delta0) / int2_f2
        pmax_array.append(pmax)
            
    return np.array(pmax_array)
# End of function maxPressure.
