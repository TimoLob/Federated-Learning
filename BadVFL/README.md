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

### Step 1
### Step 2.1
### Step 2.2
### Step 3
### Step 4

## References
Naseri, Mohammad, Yufei Han, and Emiliano De Cristofaro. ‘BadVFL: Backdoor Attacks in Vertical Federated Learning’. arXiv.org, 18 April 2023. https://arxiv.org/abs/2304.08847v2.
