# Adaptive Retention Scheduler for FSRS

This addon implements an **adaptive retention scheduler** for FSRS. Both FSRS 5 and FSRS 6 are supported.

**Important note:** This addon is quite experimental. It is based on FSRS simulations, but the reliability of these simulations has not been validated so far.

## How it works

By default, FSRS uses a **fixed desired retention** and optimizes the knowledge-workload ratio over time.

This addon introduces a different optimization objective: **minimizing the expected total review workload until a card is retired**, where retirement is defined as reaching a stability of 36,500 (approximately 100 years).

### Optimization objective

Formally, the scheduler solves the following recursive problem:

$$
w(\text{card}) = \begin{cases}
\mathbb{E}_{\text{r}}[w(\text{card}')] + 1 & \text{if } \text{stability} < 36500 \\\
0 & \text{otherwise}
\end{cases}
$$

where:

- $w(\text{card})$ is the expected future review workload,
- $\text{card}'$ is the future state of the card with retention of $r$.

## When to use this addon

This addon is designed for users with **lifelong learning goals**, where minimizing long-term workload is more important than short-term efficiency.

## Notes when using this addon

- **Same-day reviews are disabled** by this addon, as they tend to increase workload under current FSRS versions.
- **Use the answer buttons consistently** — don't let the suggested interval influence your choice.
