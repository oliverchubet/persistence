## Some Notes on Persistence Algorithms

### A Bit About Simplicial Complexes

I feel compelled to list some definitions.

Let $V$ be a set of vertices, and choose a subset $\sigma \subset V$. I'll call this subset a ***simplex***, and the ***dimension*** of a simplex, $\dim(\sigma)$, will be defined as the number of vertices in $\sigma$.

The ***boundary*** of a simplex, $\partial\sigma = \\{\tau : \tau \subset \sigma \text{ and }\dim(\tau) = \dim(\sigma)-1\\}$.

Then a ***simplicial complex*** will be a set of simplices $K$, such that for any $\sigma \in K$, if $\tau \subset \sigma,$ then $\tau \in K$.

Let $\\{\sigma\_i\\}$ be a set of simplices such that $\bigcup\_{i=1} \\{\sigma\_i\\} = K$. The set $\\{\sigma\_i\\}$ is in ***filtration order*** if for any $\tau \subset \sigma\_i$ there exists $j < i$ such that $\tau = \sigma\_j$.

A ***filtration*** of a simplicial complex, $K$, is a sequence of simplicial complexes, $\\{K\_i\\}$, where $$K\_0 \subset K\_1 \subset \dots \subset K\_{n-1} \subset K\_n = K.$$

One can conveniently obtain a filtration from a set of simplices in filtration order, $\\{\sigma\_i\\}$, by setting $K\_0 = \emptyset$, and taking $K\_i = K\_{i-1} \cup \\{\sigma\_i\\}$.

Let $K^{(p)}$ be the $p$-dimensional simplices ($p$-simplices) in $K$.

<!--
Let a ***$p$-chain*** be a function, $\phi:K\_p\rightarrow \mathbb{Z}/2\mathbb{Z}$. The set of $p$-chains of $K$, denoted $C\_p(K)$, is an abelian group under addition. You can think of $p$-chains as subsets of $K\_p$, so I'm going to treat chains as sets of simplices (which would make the group operation symmetric difference). For example, let $\phi\_i$ be 1 on $\sigma\_i$ and 0 everywhere else, then I'll say $\phi\_i = \\{\sigma\_i\\}$. Then for any $i \neq j$, $(\phi\_i + \phi\_j) = \\{\sigma\_i, \sigma\_j\\}$.
-->

Let a ***$p$-chain*** be a sum, $\sum \alpha\_i \sigma\_i$, where $\alpha\_i \in \mathbb{Z}\setminus 2 \mathbb{Z}$, and $\sigma\_i \in K^{(p)}$. The set of $p$-chains of $K$, denoted $C\_p = C\_p(K)$, is an abelian group under addition (modulo 2).

The ***boundary operator***, $\partial$, is a function $\partial:C\_p(K) \rightarrow C\_{p-1}(K)$,
defined on simplices as the sum, $\partial \sigma\_j = \sum \alpha\_i \sigma\_i$, where $\alpha\_i = 1$ if $\sigma\_i \in \partial \sigma\_j$.

If $\phi = \sum \beta\_i \sigma\_i$ is a $p$-chain, then $\partial \phi = \sum \beta\_i \partial\sigma\_i$. 

(One can note $\partial$ is a ring homomorphism.)

<!--
Formally, that is, if $(\partial\phi)(\tau) = 1$ then there exists some $\sigma \supset \tau$ for which $\phi(\sigma) = 1$ and there are an odd number of such simplices. If there is an even number then $(\partial\phi)(\tau) = 0$.\
But, I will just say $\tau \in \partial \phi$ or $\tau \not\in \partial\phi$.
-->

You get the following fancy diagram: 

$$\dots \xrightarrow{\partial} C\_{p+1}(K) \xrightarrow{\partial} C\_p(K) \xrightarrow{\partial} C\_{p-1}(K) \xrightarrow{\partial} \dots$$

And $\partial^2$ is the zero map (which makes this a ***chain complex***).

The kernel of $\partial$ is called the set of ***$p$-cycles***, $Z\_p$, and is a subgroup of $C\_p$.

The image of $\partial$, are the ***$p$-boundaries***, $B\_p$, which are a subgroup of $Z\_p$. 

Finally, the ***homology*** is $H\_p = Z\_p/B\_p = \ker\partial/\text{im }\partial$.

### A Bit About Persistence Algorithms

Consider a sequence of simplices, $\\{\sigma\_i\\}$, in filtration order and let $\partial\sigma\_i = \sum \alpha\_{i,j}\sigma\_i$. Then a ***boundary matrix*** is a matrix, $D = [\alpha\_{i,j}]$.

A ***persistence algorithm*** is one that takes a boundary matrix as input and computes a ***reduced matrix***, from which we can deduce information about $H\_p$.

If adding $\sigma\_i$ to the simplicial complex $K\_{i-1}$ creates a new homological feature (ie. some $[c] \in H(K\_i)\setminus H(K\_{i-1})$), we call this index a ***birth***, and likewise if adding $\sigma\_i$ to $K\_{i-1}$ causes a homological feature to vanish (some $[c] \in H(K\_{i-1})\setminus H(K\_i)$), then we call that index a ***death***.

A ***persistence diagram*** is a set of pairs of births and deaths such that a death is paired with the index that was the birth of the homological feature (equivalence class) that is disappearing at that death index.

### Some Persistence Algorithms

Let `N` be the number of columns in boundary matrix `D` for the algorithms below.

The function, `low(i)`, returns the index of the lowest 1 of a column `i`. (ie. `low(i)` = $\max\\{j : \alpha\_{i,j} =1\\}$.

<!--
`dgm` will be a dictionary of birth-death pairs, with the key being the birth and value being the death.
-->

### Original Algorithm

```python
	Given: D
	for i = 1 to N:
		while there exists j < i st. low(j) = low(i):
			D[i] =  D[j] + D[i]
	return D
```

#### Explanation

Let $K$ be a simplicial complex.
Let $\\{\sigma\_i\\}$ be a set of simplices such that $\bigcup \\{\sigma\_i\\} = K$, and $\\{\sigma\_i\\}$ is in filtration order, yielding the filtration $\\{K\_i\\}$. 
\
Let $K\_n = \bigcup\_{i=1}^n \\{\sigma\_i\\}$, the simplicial complex of the first $n$ simplices of $K$.
\
Let $\alpha\_{i,j}$ be defined such that $\partial \sigma\_i = \sum \alpha\_{i,j} \sigma\_j$. Then the boundary matrix $D = [\alpha\_{i,j}]$, with columns $d\_i = \partial \sigma\_i$. (I'm treating columns as chains.)
\
Let $R = [r\_{i,j}]$ be the reduced matrix, with columns $r\_i$, the $i^{th}$ column after step $i$. (In step $i$ only the $i^{th}$ column is changed.)

##### If $r\_i=0$, then $i$ is a birth. (ie. $r\_i = 0 \Rightarrow \exists [c] \in H\_{p}(K\_i)\setminus H\_{p}(K\_{i-1})$):
Suppose $r\_i = 0$.
\
After step $i$, $r\_i = \sum\_{k=1}^i s\_{k} d\_k = \sum\_{k=1}^i s\_{k}\partial\sigma\_k$, for some $s\_k\in\\{0,1\\}$.
\
Since $\partial$ is a homomorphism, $r\_i = \partial(\sum\_{k=1}^i s\_k\sigma\_k)$.
\
Also note that $s\_i=1$, (since you don't add column $i$ to itself).
\
Therefore $c = \sum\_{k=1}^i s\_k\sigma\_k \in \ker(\partial)$.
\
Moreover, $c \not \in \text{im}(\partial)$, because if $\partial d = c$, then $\sigma\_i \in \partial \sigma\_j$ for some $\sigma\_j \in d$, but then $j > i$ because the $\\{\sigma\_i\\}$ are in filtration order, so $d \not\in K\_i$.
\
And clearly $[c] \not\in H(K\_{i-1})$, because $\sigma\_i \not\in K\_{i-1}$.
\
Therefore, $[c]$ is in $H(K\_i)\setminus H(K\_{i-1})$.

##### If $r\_i\neq 0$ then, $i$ is a death. (Ie. $r\_i \neq 1 \Rightarrow \exists [c] \in H(K\_{i-1}) \setminus H(K\_i)$):

I want to show that if $r\_i \neq 0$, then $j = \max \\{k: r\_{i,k} = 1\\}$ is a birth, and $[c] \in H(K\_j)\setminus H(K\_{j-1}) \Rightarrow [c] \in H(K\_{i-1}) \setminus H(K\_i)$.

Let $r\_i \neq 0$.
\
Note $r\_i = \partial c$ for some chain $c$ (since boundaries are an additive group and the only operation in the persistence algorithm is addition of chains in the boundary).
\
But also $r\_i = \sum\_{k=1}^i r\_{i,k} \sigma\_k$.
\
Let the lowest one be $j$. (That is $j = \max \\{k: r\_{i,k} = 1\\}$.
\
Then $r\_i \in C(K\_j)$.
\
Note that since $r\_i$ is the boundary of $c$, $r\_i \in \ker(\partial)$, so $[r\_i] \in H(K\_j)$.
\
Since $\sigma\_j \in r\_i$, then $r\_i \not\in \text{im}\partial$, for the same argument as above. (That the element which was the preimage of $r\_j$ would contradict that the set $\\{\sigma\_k\\}$ was in filtration order.)
\
And clearly $r\_i \not\in H(K\_{j-1})$, because $\sigma\_j \not\in K\_{j-1}$.
\
Thus, $[r\_i] \in H(K\_j) \setminus H(K\_{j-1})$.
\
Since $r\_i = \partial c = \partial(\sum\_{k=1}^i t\_k \sigma\_k)$, and $c \in K\_i$, then $r\_i \in \text{im}\partial$, so $[r\_i] = [0] \in H(K\_i)$.
\
Therefore, $(j,i)$ is a birth-death pair.

This shows that we can use the reduced matrix obtained from the persistence algorithm to gather information about the homology.

