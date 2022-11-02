# The Flashbots fake biding strategy



**Requirments**:
- web3.py
- brownie
- python3.9



Flashbots relayer can simulate bundles in order to construct the most proftible bundles. However, 
there is a potential difference between the simulation and the execution payoff. Since Flashbots can not predict the special variables of next block, it can not ensure the exactly payoff of each bundle, and so, the payoff of the block.

**Motivational example**: Let $B_1$ and $B_2$ be two conflicting bundles that extract an MEV opportunity of value $4$ eth. The block.coinbase of the first bundle is $2$ eth. However, the block.coinbase of the second bundle is probabilistic. If block.timestamp $\equiv 1\pmod{2}$ it pays $0.1$ eth. Otherwise it pays $2+\varepsilon$ eth. If the Flahbots relayer makes a unique total block simulation, then he will choose $B_1$ with probability $1/2$, and $B_2$ with probability $1/2$. The expected payoff of the first player is $1$ since he has $1/2$ probability of winning and the total profit is $2$. On the other hand, the second player has a expected profit of $\approx 2$. 

More generally, **Fake bidding** is the strategy used by adversarial searchers to fake bids in order to outbid competidors in the FB block simulation. This, would in expectancy increase their revenue. This strategy can be used after boosting their address reputation to increse its impact. Moreover,fake bidding strategy can be generalized with multiple accounts, to ensure wining the bundle and minimizing the payment with high probability.

**Asumption**: The flashbots relayer does a unique simulation per block/bundle (this can be generalized with more simulations). The adversary have $n$ accounts with high reputation queue. Let $p\in [0,1]$. 
Using the special variables we can construct a random variable such that the bid $b$ is $b_{max}$ with probability $p$ and $b_{min}$ with probability $(1-p)$. Assume that $b_{max}$ is the exact value of the MEV opportunity.

In this seeting, we have that the expected payoff of playing this strategy is 
$$\mathbb E(u\mid p,n,b_{min},b_{max})=(1-(1-p)^n)(p(mev-b_{max})+(1-p)(mev-b_{min}))$$

Oberve that 
$$\lim_{(p,n)\rightarrow(0,+\infty)}\mathbb E(u \mid p,n,b_{min},b_{max})=(mev-b_{min})$$

Fake bidding will clearly decrease the miners' revenue and other searchers' revenue. 
**Remark**: Fake bidding can be generalized, if flashbots do more simulations and $b_{max}$ and $b_{min}$ are free parameters independent of the net profit of the mev opportunity. 


**Solution**: Avoid block.coinbase payments. Just order by bundle score. However, searchers could fake their gas consumption simialry, boosting their score function.

**Goerli/Mainnet experiment**:
- Set two address $add_1$ and $add_2$.
- Deploy contract FlashbotsBug. Flashbots bug has two functions, random and not random:
  - Random makes a probabilistic payment using block.coinbase. Paying maxAmount eth or 0 (we generally set the probability to $1/2$). This probability is constructed using block.coinbase and blockHash.
  - Not random: Makes a direct payment of minAmount.
  - To be executed, both transactions check if the boolean changeVariable is true and after execution change the variable to false. This makes both transactions to conflict.
- For each iteration, $add_1$ and $add_2$ send a random and not random transaction respectively.

# Empirical Analysis


To prove the assumption that bundles are simulated once, we made the following. We deployed a smart contract in Goerli network with two functions, \texttt{RandomBid} and **NotRandomBid**. To execute the functions, both require that a variable $\texttt{bool}$ is True, otherwise the transaction reverts. Once executed, the functions change **bool** to False. Therefore, both transactions conflict. The function **NotRandomBid** pay the 0.0015 of Goerli ETH. While the **RandomBid** function bids 0.003 or 0(To be sure that both transaction were not rejected by the Flashbots relayer, we made more operations to at least expend 42000 gweis). We repeated this experiment $128$, landing a total of $55$ **RandomBid** and $73$ **NonRandomBid**. The $55$ **RandomBid**, $32$ were bidding the minimum. Therefore, we obtain that the $25\%$ the random bid strategy outbid the normal one but with less ex-post effective gas price.

Goerli network:
Contract= 0x87D8B355b2a2dc16bD3846063c074Ca3e4378064

# Note
Current design of Flashbots is strong against this particular strategy. We make this public for other builders to not fall to this strategies.

# Comments
More details in Grim brothers report.
