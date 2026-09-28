import sys
import json
from client import CostBasedQueryOptimizer

cbo = CostBasedQueryOptimizer()

def handle_rpc(line):
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-cost-based-query-optimizer-skill", "version": "1.0.0"},
            "capabilities": {"tools": {}}
        }
    elif method == "tools/list":
        res = {
            "tools": [
                {
                    "name": "optimize_join",
                    "description": "Select the lowest-cost equi-join algorithm based on table cardinality",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "table_a_rows": {"type": "integer"},
                            "table_b_rows": {"type": "integer"}
                        },
                        "required": ["table_a_rows", "table_b_rows"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "optimize_join":
            a = args.get("table_a_rows", 100)
            b = args.get("table_b_rows", 100)
            plan = cbo.choose_optimal_join(a, b)
            res = {"content": [{"type": "text", "text": json.dumps(plan)}]}
        else:
            res = {"isError": True, "content": [{"type": "text", "text": f"Unknown tool {tool_name}"}]}
    else:
        res = {"error": {"code": -32601, "message": "Method not found"}}

    resp = {"jsonrpc": "2.0", "id": req_id, "result": res.get("result", res)}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
