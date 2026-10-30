"""Example usage for Bloom Filter and Probabilistic Membership Tester."""
from client import BloomFilter


def main():
    print("=== 1. Initializing Bloom Filter (Capacity: 1,000, Target FPR: 1%) ===")
    bf = BloomFilter(expected_items=1000, target_false_positive_rate=0.01)
    metrics_initial = bf.get_metrics()
    print(f"Optimal Bit Size: {metrics_initial['bit_size']} bits ({metrics_initial['memory_bytes']} bytes)")
    print(f"Hash Functions Count (k): {metrics_initial['num_hashes']}")

    print("\n=== 2. Inserting Known Items ===")
    known_users = [f"user_{i}@enterprise.com" for i in range(100)]
    for u in known_users:
        bf.add(u)
    print(f"Inserted {len(known_users)} items.")

    print("\n=== 3. Testing Membership (Zero False Negatives) ===")
    assert all(bf.contains(u) for u in known_users)
    print("All 100 inserted users tested Positive (True): VERIFIED 100% TRUE POSITIVES")

    print("\n=== 4. Testing Non-Inserted Items ===")
    unseen_users = [f"unseen_{i}@other.org" for i in range(500)]
    false_positives = sum(1 for u in unseen_users if bf.contains(u))
    print(f"Out of 500 unseen items, false positives observed: {false_positives} ({false_positives/500 * 100:.2f}%)")

    print("\n=== 5. Final Operational Metrics ===")
    m = bf.get_metrics()
    print("Metrics:", m)


if __name__ == "__main__":
    main()
