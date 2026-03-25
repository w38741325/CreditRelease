// Copyright (c) 2016-2024, The Monero Project
// 
// All rights reserved.
// 
// Redistribution and use in source and binary forms, with or without modification, are
// permitted provided that the following conditions are met:
// 
// 1. Redistributions of source code must retain the above copyright notice, this list of
//    conditions and the following disclaimer.
// 
// 2. Redistributions in binary form must reproduce the above copyright notice, this list
//    of conditions and the following disclaimer in the documentation and/or other
//    materials provided with the distribution.
// 
// 3. Neither the name of the copyright holder nor the names of its contributors may be
//    used to endorse or promote products derived from this software without specific
//    prior written permission.
// 
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
// EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
// MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
// THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
// PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
// STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
// THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#include "gtest/gtest.h"
#include "wallet/wallet2.h"
#include "cryptonote_basic/cryptonote_basic_impl.h"
#include "serialization/binary_utils.h"

#define MAKE_STR(arr) std::string(arr, sizeof(arr) - 1)

namespace
{
  cryptonote::account_public_address test_public_address()
  {
    const std::string serialized_keys = MAKE_STR(
      "\xf7\x24\xbc\x5c\x6c\xfb\xb9\xd9\x76\x02\xc3\x00\x42\x3a\x2f\x28"
      "\x64\x18\x74\x51\x3a\x03\x57\x78\xa0\xc1\x77\x8d\x83\x32\x01\xe9"
      "\x22\x09\x39\x68\x9e\xdf\x1a\xbd\x5b\xc1\xd0\x31\xf7\x3e\xcd\x6c"
      "\x99\x3a\xdd\x66\xd6\x80\x88\x70\x45\x6a\xfe\xb8\xe7\xee\xb6\x8d");

    cryptonote::account_public_address address{};
    EXPECT_TRUE(serialization::parse_binary(serialized_keys, address));
    return address;
  }

  const std::string& test_address()
  {
    static const std::string address =
      cryptonote::get_account_address_as_str(cryptonote::TESTNET, false, test_public_address());
    return address;
  }

  const std::string& test_integrated_address()
  {
    static const crypto::hash8 payment_id = {{
      static_cast<char>(0xf6), static_cast<char>(0x12), static_cast<char>(0xca), static_cast<char>(0xc0),
      static_cast<char>(0xb6), static_cast<char>(0xcb), static_cast<char>(0x1c), static_cast<char>(0xda)
    }};
    static const std::string address =
      cryptonote::get_account_integrated_address_as_str(cryptonote::TESTNET, test_public_address(), payment_id);
    return address;
  }
}
// included payment id: <f612cac0b6cb1cda>

#define PARSE_URI(uri, expected) \
  std::string address, payment_id, recipient_name, description, error; \
  uint64_t amount; \
  std::vector<std::string> unknown_parameters; \
  tools::wallet2 w(cryptonote::TESTNET); \
  bool ret = w.parse_uri(uri, address, payment_id, amount, description, recipient_name, unknown_parameters, error); \
  ASSERT_EQ(ret, expected);

TEST(uri, empty_string)
{
  PARSE_URI("", false);
}

TEST(uri, no_scheme)
{
  PARSE_URI("credit", false);
}

TEST(uri, bad_scheme)
{
  PARSE_URI("monero:" + test_address(), false);
}

TEST(uri, scheme_not_first)
{
  PARSE_URI(" credit:", false);
}

TEST(uri, no_body)
{
  PARSE_URI("credit:", false);
}

TEST(uri, no_address)
{
  PARSE_URI("credit:?", false);
}

TEST(uri, bad_address)
{
  PARSE_URI("credit:44444", false);
}

TEST(uri, good_address)
{
  PARSE_URI("credit:" + test_address(), true);
  ASSERT_EQ(address, test_address());
}

TEST(uri, good_integrated_address)
{
  PARSE_URI("credit:" + test_integrated_address(), true);
}

TEST(uri, parameter_without_inter)
{
  PARSE_URI("credit:" + test_address() + "&amount=1", false);
}

TEST(uri, parameter_without_equals)
{
  PARSE_URI("credit:" + test_address() + "?amount", false);
}

TEST(uri, parameter_without_value)
{
  PARSE_URI("credit:" + test_address() + "?tx_amount=", false);
}

TEST(uri, negative_amount)
{
  PARSE_URI("credit:" + test_address() + "?tx_amount=-1", false);
}

TEST(uri, bad_amount)
{
  PARSE_URI("credit:" + test_address() + "?tx_amount=alphanumeric", false);
}

TEST(uri, duplicate_parameter)
{
  PARSE_URI("credit:" + test_address() + "?tx_amount=1&tx_amount=1", false);
}

TEST(uri, unknown_parameter)
{
  PARSE_URI("credit:" + test_address() + "?unknown=1", true);
  ASSERT_EQ(unknown_parameters.size(), 1);
  ASSERT_EQ(unknown_parameters[0], "unknown=1");
}

TEST(uri, unknown_parameters)
{
  PARSE_URI("credit:" + test_address() + "?tx_amount=1&unknown=1&tx_description=desc&foo=bar", true);
  ASSERT_EQ(unknown_parameters.size(), 2);
  ASSERT_EQ(unknown_parameters[0], "unknown=1");
  ASSERT_EQ(unknown_parameters[1], "foo=bar");
}

TEST(uri, empty_payment_id)
{
  PARSE_URI("credit:" + test_address() + "?tx_payment_id=", false);
}

TEST(uri, bad_payment_id)
{
  PARSE_URI("credit:" + test_address() + "?tx_payment_id=1234567890", false);
}

TEST(uri, short_payment_id)
{
  PARSE_URI("credit:" + test_address() + "?tx_payment_id=1234567890123456", false);
}

TEST(uri, long_payment_id)
{
  PARSE_URI("credit:" + test_address() + "?tx_payment_id=1234567890123456789012345678901234567890123456789012345678901234", true);
  ASSERT_EQ(address, test_address());
  ASSERT_EQ(payment_id, "1234567890123456789012345678901234567890123456789012345678901234");
}

TEST(uri, payment_id_with_integrated_address)
{
  PARSE_URI("credit:" + test_integrated_address() + "?tx_payment_id=1234567890123456", false);
}

TEST(uri, empty_description)
{
  PARSE_URI("credit:" + test_address() + "?tx_description=", true);
  ASSERT_EQ(description, "");
}

TEST(uri, empty_recipient_name)
{
  PARSE_URI("credit:" + test_address() + "?recipient_name=", true);
  ASSERT_EQ(recipient_name, "");
}

TEST(uri, non_empty_description)
{
  PARSE_URI("credit:" + test_address() + "?tx_description=foo", true);
  ASSERT_EQ(description, "foo");
}

TEST(uri, non_empty_recipient_name)
{
  PARSE_URI("credit:" + test_address() + "?recipient_name=foo", true);
  ASSERT_EQ(recipient_name, "foo");
}

TEST(uri, url_encoding)
{
  PARSE_URI("credit:" + test_address() + "?tx_description=foo%20bar", true);
  ASSERT_EQ(description, "foo bar");
}

TEST(uri, non_alphanumeric_url_encoding)
{
  PARSE_URI("credit:" + test_address() + "?tx_description=foo%2x", true);
  ASSERT_EQ(description, "foo%2x");
}

TEST(uri, truncated_url_encoding)
{
  PARSE_URI("credit:" + test_address() + "?tx_description=foo%2", true);
  ASSERT_EQ(description, "foo%2");
}

TEST(uri, percent_without_url_encoding)
{
  PARSE_URI("credit:" + test_address() + "?tx_description=foo%", true);
  ASSERT_EQ(description, "foo%");
}

TEST(uri, url_encoded_once)
{
  PARSE_URI("credit:" + test_address() + "?tx_description=foo%2020", true);
  ASSERT_EQ(description, "foo 20");
}

