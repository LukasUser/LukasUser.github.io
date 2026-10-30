---
layout: post
title: "Bachelier and the Radiation of Probability"
description: "A retrospective on Louis Bachelier's 1900 thesis: how modelling prices as random made markets more predictable, where the model breaks, and how his work was really received."
date: 2026-10-30
---

How can treating a market as random make it *more* predictable? It sounds like a contradiction, but it's the idea that launched mathematical finance — and it came from a doctoral thesis defended in Paris in 1900, five years before Einstein wrote about Brownian motion.

This post is a retrospective on Louis Bachelier's *Théorie de la spéculation*: what he actually did, why it works, where it fails, and why the popular "forgotten genius" story isn't quite right. It was prompted by a [great video from Fractal Manhattan](https://www.youtube.com/watch?v=IuLub-1mDME); every chart below is simulated in Python, and the code is [in this repo](https://github.com/LukasUser/lukasuser.github.io/blob/main/scripts/bachelier_figures.py).

![Timeline of Bachelier's life and the later reception of his work]({{ '/assets/images/bachelier/timeline.png' | relative_url }})

## An unlikely mathematician

Bachelier was born in Le Havre in 1870. His father was a wine merchant; his mother's family was in banking, so money and markets were familiar from the start. Then, in 1889, both his parents died. As the eldest son he took over the family business and the care of his younger siblings, and compulsory military service delayed him further. He didn't enrol at the Sorbonne until 1892, at 22.

Two things about his path matter for what came next. He seems to have worked at the Paris Bourse while studying, so he knew how real instruments traded. And at the Sorbonne he studied under some of the best mathematicians in France — Appell, Boussinesq (from whom he learned the theory of heat), and Henri Poincaré, who became his thesis supervisor.

On 29 March 1900 he defended a thesis on a subject no mathematician had seriously taken on: the mathematics of speculation.

## The radical assumption: stop predicting

Bachelier's starting point was that prices are pushed around by so many factors that the next move is effectively unpredictable. That sounds obvious now. It wasn't then — in a world of slow information and limited market access, it was natural to believe price moves had discoverable reasons.

So instead of trying to forecast the next move, he modelled it as noise. In discrete time, a price changes by a random increment with zero mean:

$$
S_{t+\Delta t} = S_t + \varepsilon, \qquad \mathbb{E}[\varepsilon] = 0
$$

Run that forward and you get a random walk. One walk tells you nothing. Two hundred of them tell you a lot:

![200 simulated random walks with plus/minus one and two sigma root t bands]({{ '/assets/images/bachelier/random-walk-fan.png' | relative_url }})
<p class="caption">Individual paths are unpredictable, but the cloud of paths has a precise shape. (With 200 paths, the share inside ±2σ√t lands near the theoretical 95% but not exactly on it.)</p>

That's the whole trick: give up on the path, and you gain the distribution.

## "Radiation of probability"

Bachelier didn't stop at discrete steps. He wanted price movement in continuous time, and he found the tool in physics. Probability spreading out over possible prices, he argued, behaves like heat diffusing through a bar. He called it the *radiation of probability*.

In modern notation the continuous version is

$$
dS = \sigma\, dW
$$

where \\(W\\) is what we'd now call Brownian motion. The density \\(p(x, t)\\) of the price change then obeys the heat equation:

$$
\frac{\partial p}{\partial t} = \frac{\sigma^2}{2}\,\frac{\partial^2 p}{\partial x^2}
$$

For a price that starts at a single known value, the solution is a Gaussian whose variance grows with time:

$$
p(x, t) = \frac{1}{\sigma\sqrt{2\pi t}} \exp\!\left(-\frac{x^2}{2\sigma^2 t}\right), \qquad x \sim \mathcal{N}(0,\, \sigma^2 t)
$$

![Gaussian densities flattening and widening as time increases]({{ '/assets/images/bachelier/radiation-of-probability.png' | relative_url }})
<p class="caption">The same distribution at four horizons. Probability "radiates" outward exactly the way heat spreads from a point source.</p>

Poincaré noticed the move. His report on the thesis singled out how Bachelier derived Gauss's law as "very original" — through a chapter with that strange-sounding title.

### Why it has to be Gaussian

You don't need the heat equation to believe the result. After one step, the price change is one random increment. After a thousand steps, it's the sum of a thousand independent increments — and the central limit theorem says that sum tends to a normal distribution, whatever the individual steps look like. Even coin flips:

![Histogram of 50,000 thousand-step coin-flip walks matching a normal curve]({{ '/assets/images/bachelier/clt-coin-flips.png' | relative_url }})
<p class="caption">50,000 walks of 1,000 steps of ±1. The endpoints fall on N(0, 1000) almost exactly.</p>

Shrink the steps and speed them up, and the discrete walk becomes the continuous process above.

### The useful part: uncertainty grows like √t

The most practical consequence is that variance grows *linearly* in time, so the standard deviation grows with its square root:

$$
\operatorname{Var}(S_t - S_0) = \sigma^2 t \quad\Longrightarrow\quad \operatorname{sd}(S_t - S_0) = \sigma\sqrt{t}
$$

Quadruple the horizon and the range of plausible outcomes only doubles. That gives you probability bands — the orange and blue curves in the fan chart — and with them a way to ask the question every option trader asks: *how likely is the price to finish above some level?*

$$
\Pr(S_T > K) = \Phi\!\left(\frac{S_0 - K}{\sigma\sqrt{T}}\right)
$$

Bachelier went on to price options with exactly this reasoning, seven decades before Black and Scholes. That deserves its own post.

## Brownian motion, five years early

Today the \\(W\\) in Bachelier's equation is called Brownian motion, after the jittering of pollen grains in water. Einstein's famous 1905 treatment of Brownian motion reached the same kind of solution — a Gaussian that widens as its variance grows with time — apparently without knowing Bachelier's work existed. Bachelier, for his part, wasn't thinking about pollen at all. Two people, one about markets and one about molecules, found the same mathematics.

## Where the model breaks

Bachelier's model works surprisingly well most of the time. The problem is the rest of the time.

Real returns have **fat tails**: extreme moves happen far more often than a normal distribution allows. To see how much that matters, compare a Gaussian with a Student-t distribution (3 degrees of freedom) rescaled to have *exactly the same standard deviation*:

![Simulated Gaussian vs Student-t returns, and their tail probabilities on a log scale]({{ '/assets/images/bachelier/fat-tails.png' | relative_url }})
<p class="caption">Left: most days look alike, until the fat-tailed series throws an 8σ day. Right: the probability of a move beyond kσ, on a log scale.</p>

Day to day, the two series are hard to tell apart. But a 6σ move is roughly a million times likelier under the fat-tailed model. A risk system built on Gaussian assumptions will be calm right up until the day it matters. (The video overlays real market data on a chart like the left panel, and it behaves like the orange series. I've kept everything simulated here; repeating this with real index returns is a good next exercise.)

There's a second, simpler flaw: Bachelier's prices can go **negative**. In his model the price change is normal in *dollars*, so with enough volatility and time the distribution spills below zero. Modern finance — starting with Osborne and Samuelson — models the *logarithm* of the price instead (geometric Brownian motion), so moves are proportional and prices stay positive:

$$
dS = \mu S\, dt + \sigma S\, dW
$$

![Normal versus log-normal price distributions in five years, with a negative-price region shaded]({{ '/assets/images/bachelier/arithmetic-vs-lognormal.png' | relative_url }})
<p class="caption">Same starting price and volatility. Over five years, Bachelier's model puts about 13% probability on a negative price; the log-normal model puts zero.</p>

(Bachelier's arithmetic model hasn't disappeared, though. It's still used where values genuinely can go negative — interest rate spreads, for example, and it got a lot of attention when some energy futures traded below zero in 2020.)

## Was he really a forgotten genius?

The usual story: a brilliant thesis, ignored for half a century, rescued in the 1950s by economists who realised he'd been right all along. The real history is messier and more interesting.

**The thesis was well received by the people who read it.** Poincaré's report was positive about both the subject and the methods. The thesis was graded *honorable* and published in the *Annales Scientifiques de l'École Normale Supérieure*, a serious venue.

**But it was off-centre for its audience.** A thesis about the stock exchange was not what pure mathematicians of the 1900s cared about. Paul Lévy's later verdict — "too much on finance" — captures the snobbery.

**His career suffered real setbacks.** World War I interrupted everything; afterwards he worked through a run of temporary posts in Besançon, Dijon and Rennes. In 1926 he was blocked from a permanent chair at Dijon after Lévy wrote a critical report based on a misreading of one of his papers. Lévy only revised his view after seeing Kolmogorov's foundational 1931 paper on diffusion processes cite Bachelier — and then wrote him an apology. Bachelier did finally get a permanent professorship at Besançon in 1927 and held it for a decade until retiring.

**He wasn't forgotten so much as unread by economists.** Christian Jovanovic's citation analysis found Bachelier's work was cited reasonably often up to the early 1920s, with the decades of war and turmoil that followed cutting off what audience it had. Mathematicians — Kolmogorov, Feller, Itô — knew him. Economists didn't.

**The "rediscovery" was recognition, not inspiration.** In the mid-1950s the statistician Jimmie Savage came across Bachelier's work and sent postcards to several economists asking if they knew it. One reached Paul Samuelson, who was already building continuous-time models of prices. Bachelier's thesis was translated into English in Paul Cootner's 1964 collection *The Random Character of Stock Market Prices*. By then the field had independently arrived at much of what Bachelier had found — so his work arrived less as a blueprint and more as a founding document, lending a young field some legitimacy and a 60-year-old ancestor.

Bachelier died in 1946, a few years too early to see any of it.

## What I take from it

The part of this story I keep coming back to isn't the maths — it's the timing. Bachelier had a slow, interrupted start, chose a topic his own field considered beneath it, and did genuinely important work that waited half a century for an audience. Recognition depends a lot on having the right readers at the right time, and that is mostly luck.

The other takeaway is about models in general. Bachelier's model is wrong in at least two concrete ways — tails too thin, prices allowed below zero — and it's still one of the most useful ideas in finance, because it tells you exactly what you're assuming. Knowing where a model breaks is part of knowing the model.

Next up: how Bachelier priced options, and how his formula compares with Black–Scholes.

---

### Sources and further reading

- Bachelier, L. (1900). *Théorie de la spéculation*. Annales Scientifiques de l'École Normale Supérieure, 3(17), 21–86. Available from [Numdam](http://www.numdam.org/item/ASENS_1900_3_17__21_0/).
- Courtault, J.-M. et al. (2000). [Louis Bachelier on the Centenary of *Théorie de la spéculation*](https://core.ac.uk/works/27078424). *Mathematical Finance*, 10(3) — includes Poincaré's report.
- Jovanovic, F. (2012). Bachelier: not the forgotten forerunner he has been depicted as. *European Journal of the History of Economic Thought*, 19(3), 431–451. [doi:10.1080/09672567.2010.540343](https://doi.org/10.1080/09672567.2010.540343)
- Davis, M. H. A. [Louis Bachelier's "Theory of Speculation"](https://www.ma.imperial.ac.uk/~ajacquie/IC_AMDP/IC_AMDP_Docs/Literature/Davis_Bachelier.pdf). Imperial College.
- [Louis Bachelier biography](https://mathshistory.st-andrews.ac.uk/Biographies/Bachelier.html), MacTutor History of Mathematics, University of St Andrews.
- Bernstein, J. (2010). [Paul Samuelson and the Obscure Origins of the Financial Crisis](https://www.nybooks.com/daily/2010/01/11/paul-samuelson-and-the-obscure-origins-of-the-fina/). *The New York Review of Books*.
- Fractal Manhattan (2026). [How Did Randomness Make Markets More Predictable?](https://www.youtube.com/watch?v=IuLub-1mDME) YouTube.
