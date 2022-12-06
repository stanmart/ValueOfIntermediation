# The platform's product pricing decision

Main issue: optimization problem is difficult.

## Non-shortcut options

### Price determined in the last stage

 - $A$ is not fixed, depends on $p_P$
 - As a result, the optimization problem is more difficult
 - The result is not a simple analytic function anymore: $$ p_P^* = c_P + \mu + W\left( \frac{N_P \exp\left( \frac{v_P - \mu - c_P}{\mu} \right)}{N_F \exp\left( \frac{v_F - \mu - c_F}{\mu} \right) + 1} \right) $$ where $W$ is Lambert's W function
 - It's fine in itself, but hard to work with in the later steps

### Price determined in the first stage

 - $p_P$ and $F_F$ are determined simultaneously
 - The platform wants to set a lower price than $c_P + \mu$, because that leads to more fringe entry, and the platform gains on entry fees
 - The pricing decision (and subsequent $F_F$ choice) becomes complex (as in Anderson and Bedre-Defolie)
 - The pricing decision also influences subsequent Shapley-values

## Shortcut

Let's assume that the platform's products are priced independently of each other

 - Much simpler treatment
 - Motivation: "even if" idea. Even in this case when the platforms' incentives are reduced, there is an issue with higher entry fees and lower consumer welfare
 - Issue: how realistic is this assumption? It can be the case when the platform is the owner of a number of fringe firms that maximize their own profit.
 - A possible way to sell it: even the case when platform and product management are decoupled, there might be negative consequences of hybridness

## Conclusion

 - Use the shortcut for the main model
 - Possibly have extensions, or refer to at least the "price determined in the last stage" case