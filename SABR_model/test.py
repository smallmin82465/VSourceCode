import numpy as np
from scipy.optimize import minimize, differential_evolution
import matplotlib.pyplot as plt

def SABR(alpha, beta, rho, nu, F, K, time, MKT=0):
    """
    Returns estimated market volatilities using Hagan's [2002] formulae.
    Uses the shortened form in the ATM case to speed up computations.
    Each input value is a scalar.
    """

    if K <= 0:
        raise Exception("Negative Rates Detected. Need to shift the smile.")

    elif F == K: #ATM shortened formula
        V = (F*K)**((1-beta)/2)
        B = 1 + (((1-beta)**2 * alpha**2)/(24*(V**2)) + (rho*beta*alpha*nu)/(4*V) + ((2-3*(rho**2))*(nu**2))/(24)) * time
        # estimated volatility
        VOL = (alpha/V)*B

    elif F != K: #NON-ATM formula
        V = (F*K)**((1-beta)/2)
        log_FK = np.log(F/K)
        z = (nu*V*log_FK)/alpha
        x = np.log((np.sqrt(1-2*rho*z+z**2)+z-rho)/(1-rho))
        A = 1 + ((1-beta)**2*log_FK**2)/24 + ((1-beta)**4*log_FK**4)/1920
        B = 1 + (((1-beta)**2 * alpha**2)/(24*(V**2)) + (rho*beta*alpha*nu)/(4*V) + ((2-3*(rho**2))*(nu**2))/(24))*time
        # estimated volatility
        VOL = (alpha/(V*A)) * (z/x) * B

    return VOL

