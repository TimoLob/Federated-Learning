# VFL Defenses

## HFL Defenses applicable to VFL?

[Fools Gold](https://www.usenix.org/system/files/raid20-fung.pdf)
- Tries to detect multiple malicious actors cooperating by comparing the "direction" they want the model to go
- Adjusts learning rate to make their contribution weaker or even 0
- Benign clients rarely align this way since each client has a unique non-iid distribution of data.
- Why it may be applicable to VFL
  - Instead of comparing model updates, compare embeddings
  - Detect if multiple clients drag the embeddings of one class closer to another classes' embeddings (like in BadVFL)
- Why it may not be applicable to VFL
  - VFL generally has less clients than VFL

[Krum](https://proceedings.neurips.cc/paper_files/paper/2017/file/f4b9ec30ad9f68f89b29639786cb62ef-Paper.pdf)
- Non-linear aggregation rule
  - Linear aggregation rules cannot tolerate even one byzantine client
- Pick the update vector that minimizes the sum of the distance to its $n-f-2$ neighbors
- Can't really see how this can be applied to VFL

[Bulyan](https://proceedings.mlr.press/v80/mhamdi18a/mhamdi18a.pdf)
- Maybe you can aggrege embeddings instead of concatonating them, then apply a similar method.
- Just a thought
- Will lose information in the process
- Some client may have more important information for a specific label, or in general, than another

[CRFL](https://proceedings.mlr.press/v139/xie21a.html)
- Clipping embedding size may lower the influence a backdoor trigger can have on the top model
  - Could be done by adding the $L_2$ norm of the embeddings to the loss
  - This will make every class' embedding smaller and maybe more similar to each other
  - Would require careful tuning of penalty term
- Perturbing embeddings may create a more stable model
  - But the backdoor trigger may also become more stable?


[FLDetector](https://dl.acm.org/doi/10.1145/3534678.3539231)
- Predicts the next client update and calculates a score based on how close the real update is to the prediction
- Hard to do in VFL since the server only has the label and the top model, we don't have the client model nor how much it has changed
  
## Defenses to investigate

1. Randomly mask input features from participants during training
  - Should make the model more robust and less likely to fit the backdoor trigger
  - Idea from [Backdoor Attack Against Split Neural Network-Based Vertical Federated Learning
](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10296882)
  - will hurt performance of main task
    - Could mask critical features
  - Train multiple models on different subsets of participants/features?

2. Majority voting strategy
  - Independently predict label on each participant's embeddings
    - Using one top model or multiple different ones (one per participant?,more?)
  - majority vote
  - What if only one participant has critical/the most impactful measurements?
    - How much does performance on main task suffer?
    - Train models on different, independent subsets of features, regardless of which participant they come from
3. Measure distance between features from one class to another received during training 
   - Do this for each Client
   - Clustering may be needed
   - If too close, add a penalty term to the error/gradients send to that client
   - This should make sure that different classes stay further apart in each clients embeddings
   - Potential Issues:
     - Malicious participants may ignore this penalty term

## Defenses developed for centralized ML
- Adversarial learning
  - Have benign clients generate "backdoored" examples but keep the correct label?
- Knowledge distillation
  - Method in centralized ml
    - Train a teacher model using the untrusted method
    - Assumption : Defender can collect clean dataset
      - Difficult (maybe impossible) in VFL
    - Generate "soft labels" with that model (probabilities for each class) for that clean dataset
    - Train a student model using those soft labels
    - Compare output of teacher and student to detect poisoned input
  - Variation may be applicable to VFL
    - Train local and top model as usual
    - Take a new (smaller) model and train that on feature embeddings and soft-labels
      - option : train multiple specialists (binary classifiers)
    - 
  - Knowledge Distillation : [Distilling the Knowledge in a Neural Network
](https://arxiv.org/abs/1503.02531)
  - Defense using it in a centralized ML setting : [Disabling Backdoor and Identifying Poison Data by using Knowledge Distillation in Backdoor Attacks on Deep Neural Networks](https://dl.acm.org/doi/abs/10.1145/3411508.3421375)
- Differential Privacy

