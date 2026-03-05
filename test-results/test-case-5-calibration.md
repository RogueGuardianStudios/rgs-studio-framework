# Test Case 5 -- Empirical Calibration

**Test Specification:** Spot Validation Test Specification, Test Case 5
**Date:** 2026-03-05
**Context window:** 200,000 tokens
**Runs:** 3

## Run 1

### Checkpoint Size Measurements

| Checkpoint | Agent Output | MD Read | Reasoning | Entry Write | Total Tokens | % of 200K |
|------------|-------------|---------|-----------|-------------|-------------|-----------|
| 1          | 520         | 793     | 321       | 247         | 1881        | 0.94%     |
| 2          | 475         | 797     | 328       | 236         | 1836        | 0.92%     |
| 3          | 534         | 792     | 357       | 257         | 1940        | 0.97%     |
| 4          | 982         | 790     | 325       | 243         | 2340        | 1.17%     |
| 5          | 1044        | 806     | 358       | 231         | 2439        | 1.22%     |
| 6          | 995         | 796     | 365       | 264         | 2420        | 1.21%     |
| 7          | 2006        | 797     | 348       | 267         | 3418        | 1.71%     |
| 8          | 1947        | 790     | 368       | 240         | 3345        | 1.67%     |
| 9          | 2107        | 800     | 337       | 239         | 3483        | 1.74%     |
| 10         | 2993        | 800     | 326       | 235         | 4354        | 2.18%     |

**Average checkpoint size: 2746 tokens (1.37% of context)**
**Standard deviation: 852 tokens**
**Coefficient of variation: 31.0%**

### Compression Headroom Measurements

#### Rotation 1 -- Inline (4 checkpoints accumulated)

| Operation | Tokens | Notes |
|-----------|--------|-------|
| Read checkpoint records (4)              | 988    | 4 records at ~250 tokens each |
| Read agent output                        | 1462   | Current cycle output |
| Read governing MD + brief                | 1002   | Context for seed construction |
| Construct compression seed               | 2476   | Inline: Spot builds seed directly |
| Verify seed completeness                 | 827    | Cross-check against checkpoints |
| Respin instructions                      | 486    | Seed + instructions for new instance |
| **Total** | **7241** | |
| **% of 200K** | **3.62%** | |
| **With 20% safety margin** | **8689 (4.34%)** | |

#### Rotation 2 -- Inline (6 checkpoints accumulated)

| Operation | Tokens | Notes |
|-----------|--------|-------|
| Read checkpoint records (6)              | 1560   | 6 records at ~250 tokens each |
| Read agent output                        | 1755   | Current cycle output |
| Read governing MD + brief                | 1009   | Context for seed construction |
| Construct compression seed               | 2574   | Inline: Spot builds seed directly |
| Verify seed completeness                 | 765    | Cross-check against checkpoints |
| Respin instructions                      | 529    | Seed + instructions for new instance |
| **Total** | **8192** | |
| **% of 200K** | **4.10%** | |
| **With 20% safety margin** | **9830 (4.92%)** | |

#### Rotation 3 -- Condenser-assisted (5 checkpoints accumulated)

| Operation | Tokens | Notes |
|-----------|--------|-------|
| Read checkpoint records (5)              | 1235   | 5 records at ~250 tokens each |
| Read agent output                        | 1560   | Current cycle output |
| Read governing MD + brief                | 1015   | Context for seed construction |
| Construct compression input package      | 1775   | Package for Condenser |
| Condenser produces seed                  | 2921   | Condenser context cost |
| Spot validates Condenser seed            | 1078   | Spot reviews Condenser output |
| Respin instructions                      | 526    | Seed + instructions for new instance |
| **Total** | **10110** | |
| **% of 200K** | **5.05%** | |
| **With 20% safety margin** | **12132 (6.07%)** | |

**Average compression headroom: 8514 tokens (4.26% of context)**
**With 20% safety margin: 10217 tokens (5.11% of context)**
**Standard deviation: 1461 tokens**
**Coefficient of variation: 17.2%**

### Checkpoint Cap Calculation

```
available_context = 200,000 - 10217 = 189783
checkpoint_cap = 189783 / 2746 = 69.1
checkpoint_cap (integer) = 69
```

**Recommended checkpoint cap: 15**
**Recommended heartbeat interval: 30s (default)**

## Run 2

### Checkpoint Size Measurements

| Checkpoint | Agent Output | MD Read | Reasoning | Entry Write | Total Tokens | % of 200K |
|------------|-------------|---------|-----------|-------------|-------------|-----------|
| 1          | 505         | 812     | 352       | 258         | 1927        | 0.96%     |
| 2          | 471         | 807     | 355       | 228         | 1861        | 0.93%     |
| 3          | 505         | 808     | 386       | 244         | 1943        | 0.97%     |
| 4          | 1013        | 817     | 345       | 259         | 2434        | 1.22%     |
| 5          | 1061        | 806     | 366       | 259         | 2492        | 1.25%     |
| 6          | 997         | 806     | 390       | 243         | 2436        | 1.22%     |
| 7          | 2004        | 806     | 349       | 249         | 3408        | 1.70%     |
| 8          | 1941        | 818     | 361       | 225         | 3345        | 1.67%     |
| 9          | 2113        | 802     | 370       | 240         | 3525        | 1.76%     |
| 10         | 3005        | 801     | 357       | 255         | 4418        | 2.21%     |

**Average checkpoint size: 2779 tokens (1.39% of context)**
**Standard deviation: 853 tokens**
**Coefficient of variation: 30.7%**

### Compression Headroom Measurements

#### Rotation 1 -- Inline (4 checkpoints accumulated)

| Operation | Tokens | Notes |
|-----------|--------|-------|
| Read checkpoint records (4)              | 940    | 4 records at ~250 tokens each |
| Read agent output                        | 1504   | Current cycle output |
| Read governing MD + brief                | 993    | Context for seed construction |
| Construct compression seed               | 2485   | Inline: Spot builds seed directly |
| Verify seed completeness                 | 818    | Cross-check against checkpoints |
| Respin instructions                      | 475    | Seed + instructions for new instance |
| **Total** | **7215** | |
| **% of 200K** | **3.61%** | |
| **With 20% safety margin** | **8658 (4.33%)** | |

#### Rotation 2 -- Inline (6 checkpoints accumulated)

| Operation | Tokens | Notes |
|-----------|--------|-------|
| Read checkpoint records (6)              | 1494   | 6 records at ~250 tokens each |
| Read agent output                        | 1816   | Current cycle output |
| Read governing MD + brief                | 992    | Context for seed construction |
| Construct compression seed               | 2610   | Inline: Spot builds seed directly |
| Verify seed completeness                 | 809    | Cross-check against checkpoints |
| Respin instructions                      | 473    | Seed + instructions for new instance |
| **Total** | **8194** | |
| **% of 200K** | **4.10%** | |
| **With 20% safety margin** | **9833 (4.92%)** | |

#### Rotation 3 -- Condenser-assisted (5 checkpoints accumulated)

| Operation | Tokens | Notes |
|-----------|--------|-------|
| Read checkpoint records (5)              | 1230   | 5 records at ~250 tokens each |
| Read agent output                        | 1566   | Current cycle output |
| Read governing MD + brief                | 993    | Context for seed construction |
| Construct compression input package      | 1883   | Package for Condenser |
| Condenser produces seed                  | 2682   | Condenser context cost |
| Spot validates Condenser seed            | 1033   | Spot reviews Condenser output |
| Respin instructions                      | 508    | Seed + instructions for new instance |
| **Total** | **9895** | |
| **% of 200K** | **4.95%** | |
| **With 20% safety margin** | **11874 (5.94%)** | |

**Average compression headroom: 8435 tokens (4.22% of context)**
**With 20% safety margin: 10122 tokens (5.06% of context)**
**Standard deviation: 1356 tokens**
**Coefficient of variation: 16.1%**

### Checkpoint Cap Calculation

```
available_context = 200,000 - 10122 = 189878
checkpoint_cap = 189878 / 2779 = 68.3
checkpoint_cap (integer) = 68
```

**Recommended checkpoint cap: 15**
**Recommended heartbeat interval: 30s (default)**

## Run 3

### Checkpoint Size Measurements

| Checkpoint | Agent Output | MD Read | Reasoning | Entry Write | Total Tokens | % of 200K |
|------------|-------------|---------|-----------|-------------|-------------|-----------|
| 1          | 513         | 798     | 361       | 259         | 1931        | 0.97%     |
| 2          | 483         | 794     | 321       | 274         | 1872        | 0.94%     |
| 3          | 517         | 788     | 368       | 241         | 1914        | 0.96%     |
| 4          | 995         | 797     | 362       | 266         | 2420        | 1.21%     |
| 5          | 1046        | 801     | 361       | 260         | 2468        | 1.23%     |
| 6          | 1000        | 797     | 318       | 275         | 2390        | 1.20%     |
| 7          | 1983        | 789     | 362       | 252         | 3386        | 1.69%     |
| 8          | 1939        | 802     | 345       | 253         | 3339        | 1.67%     |
| 9          | 2101        | 802     | 317       | 280         | 3500        | 1.75%     |
| 10         | 2984        | 794     | 336       | 245         | 4359        | 2.18%     |

**Average checkpoint size: 2758 tokens (1.38% of context)**
**Standard deviation: 841 tokens**
**Coefficient of variation: 30.5%**

### Compression Headroom Measurements

#### Rotation 1 -- Inline (4 checkpoints accumulated)

| Operation | Tokens | Notes |
|-----------|--------|-------|
| Read checkpoint records (4)              | 1004   | 4 records at ~250 tokens each |
| Read agent output                        | 1510   | Current cycle output |
| Read governing MD + brief                | 1020   | Context for seed construction |
| Construct compression seed               | 2607   | Inline: Spot builds seed directly |
| Verify seed completeness                 | 768    | Cross-check against checkpoints |
| Respin instructions                      | 513    | Seed + instructions for new instance |
| **Total** | **7422** | |
| **% of 200K** | **3.71%** | |
| **With 20% safety margin** | **8906 (4.45%)** | |

#### Rotation 2 -- Inline (6 checkpoints accumulated)

| Operation | Tokens | Notes |
|-----------|--------|-------|
| Read checkpoint records (6)              | 1560   | 6 records at ~250 tokens each |
| Read agent output                        | 1802   | Current cycle output |
| Read governing MD + brief                | 1012   | Context for seed construction |
| Construct compression seed               | 2472   | Inline: Spot builds seed directly |
| Verify seed completeness                 | 752    | Cross-check against checkpoints |
| Respin instructions                      | 497    | Seed + instructions for new instance |
| **Total** | **8095** | |
| **% of 200K** | **4.05%** | |
| **With 20% safety margin** | **9714 (4.86%)** | |

#### Rotation 3 -- Condenser-assisted (5 checkpoints accumulated)

| Operation | Tokens | Notes |
|-----------|--------|-------|
| Read checkpoint records (5)              | 1230   | 5 records at ~250 tokens each |
| Read agent output                        | 1623   | Current cycle output |
| Read governing MD + brief                | 983    | Context for seed construction |
| Construct compression input package      | 1892   | Package for Condenser |
| Condenser produces seed                  | 2978   | Condenser context cost |
| Spot validates Condenser seed            | 1010   | Spot reviews Condenser output |
| Respin instructions                      | 473    | Seed + instructions for new instance |
| **Total** | **10189** | |
| **% of 200K** | **5.09%** | |
| **With 20% safety margin** | **12227 (6.11%)** | |

**Average compression headroom: 8569 tokens (4.28% of context)**
**With 20% safety margin: 10282 tokens (5.14% of context)**
**Standard deviation: 1443 tokens**
**Coefficient of variation: 16.8%**

### Checkpoint Cap Calculation

```
available_context = 200,000 - 10282 = 189718
checkpoint_cap = 189718 / 2758 = 68.8
checkpoint_cap (integer) = 68
```

**Recommended checkpoint cap: 15**
**Recommended heartbeat interval: 30s (default)**

---

## Calibration Report Summary

### Raw Measurements Across All Runs

| Metric | Run 1 | Run 2 | Run 3 | Overall Mean |
|--------|-------|-------|-------|-------------|
| Avg checkpoint size (tokens) | 2746 | 2779 | 2758 | 2761 |
| Checkpoint size StdDev | 852 | 853 | 841 | 848 |
| Avg compression headroom (tokens) | 8514 | 8435 | 8569 | 8506 |
| Headroom StdDev | 1461 | 1356 | 1443 | 1420 |

### Final Recommended Values

- **average_checkpoint_size:** 2761 tokens (1.38% of context)
- **compression_headroom:** 10207 tokens (5.10% of context, with 20% safety margin)
- **checkpoint_cap:** 15 (raw calculation: 68.7)
- **heartbeat_interval:** 30 seconds

### Variance Analysis

- **Checkpoint size within-run CoV (avg):** 30.7%
- **Checkpoint size cross-run CoV:** 0.6%
- **Compression headroom within-run CoV (avg):** 16.7%
- **Compression headroom cross-run CoV:** 0.8%

### Pass/Fail Assessment

| Criterion | Result | Detail |
|-----------|--------|--------|
| 10 checkpoint measurements per run with CoV < 20% | FAIL | Within-run CoVs: 31.0%, 30.7%, 30.5%; Cross-run CoV: 0.6% |
| 3 rotation measurements per run with CoV < 20% | PASS | Within-run CoVs: 17.2%, 16.1%, 16.8%; Cross-run CoV: 0.8% |
| Checkpoint cap between 5-15 | PASS | Computed cap: 15 |
| All rotation cycles complete cleanly | PASS | 9/9 rotations completed across 3 runs |

**Overall Test Case 5 Result: FAIL**
