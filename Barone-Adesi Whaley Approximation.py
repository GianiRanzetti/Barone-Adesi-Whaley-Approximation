import numpy as np
import scipy.stats as si
import math

# Creates a normal distribution
def Normal_dist(x):
    Normal_dist = si.norm.cdf(x,0.0,1.0)
    return (Normal_dist)

# Prices a European call option
def GeneralizedBlackScholesCall(StockPrice, StrikePrice, Maturity, RiskFreeRate, DividendYield, Volatility):
    d1 = (np.log(StockPrice/StrikePrice)+(RiskFreeRate-DividendYield+0.5*Volatility**2)*Maturity)/(Volatility*np.sqrt(Maturity))
    d2 = (np.log(StockPrice/StrikePrice)+(RiskFreeRate-DividendYield-0.5*Volatility**2)*Maturity)/(Volatility*np.sqrt(Maturity))
    GeneralizedBlackScholesCall = StockPrice*np.exp(-DividendYield*Maturity)*Normal_dist(d1)-StrikePrice*np.exp(-RiskFreeRate*Maturity)*Normal_dist(d2)
    return(GeneralizedBlackScholesCall)

# Prices a European Put option
def GeneralizedBlackScholesPut(StockPrice, StrikePrice, Maturity, RiskFreeRate, DividendYield, Volatility):
    d1 = (np.log(StockPrice/StrikePrice)+(RiskFreeRate-DividendYield+0.5*Volatility**2)*Maturity)/(Volatility*np.sqrt(Maturity))
    d2 = (np.log(StockPrice/StrikePrice)+(RiskFreeRate-DividendYield-0.5*Volatility**2)*Maturity)/(Volatility*np.sqrt(Maturity))
    GeneralizedBlackScholesPut = StrikePrice*np.exp(-RiskFreeRate*Maturity)*Normal_dist(-d2)-StockPrice*np.exp(-DividendYield*Maturity)*Normal_dist(-d1)
    return(GeneralizedBlackScholesPut)


# Calculates the Probability Density Function (PDF) for a normal distribution
def NormDist(x):
    NormDist = 1 / np.sqrt(2 * math.pi) * np.exp(-x ** 2 / 2)
    return (NormDist)


# Calculates S* the underlying price at which it is optimal to exercise early for a call
def Opt_Strike_Call(StrikePrice, Maturity, RiskFreeRate, DividendYield, Volatility):
    b = RiskFreeRate - DividendYield

    ##II Calculation of seed value, Si
    N = 2 * b / Volatility ** 2
    m = 2 * RiskFreeRate / Volatility ** 2
    q2u = (-(N - 1) + np.sqrt((N - 1) ** 2 + 4 * m)) / 2
    su = StrikePrice / (1 - 1 / q2u)
    h2 = -(b * Maturity + 2 * Volatility * np.sqrt(Maturity)) * StrikePrice / (su - StrikePrice)
    Si = StrikePrice + (su - StrikePrice) * (1 - np.exp(h2))
    K = 2 * RiskFreeRate / (Volatility ** 2 * (1 - np.exp(-RiskFreeRate * Maturity)))
    d1 = (np.log(Si / StrikePrice) + (b + Volatility ** 2 / 2) * Maturity) / (Volatility * np.sqrt(Maturity))
    Q2 = (-(N - 1) + np.sqrt((N - 1) ** 2 + 4 * K)) / 2
    LHS = Si - StrikePrice
    RHS = GeneralizedBlackScholesCall(Si, StrikePrice, Maturity, RiskFreeRate, DividendYield, Volatility) + (1 - np.exp((b - RiskFreeRate) * Maturity)) * Normal_dist(d1) * Si / Q2
    b = RiskFreeRate - DividendYield
    bi = np.exp((b - RiskFreeRate) * Maturity) * Normal_dist(d1) * (1 - 1 / Q2) + (1 - np.exp((b - RiskFreeRate) * Maturity) * Normal_dist(d1) / (Volatility * np.sqrt(Maturity))) / Q2
    E = 0.000001

    ### II Newton Raphson algorithm for finding critical price Si
    while abs(LHS - RHS) / StrikePrice > E:
        Si = (StrikePrice + RHS - bi * Si) / (1 - bi)
        d1 = (np.log(Si / StrikePrice) + (b + Volatility ** 2 / 2) * Maturity) / (Volatility * np.sqrt(Maturity))
        LHS = Si - StrikePrice
        RHS = GeneralizedBlackScholesCall(Si, StrikePrice, Maturity, RiskFreeRate, DividendYield, Volatility) + (1 - np.exp((b - RiskFreeRate) * Maturity) * Normal_dist(d1)) * Si / Q2
        b = RiskFreeRate - DividendYield
        bi = np.exp((b - RiskFreeRate) * Maturity) * Normal_dist(d1) * (1 - 1 / Q2) + (1 - np.exp((b - RiskFreeRate) * Maturity) * NormDist(d1) / (Volatility * np.sqrt(Maturity))) / Q2
        Opt_Strike_Call = Si
    return (Opt_Strike_Call)


# Prices the American Call option
def BAW_Call(StockPrice, StrikePrice, Maturity, RiskFreeRate, DividendYield, Volatility):
    b = RiskFreeRate - DividendYield
    if b >= RiskFreeRate:
        BAW_Call = GeneralizedBlackScholesCall(StockPrice, StrikePrice, Maturity, RiskFreeRate, DividendYield, Volatility)
        b = RiskFreeRate - DividendYield
    else:
        Sk = Opt_Strike_Call(StrikePrice, Maturity, RiskFreeRate, DividendYield, Volatility)
        b = RiskFreeRate - DividendYield
        N = 2 * b / Volatility ** 2
        K = 2 * RiskFreeRate / (Volatility ** 2 * (1 - np.exp(-RiskFreeRate * Maturity)))
        d1 = (np.log(Sk / StrikePrice) + (b + Volatility ** 2 / 2) * Maturity) / (Volatility * np.sqrt(Maturity))
        Q2 = (-(N - 1) + np.sqrt((N - 1) ** 2 + 4 * K)) / 2
        a2 = (Sk / Q2) * (1 - np.exp((b - RiskFreeRate) * Maturity) * Normal_dist(d1))
        if StockPrice < Sk:
            BAW_Call = GeneralizedBlackScholesCall(StockPrice, StrikePrice, Maturity, RiskFreeRate, DividendYield, Volatility) + a2 * (StockPrice / Sk) ** Q2
        else:
            BAW_Call = StockPrice - StrikePrice
    return (BAW_Call)


# Calculates S* the underlying price at which it is optimal to exercise early for a put
def Opt_Strike_Put(StrikePrice, Maturity, RiskFreeRate, DividendYield, Volatility):
    b = RiskFreeRate - DividendYield
    ##II Calculation of seed value, Si
    N = 2 * b / Volatility ** 2
    m = 2 * RiskFreeRate / Volatility ** 2
    q1u = (-(N - 1) - np.sqrt((N - 1) ** 2 + 4 * m)) / 2
    su = StrikePrice / (1 - 1 / q1u)
    h1 = (b * Maturity - 2 * Volatility * np.sqrt(Maturity)) * StrikePrice / (StrikePrice - su)
    Si = su + (StrikePrice - su) * np.exp(h1)
    k = 2 * RiskFreeRate / (Volatility ** 2 * (1 - np.exp(-RiskFreeRate * Maturity)))
    d1 = (np.log(Si / StrikePrice) + (b + Volatility ** 2 / 2) * Maturity) / (Volatility * np.sqrt(Maturity))
    Q1 = (-(N - 1) - np.sqrt((N - 1) ** 2 + 4 * k)) / 2
    LHS = StrikePrice - Si
    RHS = GeneralizedBlackScholesPut(Si, StrikePrice, Maturity, RiskFreeRate, DividendYield, Volatility) - (1 - np.exp((b - RiskFreeRate) * Maturity) * Normal_dist(-d1)) * Si / Q1
    b = RiskFreeRate - DividendYield
    bi = -np.exp((b - RiskFreeRate) * Maturity) * Normal_dist(-d1) * (1 - 1 / Q1) - (1 + np.exp((b - RiskFreeRate) * Maturity) * NormDist(-d1) / (Volatility * np.sqrt(Maturity))) / Q1
    E = 0.000001
    while abs(LHS - RHS) / StrikePrice > E:
        Si = (StrikePrice - RHS + bi * Si) / (1 + bi)
        d1 = (np.log(Si / StrikePrice) + (b + Volatility ** 2 / 2) * Maturity) / (Volatility * np.sqrt(Maturity))
        LHS = StrikePrice - Si
        RHS = GeneralizedBlackScholesPut(Si, StrikePrice, Maturity, RiskFreeRate, DividendYield, Volatility) - (1 - np.exp((b - RiskFreeRate) * Maturity) * Normal_dist(-d1)) * Si / Q1
        b = RiskFreeRate - DividendYield
        bi = -np.exp((b - RiskFreeRate) * Maturity) * Normal_dist(-d1) * (1 - 1 / Q1) - (1 + np.exp((b - RiskFreeRate) * Maturity) * Normal_dist(-d1) / (Volatility * np.sqrt(Maturity))) / Q1
        Opt_Strike_Put = Si
    return (Opt_Strike_Put)


# Prices the American Put option
def BAW_Put(StockPrice, StrikePrice, Maturity, RiskFreeRate, DividendYield, Volatility):
    b = RiskFreeRate - DividendYield
    Sk = Opt_Strike_Put(StrikePrice, Maturity, RiskFreeRate, DividendYield, Volatility)
    b = RiskFreeRate - DividendYield
    N = 2 * b / Volatility ** 2
    k = 2 * RiskFreeRate / (Volatility ** 2 * (1 - np.exp(-RiskFreeRate * Maturity)))
    d1 = (np.log(Sk / StrikePrice) + (b + Volatility ** 2 / 2) * Maturity) / (Volatility * np.sqrt(Maturity))
    Q1 = (-(N - 1) - np.sqrt((N - 1) ** 2 + 4 * k)) / 2
    a1 = -(Sk / Q1) * (1 - np.exp((b - RiskFreeRate) * Maturity) * Normal_dist(-d1))
    if StockPrice > Sk:
        BAW_Put = GeneralizedBlackScholesPut(StockPrice, StrikePrice, Maturity, RiskFreeRate, DividendYield, Volatility) + a1 * (StockPrice / Sk) ** Q1
        b = RiskFreeRate - DividendYield
    else:
        BAW_Put = StrikePrice - StockPrice
    return (BAW_Put)

# Assumptions: Values for Apple stock on February 2 2024 (In later versions of this code, stock data should be automatically inserted)
StockPrice = 180.23
StrikePrice = 180 #the put is at-the-money
Maturity = 2
RiskFreeRate = 0.0585
DividendYield = 0.0051
Volatility = 0.2213
roi3 = BAW_Call(StockPrice, StrikePrice, Maturity, RiskFreeRate, DividendYield, Volatility)
print("The fair value of the American call option based on the Barone-Adesi and Whaley Model is: ${:.5}".format(roi3))
print("The actual value of the American call option based the Nasdaq website on the 2nd Feb 2024 is: $34.63")
roi4 = BAW_Put(StockPrice, StrikePrice, Maturity, RiskFreeRate, DividendYield, Volatility)
print("\nThe fair value of the American put option based on the Barone-Adesi and Whaley Model is: ${:.5}".format(roi4))
print("The actual value of the American put option based the Nasdaq website on the 2nd Feb 2024 is: $16.70")