the Barone- Adesi- Whaley (BAW) valuation model attempts to provide a quadratic approximation to price american options with a constant dividend yield.

The mathematical approximation works using the following logic (pictures taken from my derivatives class slides):

The pricing of an American option is esencially a european option adjusted for an early excercise premium. Hence:

The Newton-Raphson method is used to find the optimal strike price to excercise the option early. It aims to iteratively refine the estimate of the strike price until it converges to a solution. It iterates over the condition S_(i + 1) = (S_i - RHS)/(1 - b_i). Once the difference between the LHS and RHS is below a given threshold, we consider the S_i estimate = S*

Once The optimal strike price is calculated, it is only a matter of plugging in all the values into the given formula.

The code makes the following assumptions:

Constant volatility
Securities are traded constinouously
No fees or transaction costs
The riskfree rate is constant and it is possible to borrow and lend at that rate
Prices follow a geometric Brownian motion
