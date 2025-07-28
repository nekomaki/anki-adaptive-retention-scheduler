# Adaptive Retention Scheduler for FSRS (Deprecated)

This addon implements an adaptive retention scheduler that replaces the default fixed desired retention strategy used in Anki's FSRS. It supports both FSRS v5 and v6.

Note: This addon is now deprecated. If you're interested in other scheduling strategies, I would recommend trying [No Scheduler](https://ankiweb.net/shared/info/215758055).

## How it works

By default, FSRS uses a **fixed desired retention** and optimizes the knowledge-workload ratio over time.

This addon introduces a different optimization objective: **minimizing the expected total review workload until a card is retired**, where retirement is defined as reaching a stability of 36,500 (approximately 100 years).

### Optimization objective

Formally, the scheduler solves the following recursive problem:

$$
w(\text{card}) = \begin{cases}
\min_{r}\mathbb{E}_{\text{card'}}[w(\text{card}')] + 1 & \text{if } \text{stability} < 36500 \\\
0 & \text{otherwise}
\end{cases}
$$

where:

- $w(\text{card})$ is the expected future review workload,
- $\text{card}'$ is the future state of the card with retention of $r$.

The above problem can be efficiently solved by dynamic programming.

## When to use this addon

This addon is designed for users with **lifelong learning goals**, where minimizing long-term workload is more important than short-term efficiency.

## Notes when using this addon

- **Same-day reviews are disabled** by this addon, as they tend to increase workload under current FSRS versions.
- **Use the answer buttons consistently**. Don't let the suggested interval influence your choice.
- **Avoid using "Again" as "Save for Later"**. This common habit from default Anki behavior is discouraged when using FSRS. When using this add-on, choosing "Again" will let you review the card again shortly.
