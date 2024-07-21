// -----------------------------------------------------------------
// (c) WGan mataprogram code generator - data_types
// -----------------------------------------------------------------
// Deserailizer interface - when providing data for deserialization
// of data objects (and messages) implement this interface to allow
// deserialization of all generated clesses.
// -----------------------------------------------------------------

#pragma once

#include <cstdint>
#include <bit>

namespace MethToolbox
{
  class DeserializationInterface
  {
    public:
      virtual ~DeserializationInterface()
      {  }

      virtual uint8_t getByte() = 0;

      template <class INTEGER> void deserializeInteger(INTEGER& value)
      {
        if constexpr (std::endian::native == std::endian::big)
        {
          // Big-endian system
          uint8_t* bytes = reinterpret_cast<uint8_t*>(&value);
          for (unsigned i = 0; i < sizeof(INTEGER); ++i)
          {
              bytes[i] = getByte();
          }
        }
        else
        {
          // Little endian system
          unsigned len = sizeof(INTEGER);
          uint8_t* bytes = reinterpret_cast<uint8_t*>(&value) + len - 1;
          while (len)
          {
            *bytes = getByte();
            --bytes;
            --len;
          }
        }
      }
  };
};
