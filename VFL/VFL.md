# Vertical Federated Learning
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

