#include "blocks.h"

#include <unordered_map>

namespace blocks
{

  const std::unordered_map<cryptonote::network_type, const epee::span<const unsigned char>, std::hash<size_t>> CheckpointsByNetwork = {
    {cryptonote::network_type::MAINNET, {}},
    {cryptonote::network_type::STAGENET, {}},
    {cryptonote::network_type::TESTNET, {}}
  };

  const epee::span<const unsigned char> GetCheckpointsData(cryptonote::network_type network)
  {
    const auto it = CheckpointsByNetwork.find(network);
    if (it != CheckpointsByNetwork.end())
    {
      return it->second;
    }
    return nullptr;
  }

}
