# genpark-bloom-filter-and-probabilistic-membership-tester-skill

Memory-efficient Bloom filter, probabilistic set membership tester, and false-positive rate optimizer.

100% Python Standard Library implementation with zero external dependencies.

## Key Capabilities

- **Mathematical Capacity & False-Positive Optimization**: Automatically sizes bit-arrays and computes the optimal number of hash functions ($k$) given expected item volume and target error rates ($p$).
- **Kirsch-Mitzenmacher Double-Hashing**: Generates arbitrary numbers of uniform hash functions from a single SHA-256 digest with minimal CPU overhead.
- **Strict Zero False-Negative Guarantee**: Guarantees that items not present in the set are never falsely reported as present.
- **Ultra-Low Memory Footprint**: Uses bytearray representations consuming under 10 bits per item at 1% error probability.

## Architecture

```
[Inbound Key / Item String + Target Capacity / FPR Config]
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│                      BloomFilter                       │
│  - Optimal Bit Array Sizer: m = -n*ln(p)/(ln2)^2       │
│  - Double-Hashing Engine: gi(x) = h1(x) + i*h2(x)      │
│  - Bitwise Bytearray Mutation & Inspection             │
│  - Real-Time False Positive Probability Estimator      │
└────────────────────────────────────────────────────────┘
          │                                  │
    (Bit Missing)                    (All k Bits Set)
          ▼                                  ▼
[100% Definite Negative]            [Probabilistic Positive]
```

## MCP Server Integration

Run standard MCP stdio server:
```bash
python mcp_server.py
```

Exposed Tools:
- `bloom_add`: Adds an item to the Bloom filter.
- `bloom_contains`: Checks if an item is likely in the set (guarantees zero false negatives).
- `bloom_metrics`: Retrieves Bloom filter capacity, memory footprint, and false positive metrics.

## Quickstart (Python API)

```python
from client import BloomFilter

bf = BloomFilter(expected_items=5000, target_false_positive_rate=0.01)
bf.add("user_123")
print("Contains user_123:", bf.contains("user_123"))
print("Contains user_999:", bf.contains("user_999"))
```

---

## GenPark Ecosystem

- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)
