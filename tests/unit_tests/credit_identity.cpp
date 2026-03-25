// Copyright (c) 2026, The Credit Project
//
// All rights reserved.

#include "gtest/gtest.h"
#include "cryptonote_config.h"
#include "version.h"

TEST(credit_identity, uses_credit_mainnet_release_name_ports_and_prefixes)
{
  const auto &cfg = cryptonote::get_config(cryptonote::MAINNET);
  EXPECT_STREQ(MONERO_RELEASE_NAME, "Credit");
  EXPECT_EQ(cfg.CRYPTONOTE_PUBLIC_ADDRESS_BASE58_PREFIX, 70);
  EXPECT_EQ(cfg.CRYPTONOTE_PUBLIC_INTEGRATED_ADDRESS_BASE58_PREFIX, 71);
  EXPECT_EQ(cfg.CRYPTONOTE_PUBLIC_SUBADDRESS_BASE58_PREFIX, 72);
  EXPECT_EQ(cfg.P2P_DEFAULT_PORT, 47080);
  EXPECT_EQ(cfg.RPC_DEFAULT_PORT, 47081);
  EXPECT_EQ(cfg.ZMQ_RPC_DEFAULT_PORT, 47082);
  EXPECT_EQ(cfg.GENESIS_NONCE, 47000);
}

TEST(credit_identity, uses_credit_testnet_ports_and_prefixes)
{
  const auto &cfg = cryptonote::get_config(cryptonote::TESTNET);
  EXPECT_EQ(cfg.CRYPTONOTE_PUBLIC_ADDRESS_BASE58_PREFIX, 73);
  EXPECT_EQ(cfg.CRYPTONOTE_PUBLIC_INTEGRATED_ADDRESS_BASE58_PREFIX, 74);
  EXPECT_EQ(cfg.CRYPTONOTE_PUBLIC_SUBADDRESS_BASE58_PREFIX, 75);
  EXPECT_EQ(cfg.P2P_DEFAULT_PORT, 48080);
  EXPECT_EQ(cfg.RPC_DEFAULT_PORT, 48081);
  EXPECT_EQ(cfg.ZMQ_RPC_DEFAULT_PORT, 48082);
  EXPECT_EQ(cfg.GENESIS_NONCE, 48000);
}

TEST(credit_identity, uses_credit_testnet_network_id)
{
  const auto &cfg = cryptonote::get_config(cryptonote::TESTNET);
  const boost::uuids::uuid expected = {{
    0x43, 0x72, 0x65, 0x64, 0x69, 0x74, 0x02, 0x48,
    0x10, 0x80, 0x48, 0x10, 0x80, 0x48, 0x10, 0x80
  }};
  EXPECT_EQ(cfg.NETWORK_ID, expected);
}
