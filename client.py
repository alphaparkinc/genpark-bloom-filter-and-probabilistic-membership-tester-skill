"""Bloom Filter and Probabilistic Membership Tester.
100% Python Standard Library.
"""

import math
import hashlib
from typing import Dict, Any, Optional, List


class BloomFilter:
    """Memory-efficient probabilistic set membership filter. Guarantees zero false negatives
    and bounded false positive probability using Kirsch-Mitzenmacher double-hashing."""

    def __init__(self, expected_items: int = 10000, target_false_positive_rate: float = 0.01):
        self.expected_items = max(1, expected_items)
        self.target_fpr = target_false_positive_rate

        # Optimal bit array size m = -(n * ln(p)) / (ln(2)^2)
        self.bit_size = int(math.ceil(-(self.expected_items * math.log(self.target_fpr)) / (math.log(2) ** 2)))
        # Optimal number of hash functions k = (m / n) * ln(2)
        self.num_hashes = max(1, int(round((self.bit_size / self.expected_items) * math.log(2))))

        # Bytearray representation: 8 bits per byte
        self.byte_count = (self.bit_size + 7) // 8
        self.bit_array = bytearray(self.byte_count)
        self.inserted_count = 0

    def _get_hash_indices(self, item: str) -> List[int]:
        """Generates k bit indices using Kirsch-Mitzenmacher double-hashing:
        gi(x) = h1(x) + i * h2(x) mod m."""
        digest = hashlib.sha256(item.encode("utf-8")).digest()
        # Extract two 64-bit integer hashes from 32-byte digest
        h1 = int.from_bytes(digest[:8], byteorder="big")
        h2 = int.from_bytes(digest[8:16], byteorder="big")

        indices = []
        for i in range(self.num_hashes):
            idx = (h1 + i * h2) % self.bit_size
            indices.append(idx)
        return indices

    def add(self, item: str):
        """Adds an item to the Bloom filter."""
        for idx in self._get_hash_indices(item):
            byte_idx = idx // 8
            bit_idx = idx % 8
            self.bit_array[byte_idx] |= (1 << bit_idx)
        self.inserted_count += 1

    def contains(self, item: str) -> bool:
        """Tests whether an item is probably in the set (zero false negatives)."""
        for idx in self._get_hash_indices(item):
            byte_idx = idx // 8
            bit_idx = idx % 8
            if not (self.bit_array[byte_idx] & (1 << bit_idx)):
                return False
        return True

    def get_metrics(self) -> Dict[str, Any]:
        """Returns diagnostic metrics including estimated current false-positive probability."""
        # Estimated FPR: (1 - e^(-k * n / m))^k
        exponent = - (self.num_hashes * self.inserted_count) / float(self.bit_size)
        current_fpr = (1.0 - math.exp(exponent)) ** self.num_hashes

        return {
            "expected_items": self.expected_items,
            "inserted_count": self.inserted_count,
            "bit_size": self.bit_size,
            "memory_bytes": self.byte_count,
            "num_hashes": self.num_hashes,
            "target_false_positive_rate": self.target_fpr,
            "estimated_current_false_positive_rate": round(current_fpr, 6),
            "bits_per_item": round(self.bit_size / self.expected_items, 2),
        }
