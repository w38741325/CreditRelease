# Credit Blockchain Utilities

Copyright (c) 2014-2024, The Monero Project

## Introduction

The blockchain utilities allow one to import and export the Credit blockchain.

## Usage

See also each utility's `--help` option.

### Export an existing blockchain database

`$ credit-blockchain-export`

This loads the existing blockchain and exports it to `<data-dir>/export/blockchain.raw`.

### Import the exported file

`$ credit-blockchain-import`

This imports blocks from `<data-dir>/export/blockchain.raw` (exported using the
`credit-blockchain-export` tool as described above) into the current database.

Defaults: `--batch on`, `--batch size 20000`, `--verify on`

Batch size refers to the number of blocks and can be adjusted for performance based on available RAM.

Verification should only be turned off if importing from a trusted blockchain.

If you encounter an error like "resizing not supported in batch mode", you can just re-run
the `credit-blockchain-import` command again, and it will restart from where it left off.

```bash
## use default settings to import blockchain.raw into the database
$ credit-blockchain-import

## fast import with large batch size, database mode "fastest", verification off
$ credit-blockchain-import --batch-size 20000 --database lmdb#fastest --verify off
```

### Import options

`--input-file`
specifies the input file path for importing

default: `<data-dir>/export/blockchain.raw`

`--output-file`
specifies the output file path to export to

default: `<data-dir>/export/blockchain.raw`

`--block-stop`
stop at block number

`--database <database type>`

`--database <database type>#<flag(s)>`

database type: `lmdb, memory`

flags:

The flag after the `#` is interpreted as a composite mode/flag if there's only
one (no comma-separated arguments).

The composite mode represents multiple DB flags and supports different database types:

`safe, fast, fastest`

Database-specific flags can be set instead.

LMDB flags (more than one may be specified):

`nosync, nometasync, writemap, mapasync, nordahead`

## Examples

```bash
$ credit-blockchain-import --database lmdb#fastest

$ credit-blockchain-import --database lmdb#nosync

$ credit-blockchain-import --database lmdb#nosync,nometasync
```
