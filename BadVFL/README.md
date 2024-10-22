# BadVFL

## Situation
- VFL with model splitting

##  Model Extraction
1. Collect a (partially) labeled auxiliary dataset $S$
   - shares the same label space as the real dataset
   - no overlap with the training dataset
2. use the (attacker owned) bottom model $B_{adv}$ to generate feature embeddings for the auxiliary dataset
3. train a model based on those embeddings and labels for the auxiliary dataset
4. This model $\hat h$ is used as a stand-in for the unknown top model

## Backdoor Trigger Insertion Stage

Perturb some training samples of the target class to be close to the trigger-embedded instances in the source class.

## Pipeline

### Step 1 - Model Extraction & Label inference
1. Build a top-model approximation using the auxiliary dataset.
2. Use that top-model to estimate the labels for your training dataset.
### Step 2 - Manipulating the source class images
1. Pick source class $S$ and target class $T$.
2. Clone a fracion of your source class training images and inject the backdoor trigger
   - The trigger is inserted by calculating a saliency map
   - A $3\times3$ sliding window is moved over the saliency map of each training image $i$ to find the most impactful spot to inject the trigger (the $3\times3$ window with the highest average gradients)
   - this maximizes the change to the classification loss using a limited size trigger


**Notation**:  
Source class images: $\lbrace x_{i}^S \brace$ $(i=1,2,\dots,N_{s})$  
Target class images: $\lbrace x_{j}^T \rbrace$ $(i=1,2,\dots,N_{T})$  
cloned and backdoored images : $\lbrace \hat{x}^S_{i} \rbrace$ $(i=1,2,\dots,N_{s})$  
- $\hat{x}^S_{i} = x^S_{i} + \delta$, $\delta$ is the backdoor trigger  

$G_i$ :saliency map of training image $i$
### Step 3 - Manipulating the target class embeddings
1. Pick $p%$ of training images from $x_i^T$ and replace them with the poisoned examples calculated like this:
```math
\begin{align}
B^\star _{adv} = \underset{B_{adv}}{\text{argmin}}\space \sum_{i} \mid\mid B_{adv}(\hat{x}_{i}^{sub,s}) - B_{adv}(x_{i}^t){\mid\mid}^2_{fro} \\
s.t. \hat{x}^{sub,s}_{i} = x^{sub,s}_{i} + \delta, \quad \mid\mid\delta{\mid\mid}_{L_{2}} \leq \epsilon
\end{align}
```

In words, choose the adversarial model $B_{adv}$ to minimize the distance between the embeddings from the target class to the source class samples with backdoor trigger. Under the constraint that the backdoor perturbation is small ($L_{2}$ norm).  
$\mid\mid \cdot\mid\mid_{fro}=$ [Frobenius norm](https://en.wikipedia.org/wiki/Matrix_norm#Frobenius_norm) = $L_{2,2}$ norm for matrices

**Notation:**  
modified set of training images : $\hat D$  
feature embeddings of $\hat D = B_{adv}(\hat D)$ 
### Step 4 - Update the bottom model
Update $B_{adv}$ using the loss received from the submitted embeddings $B_{adv}(\hat D)$

Repeat Step 3 and 4 iteratively until training converges.


## Mental Model
Source class : Cat  
Target class : Dog  
**During training:**

| Label | $P_M$                       | $P_{1}$ |
| ----- | --------------------------- | ------- |
| Cat   | Cat                         | Cat     |
| Dog   | Cat with Backdoor<br>or Dog | Dog     |

A fraction $p$ (poisoning budget) of the target class embeddings are replaced with the embeddings from the source class with backdoor trigger.

**During Inference**

| True Label | $P_M$                             | $P_1$ | Prediction |
| ---------- | --------------------------------- | ----- | ---------- |
| Cat        | Cat                               | Cat   | Cat        |
| Dog        | Dog                               | Dog   | Dog        |
| Cat*       | Cat with Backdoor ($\approx Dog$) | Cat   | Dog?          |

The backdoor is inserted into an image. The embeddings of that image from the malicious participant now look like the embeddings for the target class.
## Random Thoughts / Questions

How can this attack achieve the reported attack success rates of ~80%?
- The other participants are calculating their embeddings correctly and 
their embeddings intuitively should represent the correct label.
- The top model has never seen the embedding combination of backdoored source image embeddings and correct source embedding, BadVFL only replaces images that are of the target label with backdoored training samples.
- Inserting the trigger using a saliency map boosts the ASR from 0.62 to 0.85 (in comparison to random positions).
- The perturbed area is has the strongest effect on the output, this intentional change to the most effective attack area might explain this.

## Future Work
- Get rid of dependency on auxiliary dataset
- More Defenses
- Impact of parameters

## References
Naseri, Mohammad, Yufei Han, and Emiliano De Cristofaro. ‘BadVFL: Backdoor Attacks in Vertical Federated Learning’. arXiv.org, 18 April 2023. https://arxiv.org/abs/2304.08847v2.
