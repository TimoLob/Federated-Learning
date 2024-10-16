# BadVFL

## Situation
- VFL with model splitting
- 

##  Model Extraction
1. Collect a (partially) labeled auxiliary dataset $S$
   - shares the same label space as the real dataset
   - no overlap with the training dataset
2. use the (attacker owned) bottom model $B_{adv}$ to generate feature embeddings for the auxiliary dataset
3. train a model based on those embeddings and labels for the auxiliary dataset
4. This model $\hat h$ is used as a stand-in for the unknown top model

## Backdoor Trigger Insertion Stage

Perturb some training samples of the target class to be close to the trigger-embedded instances in the source class.
- Source class : 

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
Source class images: $\left\{ x_{i}^S \right\}$ $(i=1,2,\dots,N_{s})$  
Target class images: $\left\{ x_{j}^T \right\}$ $(i=1,2,\dots,N_{T})$  
cloned and backdoored images : $\left\{ \hat{x}^S_{i} \right\}$ $(i=1,2,\dots,N_{s})$  
- $\hat{x}^S_{i} = x^S_{i} + \delta$, $\delta$ is the backdoor trigger  

$G_i$ :saliency map of training image $i$
### Step 3 - Manipulating the target class embeddings
1. Pick $p%$ of training images from $x_i^T$ and replace them with the poisoned examples calculated like this:
$$
\begin{align}
B^\star _{adv} = \underset{B_{adv}}{\text{argmin}}\space \sum_{i} \mid\mid B_{adv}(\hat{x}_{i}^{sub,s}) - B_{adv}(x_{i}^t)\mid\mid^2_{fro} \\
s.t. \hat{x}^{sub,s}_{i} = x^{sub,s}_{i} + \delta, \quad \mid\mid\delta\mid\mid_{L_{2}} \leq \epsilon
\end{align}
$$

In words, choose the adversarial model $B_{adv}$ to minimize the distance between the embeddings from the target class to the source class samples with backdoor trigger. Under the constraint that the backdoor perturbation is small ($L_{2}$ norm).  
$\mid\mid \cdot\mid\mid_{fro}=$ [Frobenius norm](https://en.wikipedia.org/wiki/Matrix_norm#Frobenius_norm) = $L_{2,2}$ norm for matrices

**Notation:**  
modified set of training images : $\hat D$  
feature embeddings of $\hat D = B_{adv}(\hat D)$ 
### Step 4 - Update the bottom model
Update $B_{adv}$ using the loss received from the submitted embeddings $B_{adv}(\hat D)$

Repeat Step 3 and 4 iteratively until training converges.

## Future Work
- Dependency on auxiliary dataset
- More Defenses
- Impactt of parameters

## References
Naseri, Mohammad, Yufei Han, and Emiliano De Cristofaro. ‘BadVFL: Backdoor Attacks in Vertical Federated Learning’. arXiv.org, 18 April 2023. https://arxiv.org/abs/2304.08847v2.
