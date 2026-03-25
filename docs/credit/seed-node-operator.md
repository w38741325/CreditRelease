# Credit Seed Node Operator Guide

This guide covers running public bootstrap nodes for the Credit mainnet. The current Credit launch defaults use mainnet ports `47080`, `47081`, and `47082`.

## Current Bootstrap Set

- `45.63.65.47:47080`
- `144.202.61.40:47080`
- No DNS seed hostnames are configured yet. Add them later once you have a domain and stable records.

## Recommended Seed Node Command

Run `creditd` in mainnet mode with explicit ports and a dedicated data directory:

```bash
./build/bin/creditd --non-interactive --data-dir /var/lib/credit/mainnet-seed --p2p-bind-ip 0.0.0.0 --p2p-bind-port 47080 --rpc-bind-ip 0.0.0.0 --rpc-bind-port 47081 --zmq-rpc-bind-ip 0.0.0.0 --zmq-rpc-bind-port 47082 --confirm-external-bind
```

If the node is only meant to bootstrap peers, it is reasonable to keep `47081` and `47082` firewalled to trusted operators while leaving `47080` publicly reachable.

## Firewall And Reachability

- Open inbound TCP `47080` so new Credit mainnet peers can discover and sync from the node.
- Only expose `47081` and `47082` publicly if you intend to support external RPC or monitoring clients.
- If you do expose `47081` or `47082`, restrict them with host firewall rules, network ACLs, or a private operator network.
- Store blockchain data in a dedicated directory and monitor disk growth during early mainnet activity.

## DNS And Bootstrap Hygiene

- The hardcoded bootstrap list currently uses the two raw IP endpoints above.
- When you add DNS later, publish at least two independent seed hosts and keep them aligned with the fallback IP list.
- Keep configs, docs, and release notes aligned with the same bootstrap endpoints after every change.
- Re-check that the daemon reports the Credit mainnet network and the expected ports after every upgrade.

## Suggested Operator Checks

- Confirm the process is listening on `47080`, `47081`, and `47082` as intended.
- Start a second mainnet node with `--seed-node 45.63.65.47:47080 --seed-node 144.202.61.40:47080` and verify peer discovery succeeds.
- Watch logs for recurring handshake failures, bind failures, or stale DNS records after restarts.
