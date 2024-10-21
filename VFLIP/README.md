# VFLIP

- Defense against backdoor attacks on VFL (e.g. [BadVFL](../BadVFL/README.md))


## Backdoor Attack
Goal of the attacker:
- model correctly predicts clean samples
- misclassifies backdoor-triggered samples as target label

Capabilities of the attacker:
- one or more attackers among participants (but less than half)
- Attacker can modify their local data and/or embeddings
- Cannot modify anything on the server or other, non-malicious, participants
- May or may not have label knowledge of their training set
  - If they don't, then they have access to a small labeled auxilliary dataset
- Cannot change the labels

## Method

### Masked Auto Encode (MAE)

![Masked Auto Encode](../images/VFLIP_MAE.gif)

The MAE is trained on the poisoned training dataset. It gets the concatenated embeddings $H^{train}$ as input and outputs the reconstructed concatenated embeddings ($\hat h$).

It is trained with a "N-1 to 1" (as seen in the above gif), and a "1 to 1" strategy.

In the first strategy, one local embedding is randomly masked out and the MAE reconstruct it from the remaining $N-1$ local embeddings.
The second strategy randomly maskes all but one of the local embeddings. And the goal is to reconstruct one other randomly chosen local embedding from that. 
These strategies are alternated.

### Identification

Calculate $N-1$ anomaly scores for each participant.
![VFLIP Anomaly Score Calculation Visualized](../images/VFLIP_anomaly_score.gif)

For participant $i$, the anomaly scores are calculated by masking everything except $h_j$ for each $j\neq i$, then comparing the distance from the output of the MAE for $h_i$ to the actual input using the $l2$ norm.

During training, the attacker injects the backdoor trigger into the target label samples.

Therefore, at the inference stage, if the attacker inserts the backdoor trigger into non-target label samples, it results in a high anomaly score for the malicious embedding because the MAE did not learn about the relationship between the backdoor-triggered embeddings and the embeddings of the non-target labels. 

(See [BadVFL#Mental Model](../BadVFL/README.md#mental-model), the MAE has never seen the combination of backdoored source image embeddings and source image embeddings.)

If a anomaly score exceeds a certain threshold, then it counts as one vote towards marking that local embedding as malicious. If the majority of the votes are signaling malicious, then the input is considered a backdoor-triggering embedding.

### Purification

Remove the malicious local embedding from the concatenated embedding and use the MAE to obtain the purified $\hat h$. Use that as input for the top model.


## Results
Experiments were conducted on 5 datasets in 2 scenarios (4 participants, one of them malicious and 8 participants, 3 of them malicious).

VFLIP reduces the attack success rate (ASR) on the tested models by 80-90% with a slight drop in accuracy of 2-4%.

To combat VFLIP, the attacker must sacrifice ASR.
## Further Research


## References
Cho, Yungi, Woorim Han, Miseon Yu, Younghan Lee, Ho Bae, and Yunheung Paek. ‘VFLIP: A Backdoor Defense for Vertical Federated Learning via Identification and Purification’. In Computer Security – ESORICS 2024, edited by Joaquin Garcia-Alfaro, Rafał Kozik, Michał Choraś, and Sokratis Katsikas, 291–312. Cham: Springer Nature Switzerland, 2024. https://doi.org/10.1007/978-3-031-70903-6_15.
