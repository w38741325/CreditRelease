# Credit Public Testnet Fork Design

## Summary

Credit is a direct fork of upstream Monero intended to launch first as a public testnet. The fork should stay as close to Monero as possible and should not introduce custom consensus, emission, mining, wallet, or transaction behavior in the first milestone.

The goal of the first Credit milestone is to publish a clean, public, Monero-compatible testnet fork with Credit-specific branding, chain identity, network parameters, seed bootstrap, binaries, and launch documentation.

## Baseline

- Upstream source: Monero `master`
- Upstream reference commit: `b9998fc9e1c280d30e4b40ba983b1964eb256d66`
- Fork approach: direct fork of upstream Monero, keeping the repository layout and major behavior intact
- Initial launch target: public testnet only

## Non-Goals

The first Credit milestone explicitly does not include:

- Consensus rule changes
- Emission or reward schedule changes
- GUI wallet work
- Explorer, faucet, or other ecosystem services
- New discovery systems beyond Monero's existing seed-node model
- Mainnet launch

## Product Identity

Credit uses Credit as both the public brand and the technical identity.

- Daemon binary: `creditd`
- CLI wallet binary: `credit-wallet-cli`
- Wallet RPC binary: `credit-wallet-rpc`
- URI scheme: `credit:`
- Default data directory root: `.credit`
- User-facing chain name: `Credit`

## Architecture

### 1. Direct Monero Fork

Credit should remain a mechanical fork of Monero rather than a redesign. The repository should keep upstream structure, build layout, and behavior so the diff is narrowly focused on fork identity and testnet publication requirements.

### 2. Chain Identity Split

Credit must be cryptographically and operationally separate from Monero. The fork should change all chain identity surfaces that would otherwise allow confusion or accidental cross-network usage:

- `CRYPTONOTE_NAME`
- network UUIDs
- default ports
- base58 address prefixes
- genesis transaction and nonce values
- binary names
- wallet URI scheme
- default filenames and data paths
- user-facing banners and help text

The main source of truth for these values is expected to live in Monero's existing configuration paths, especially `src/cryptonote_config.h`, build metadata, and version metadata.

### 3. Peer Bootstrap

Credit testnet should reuse Monero's existing peer bootstrap model:

- Credit-operated DNS seed hosts
- Credit-operated fallback static seed nodes
- optional Credit-operated bootstrap RPC daemon

No new peer discovery mechanism should be introduced for the first milestone.

### 4. Wallet and Daemon Renaming

All obvious Monero-specific user-facing strings and artifact identifiers should be renamed where they would confuse Credit users. This includes:

- startup banners
- help text
- config examples
- wallet export/import magic strings
- transaction artifact filenames
- update and donation references
- `monero:` URI handling
- `.bitmonero` references and related file paths

The purpose is not cosmetic polish for its own sake. The purpose is to prevent accidental mixing of Credit and Monero tooling or artifacts.

### 5. Monero Infrastructure Detachment

The Credit fork must not point by default at Monero-operated services.

This includes removing or replacing inherited:

- DNS checkpoint domains
- compiled checkpoint blobs when not valid for Credit
- donation references
- update endpoints
- help links that still present Credit as Monero

For the first public testnet, checkpoints should either be empty or Credit-owned only.

## Public Testnet Rollout

For the first release, "public-ready" means a third party can download the binaries, start a Credit testnet node, discover peers, sync, create a wallet, mine test blocks, and send transactions without patching the source.

### Required Infrastructure

- At least 2 public Credit P2P seed nodes
- DNS or published hostnames for those seeds
- Static fallback seed entries baked into the fork
- Optional 1 public Credit bootstrap RPC daemon

### Required Release Artifacts

- Source repository
- CLI binaries for the platforms that are actually built and tested
- Example daemon configuration for Credit
- Seed-node operator instructions
- Testnet user quickstart for daemon and wallet usage

### Supported Surface

The first Credit milestone supports:

- `creditd`
- `credit-wallet-cli`
- `credit-wallet-rpc`

It does not promise:

- GUI binaries
- mainnet
- production infrastructure beyond testnet bootstrap

## Testing Strategy

Even though Monero is mature, the Credit fork points are new and must be validated. The test focus should be on proving fork wiring, not re-proving Monero's entire protocol from scratch.

### Validation Stages

1. Local build and smoke validation
2. Local single-node daemon and wallet bring-up
3. Local multi-node sync validation
4. Public seed-node bring-up
5. Public testnet validation with clean machines and fresh data directories

### Core Acceptance Checks

#### Build Validation

- Claimed target builds succeed cleanly
- Produced binary names are Credit-specific
- Version banners and help output identify Credit, not Monero

#### Chain Separation

- Credit nodes do not handshake with Monero nodes
- Credit addresses are distinct from Monero addresses
- Credit wallet artifacts are distinct from Monero artifacts
- Credit daemon uses Credit-specific default ports and data paths

#### Network Validation

- A fresh Credit node can discover peers from Credit seed nodes
- Two or more fresh Credit testnet nodes can sync from zero
- Nodes reconnect and continue syncing after restart

#### Wallet Validation

- A wallet can be created against Credit testnet
- A wallet can connect to a Credit daemon
- Test blocks can be mined on Credit testnet
- Funds can be transferred end to end on Credit testnet

#### Release Readiness

- No default Monero checkpoint, donation, or update infrastructure remains active
- User documentation matches Credit names, ports, flags, and URI scheme
- Known limitations are documented honestly

## Implementation Boundaries

The implementation should stay minimal and mechanical:

- prefer targeted renames over refactors
- preserve upstream directory structure
- preserve upstream build flow
- preserve upstream network and wallet behavior unless required for Credit identity separation

If any work starts to drift into new features or protocol redesign, it should be cut from the first milestone.

## Open Operational Inputs

The following values must be supplied during implementation or release preparation:

- final Credit testnet ports
- final Credit address prefixes
- final Credit network UUIDs
- final Credit genesis transaction and nonce values
- final Credit DNS seed hostnames
- final Credit fallback seed node addresses
- target binary release platforms

## Milestone Definition

The Credit public testnet milestone is complete when:

- the fork builds as Credit
- the fork is separated from Monero by chain identity and network configuration
- public Credit seed bootstrap is operational
- daemon and wallet flows work on Credit testnet
- launch and operator documentation are present
- a third party can join the Credit testnet using published instructions
