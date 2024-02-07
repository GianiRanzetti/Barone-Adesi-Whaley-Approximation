# The Barone-Adesi Whaley Approximation
The Barone- Adesi- Whaley (BAW) valuation model attempts to provide a quadratic approximation to price american options with a constant dividend yield

The pricing of an American option is esencially a european option adjusted for an early excercise.
 premium. Hence, the payoffs can be written as:

 ![image](https://github.com/GianiRanzetti/Barone-Adesi-Whaley-Approximation/assets/157379587/9d8172e1-1048-4a83-a256-8f3a888daceb)

The calculations of the relevant parameters is acheived through the following equations:
![image](https://github.com/GianiRanzetti/Barone-Adesi-Whaley-Approximation/assets/157379587/81a31154-7512-4181-92e9-5d99d5ade2a3)

The Newton-Raphson method is used to find the optimal strike price to excercise the option early. It aims to iteratively refine the estimate of the strike price until it converges to a solution. It iterates over the condition S_(i + 1) = (S_i - RHS)/(1 - b_i). When the difference between the LHS and RHS of the bottom equation is below a given threshold, we consider the S_i estimate = S*

Once The optimal strike price is calculated, it is only a matter of plugging in all the values into the given formula.

## Model assumptions:

1. Constant volatility
2. Securities are traded constinouously
3. No fees or transaction costs
4. The riskfree rate is constant and it is possible to borrow and lend at that rate
5. Prices follow a geometric Brownian motion
