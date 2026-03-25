# Credit

Credit is a Monero-derived codebase prepared for an early public Credit mainnet. The current fork keeps the upstream consensus and emission model while renaming the network identity, binaries, address prefixes, and wallet URI scheme for Credit operators and integrators.

This repository builds and ships:

- `creditd`
- `credit-wallet-cli`
- `credit-wallet-rpc`

## Quick Facts

| Item | Value |
| --- | --- |
| Wallet URI scheme | `credit:` |
| Mainnet address prefixes | `70` standard, `71` integrated, `72` subaddress |
| Mainnet ports | P2P `47080`, daemon RPC `47081`, ZMQ RPC `47082` |
| Testnet ports | P2P `48080`, daemon RPC `48081`, ZMQ RPC `48082` |
| Stagenet ports | P2P `49080`, daemon RPC `49081`, ZMQ RPC `49082` |
| Fallback seed nodes | `45.63.65.47:47080`, `144.202.61.40:47080` |
| DNS seed hostnames | Not configured yet |

## Build From Source (Linux / Ubuntu)

The verified Linux path for public mainnet operators is Ubuntu with CMake and Ninja.

Install the build dependencies:

```bash
sudo apt update
sudo DEBIAN_FRONTEND=noninteractive apt install -y \
  build-essential ca-certificates git cmake ninja-build pkg-config ccache \
  libboost-all-dev libssl-dev libsodium-dev libunbound-dev libzmq3-dev \
  libreadline-dev curl
```

Clone the repository and build the daemon plus wallet binaries:

```bash
git clone https://github.com/w38741325/CreditRelease.git
cd CreditRelease

cmake -S . -B build-linux -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DMANUAL_SUBMODULES=1 \
  -DBUILD_TESTS=OFF \
  -DUSE_DEVICE_TREZOR=OFF

cmake --build build-linux --target daemon simplewallet wallet_rpc_server --parallel "$(nproc)"
```

Install the resulting binaries into `/usr/bin`:

```bash
sudo install -Dm755 build-linux/bin/creditd /usr/bin/creditd
sudo install -Dm755 build-linux/bin/credit-wallet-cli /usr/bin/credit-wallet-cli
sudo install -Dm755 build-linux/bin/credit-wallet-rpc /usr/bin/credit-wallet-rpc
```

Build outputs are written to `build-linux/bin/`.

For a public bootstrap or seed node, keep TCP `47080` reachable and usually keep `47081` and `47082` restricted to localhost or trusted operators. The checked-in service template lives at `utils/systemd/creditd.service`, and the fuller operator runbook is in `docs/credit/seed-node-operator.md`.

`MANUAL_SUBMODULES=1` only skips the CMake submodule freshness check. The dependency trees used by this repo are already vendored under `external/`.

## Build From Source (Windows / MSYS2 MinGW64)

The verified Windows build path for this repository is `MSYS2 MinGW64`.

From the repository root in the `MSYS2 MinGW64` shell, run:

```bash
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTS=ON -DMANUAL_SUBMODULES=1
cmake --build build --target daemon simplewallet wallet_rpc_server unit_tests functional_tests --parallel 6
```

Build outputs are written to `build/bin/`.

If you start the binaries from PowerShell instead of the MSYS2 shell, add `C:\msys64\mingw64\bin` to `PATH` first so the MinGW runtime DLLs can be located.

## Optional Functional Test Dependencies

If you plan to run the Python-backed functional tests, install the packages currently referenced by `tests/README.md`:

```bash
pip install requests psutil monotonic zmq deepdiff
```

## Start A Local Node

The simplest Windows launch path from PowerShell is:

```powershell
$env:PATH = "C:\msys64\mingw64\bin;$env:PATH"
.\build\bin\creditd.exe --non-interactive --data-dir .\build\mainnet-node --p2p-bind-port 47080 --rpc-bind-port 47081 --zmq-rpc-bind-port 47082 --seed-node 45.63.65.47:47080 --seed-node 144.202.61.40:47080
```

This starts a local mainnet daemon with the current Credit launch defaults and explicit bootstrap peers.

## Wallet Usage

CLI wallet example:

```powershell
.\build\bin\credit-wallet-cli.exe --daemon-address 127.0.0.1:47081 --wallet-file .\build\wallets\demo
```

Wallet RPC example:

```powershell
.\build\bin\credit-wallet-rpc.exe --daemon-address 127.0.0.1:47081 --wallet-dir .\build\wallets --rpc-bind-port 47083 --disable-rpc-login --non-interactive
```

Payment URIs now use the `credit:` scheme, for example:

```text
credit:<credit-address>?tx_amount=1.25
```

## Documentation

- [docs/credit/public-mainnet-quickstart.md](docs/credit/public-mainnet-quickstart.md) for a shorter operator-first startup guide
- [docs/credit/seed-node-operator.md](docs/credit/seed-node-operator.md) for public seed-node operation and deployment notes
- [docs/credit/launch-inputs.md](docs/credit/launch-inputs.md) for the current launch constants and network settings
- [tests/README.md](tests/README.md) for the broader test suite layout and test-specific instructions

## Repository Notes

- `external/` now vendors the dependency trees used by the build, including `gtest`, `miniupnp`, `randomx`, `rapidjson`, and `supercop`.
- No DNS seed hostnames are configured in this cut yet, so bootstrap currently relies on the fallback IP seeds above and any explicit `--seed-node` values you provide.
- Treat this repository like freshly launched network infrastructure: watch bootstrap reachability, daemon health, release packaging, and docs drift closely while the network is still small.
