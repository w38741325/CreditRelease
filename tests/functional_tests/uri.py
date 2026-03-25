#!/usr/bin/env python3
#encoding=utf-8

# Copyright (c) 2019-2024, The Monero Project
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of
#    conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list
#    of conditions and the following disclaimer in the documentation and/or other
#    materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be
#    used to endorse or promote products derived from this software without specific
#    prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
# THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Test URI RPC"""

try:
  from urllib import quote as urllib_quote
except:
  from urllib.parse import quote as urllib_quote

import credit_fixtures as fixtures

from framework.wallet import Wallet


class URITest():
    def run_test(self):
      self.create()
      self.test_credit_uri()

    def create(self):
        print('Creating wallet')
        wallet = Wallet()
        # close the wallet if any, will throw if none is loaded
        try:
            wallet.close_wallet()
        except:
            pass
        res = wallet.restore_deterministic_wallet(seed=fixtures.SEED)
        assert res.address == fixtures.PRIMARY_ADDRESS
        assert res.seed == fixtures.SEED

    def test_credit_uri(self):
        print('Testing credit: URI')
        wallet = Wallet()

        utf8string = [u'ãˆã‚“ã—ã‚…ã†', u'ã‚ã¾ã‚„ã‹ã™']
        quoted_utf8string = [urllib_quote(x.encode('utf8')) for x in utf8string]

        ok = False
        try:
            res = wallet.make_uri()
        except:
            ok = True
        assert ok
        ok = False
        try:
            res = wallet.make_uri(address='')
        except:
            ok = True
        assert ok
        ok = False
        try:
            res = wallet.make_uri(address='kjshdkj')
        except:
            ok = True
        assert ok

        for address in fixtures.URI_ADDRESSES:
            res = wallet.make_uri(address=address)
            assert res.uri == fixtures.URI_SCHEME + address
            res = wallet.parse_uri(res.uri)
            assert res.uri.address == address
            assert res.uri.payment_id == ''
            assert res.uri.amount == 0
            assert res.uri.tx_description == ''
            assert res.uri.recipient_name == ''
            assert not 'unknown_parameters' in res or len(res.unknown_parameters) == 0
            res = wallet.make_uri(address=address, amount=11000000000)
            assert res.uri == fixtures.URI_SCHEME + address + '?tx_amount=0.011' or res.uri == fixtures.URI_SCHEME + address + '?tx_amount=0.011000000000'
            res = wallet.parse_uri(res.uri)
            assert res.uri.address == address
            assert res.uri.payment_id == ''
            assert res.uri.amount == 11000000000
            assert res.uri.tx_description == ''
            assert res.uri.recipient_name == ''
            assert not 'unknown_parameters' in res or len(res.unknown_parameters) == 0

        address = fixtures.PRIMARY_ADDRESS

        res = wallet.make_uri(address=address, tx_description=utf8string[0])
        assert res.uri == fixtures.URI_SCHEME + address + '?tx_description=' + quoted_utf8string[0]
        res = wallet.parse_uri(res.uri)
        assert res.uri.address == address
        assert res.uri.payment_id == ''
        assert res.uri.amount == 0
        assert res.uri.tx_description == utf8string[0]
        assert res.uri.recipient_name == ''
        assert not 'unknown_parameters' in res or len(res.unknown_parameters) == 0

        res = wallet.make_uri(address=address, recipient_name=utf8string[0])
        assert res.uri == fixtures.URI_SCHEME + address + '?recipient_name=' + quoted_utf8string[0]
        res = wallet.parse_uri(res.uri)
        assert res.uri.address == address
        assert res.uri.payment_id == ''
        assert res.uri.amount == 0
        assert res.uri.tx_description == ''
        assert res.uri.recipient_name == utf8string[0]
        assert not 'unknown_parameters' in res or len(res.unknown_parameters) == 0

        res = wallet.make_uri(address=address, recipient_name=utf8string[0], tx_description=utf8string[1])
        assert res.uri == fixtures.URI_SCHEME + address + '?recipient_name=' + quoted_utf8string[0] + '&tx_description=' + quoted_utf8string[1]
        res = wallet.parse_uri(res.uri)
        assert res.uri.address == address
        assert res.uri.payment_id == ''
        assert res.uri.amount == 0
        assert res.uri.tx_description == utf8string[1]
        assert res.uri.recipient_name == utf8string[0]
        assert not 'unknown_parameters' in res or len(res.unknown_parameters) == 0

        res = wallet.make_uri(address=address, recipient_name=utf8string[0], tx_description=utf8string[1], amount=1000000000000)
        assert res.uri == fixtures.URI_SCHEME + address + '?tx_amount=1.000000000000&recipient_name=' + quoted_utf8string[0] + '&tx_description=' + quoted_utf8string[1]
        res = wallet.parse_uri(res.uri)
        assert res.uri.address == address
        assert res.uri.payment_id == ''
        assert res.uri.amount == 1000000000000
        assert res.uri.tx_description == utf8string[1]
        assert res.uri.recipient_name == utf8string[0]
        assert not 'unknown_parameters' in res or len(res.unknown_parameters) == 0

        # external payment ids are not supported anymore
        ok = False
        try:
            res = wallet.make_uri(address=address, recipient_name=utf8string[0], tx_description=utf8string[1], amount=1000000000000, payment_id='1' * 64)
        except:
            ok = True
        assert ok

        # spaces must be encoded as %20
        res = wallet.make_uri(address=address, tx_description=' ' + utf8string[1] + ' ' + utf8string[0] + ' ', amount=1000000000000)
        assert res.uri == fixtures.URI_SCHEME + address + '?tx_amount=1.000000000000&tx_description=%20' + quoted_utf8string[1] + '%20' + quoted_utf8string[0] + '%20'
        res = wallet.parse_uri(res.uri)
        assert res.uri.address == address
        assert res.uri.payment_id == ''
        assert res.uri.amount == 1000000000000
        assert res.uri.tx_description == ' ' + utf8string[1] + ' ' + utf8string[0] + ' '
        assert res.uri.recipient_name == ''
        assert not 'unknown_parameters' in res or len(res.unknown_parameters) == 0

        # the example from the docs
        res = wallet.parse_uri(fixtures.URI_SCHEME + fixtures.SECONDARY_ADDRESS + '?tx_amount=239.39014&tx_description=donation')
        assert res.uri.address == fixtures.SECONDARY_ADDRESS
        assert res.uri.amount == 239390140000000
        assert res.uri.tx_description == 'donation'
        assert res.uri.recipient_name == ''
        assert res.uri.payment_id == ''
        assert not 'unknown_parameters' in res or len(res.unknown_parameters) == 0

        # malformed/invalid
        for uri in [
            '',
            ':',
            'credit',
            'notcredit:' + fixtures.PRIMARY_ADDRESS,
            'CREDIT:' + fixtures.PRIMARY_ADDRESS,
            'CREDIT::' + fixtures.PRIMARY_ADDRESS,
            'credit:',
            'credit:badaddress',
            'credit:tx_amount=10',
            'credit:?tx_amount=10',
            fixtures.URI_SCHEME + fixtures.PRIMARY_ADDRESS + '?tx_amount=-1',
            fixtures.URI_SCHEME + fixtures.PRIMARY_ADDRESS + '?tx_amount=1e12',
            fixtures.URI_SCHEME + fixtures.PRIMARY_ADDRESS + '?tx_amount=+12',
            fixtures.URI_SCHEME + fixtures.PRIMARY_ADDRESS + '?tx_amount=1+2',
            fixtures.URI_SCHEME + fixtures.PRIMARY_ADDRESS + '?tx_amount=A',
            fixtures.URI_SCHEME + fixtures.PRIMARY_ADDRESS + '?tx_amount=0x2',
            fixtures.URI_SCHEME + fixtures.PRIMARY_ADDRESS + '?tx_amount=222222222222222222222',
            fixtures.URI_SCHEME + fixtures.BAD_PRIMARY_ADDRESS + '?tx_amount=10',
            fixtures.URI_SCHEME + fixtures.PRIMARY_ADDRESS + '&',
            fixtures.URI_SCHEME + fixtures.PRIMARY_ADDRESS + '&tx_amount',
            fixtures.URI_SCHEME + fixtures.PRIMARY_ADDRESS + '&tx_amount=',
            fixtures.URI_SCHEME + fixtures.PRIMARY_ADDRESS + '&tx_amount=10=',
            fixtures.URI_SCHEME + fixtures.PRIMARY_ADDRESS + '&tx_amount=10=&',
            fixtures.URI_SCHEME + fixtures.PRIMARY_ADDRESS + '&tx_amount=10=&foo=bar',
            fixtures.URI_SCHEME + fixtures.PRIMARY_ADDRESS + '?tx_amount=10&tx_amount=20',
            fixtures.URI_SCHEME + fixtures.PRIMARY_ADDRESS + '?tx_payment_id=1111111111111111',
            fixtures.URI_SCHEME + fixtures.PRIMARY_INTEGRATED_ADDRESS + '?tx_payment_id=' + '1' * 64,
        ] + [fixtures.URI_SCHEME + address for address in fixtures.URI_INVALID_NETWORK_ADDRESSES]:
            ok = False
            try:
                res = wallet.parse_uri(uri)
            except:
                ok = True
            assert ok, res

        # unknown parameters but otherwise valid
        res = wallet.parse_uri(fixtures.URI_SCHEME + address + '?tx_amount=239.39014&foo=bar')
        assert res.uri.address == address
        assert res.uri.amount == 239390140000000
        assert res.unknown_parameters == ['foo=bar'], res
        res = wallet.parse_uri(fixtures.URI_SCHEME + address + '?tx_amount=239.39014&foo=bar&baz=quux')
        assert res.uri.address == address
        assert res.uri.amount == 239390140000000
        assert res.unknown_parameters == ['foo=bar', 'baz=quux'], res
        res = wallet.parse_uri(fixtures.URI_SCHEME + address + '?tx_amount=239.39014&%20=%20')
        assert res.uri.address == address
        assert res.uri.amount == 239390140000000
        assert res.unknown_parameters == ['%20=%20'], res
        res = wallet.parse_uri(fixtures.URI_SCHEME + address + '?tx_amount=239.39014&unknown=' + quoted_utf8string[0])
        assert res.uri.address == address
        assert res.uri.amount == 239390140000000
        assert res.unknown_parameters == [u'unknown=' + quoted_utf8string[0]], res


if __name__ == '__main__':
    URITest().run_test()
