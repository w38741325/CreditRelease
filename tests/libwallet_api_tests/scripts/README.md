# Running libwallet_api tests

## Environment for the tests
* A running Credit daemon linked to Credit testnet.
  By default, tests expect a daemon at `localhost:38081`.
  This can be overridden with `TESTNET_DAEMON_ADDRESS=<your_daemon_address>`.
  The upstream [Monero private testnet guide](https://github.com/moneroexamples/private-testnet) is still a useful reference for the inherited workflow.

* A directory with pre-generated wallets
  (`wallet_01.bin`, `wallet_02.bin`, ..., `wallet_06.bin`; some of these wallets might not be used in the tests currently).
  By default, tests expect these wallets in `/var/lib/credit/testnet_pvt`.
  This can be overridden with `WALLETS_ROOT_DIR=<your_directory_with_wallets>`.
  The directory and files should be writable for the user running tests.

## Generating test wallets
* `create_wallets.sh` creates wallets (`wallet_01.bin`, `wallet_02.bin`, ..., `wallet_06.bin`) in the current directory.
  When running it the first time, uncomment `# create_wallet wallet_m` to create the miner wallet as well.
  This wallet should be used for mining and seeding the test wallets.

* `mining_start.sh` and `mining_stop.sh` are helper scripts to start and stop mining on the miner wallet.

* `send_funds.sh` seeds the test wallets. Run it after the miner wallet has enough balance.

