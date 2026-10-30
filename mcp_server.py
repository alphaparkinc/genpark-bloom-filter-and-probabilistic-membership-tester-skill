"""MCP server for Bloom Filter and Probabilistic Membership Tester."""
import sys
import json
from client import BloomFilter

_filter_instance = BloomFilter(expected_items=10000, target_false_positive_rate=0.01)


def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "bloom_add",
                    "description": "Adds an item to the Bloom filter",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "item": {"type": "string"},
                        },
                        "required": ["item"],
                    },
                },
                {
                    "name": "bloom_contains",
                    "description": "Checks if an item is likely in the set (guarantees zero false negatives)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "item": {"type": "string"},
                        },
                        "required": ["item"],
                    },
                },
                {
                    "name": "bloom_metrics",
                    "description": "Retrieves Bloom filter capacity, memory footprint, and false positive metrics",
                    "inputSchema": {
                        "type": "object",
                        "properties": {},
                    },
                },
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "bloom_add":
            _filter_instance.add(args.get("item", ""))
            return {"content": [{"type": "text", "text": json.dumps({"status": "added", "item": args.get("item")})}]}
        elif tool_name == "bloom_contains":
            res = _filter_instance.contains(args.get("item", ""))
            return {"content": [{"type": "text", "text": json.dumps({"item": args.get("item"), "probably_contains": res})}]}
        elif tool_name == "bloom_metrics":
            res = _filter_instance.get_metrics()
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}


if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
