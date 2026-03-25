# Credit Public Mainnet Quickstart

This quickstart covers the shortest path to building the Credit binaries and bringing up a local Credit mainnet daemon plus a wallet client on Windows.

## 1. Build In MSYS2 MinGW64

Open the `MSYS2 MinGW64` shell in the repository root and run:

```bash
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTS=ON -DMANUAL_SUBMODULES=1
cmake --build build --target daemon simplewallet wallet_rpc_server
```

This produces the renamed Credit binaries under `build/bin/`.

## 2. Start A Local Credit Mainnet Daemon

The Credit mainnet launch inputs reserve these daemon ports:

- P2P: `47080`
- JSON-RPC: `47081`
- ZMQ-RPC: `47082`

Start a local node with those ports:

```bash
./build/bin/creditd --non-interactive --data-dir ./build/mainnet-node --p2p-bind-port 47080 --rpc-bind-port 47081 --zmq-rpc-bind-port 47082 --seed-node 45.63.65.47:47080 --seed-node 144.202.61.40:47080
```

Wait for the daemon log to show that the RPC server is ready before connecting a wallet.

## 3. Connect With A Wallet

Use either the CLI wallet or the wallet RPC server.

CLI wallet example:

```bash
./build/bin/credit-wallet-cli --daemon-address 127.0.0.1:47081 --wallet-file ./build/mainnet-wallets/demo
```

Wallet RPC example:

```bash
./build/bin/credit-wallet-rpc --daemon-address 127.0.0.1:47081 --wallet-dir ./build/mainnet-wallets --rpc-bind-port 47083 --disable-rpc-login --non-interactive
```

If you start `credit-wallet-cli.exe` from PowerShell, add `C:\msys64\mingw64\bin` to `PATH` first so the MinGW runtime DLLs resolve correctly.

## 4. Use The Credit URI Scheme

Payment URIs now use the `credit:` scheme instead of `monero:`.

Example:

```text
credit:<credit-address>?tx_amount=1.25
```

Any tooling or documentation that still emits `monero:` should be updated before sharing the Credit mainnet with external users.

## 5. Bootstrap Notes

- The launch inputs file is at [launch-inputs.md](./launch-inputs.md).
- The current hardcoded bootstrap endpoints are `45.63.65.47:47080` and `144.202.61.40:47080`.
- No DNS seed hostnames are configured yet in this cut. When you later publish stable hostnames, update `src/p2p/net_node.h` to match them.
- For a public-facing node, continue with the operator guide at [seed-node-operator.md](./seed-node-operator.md).
