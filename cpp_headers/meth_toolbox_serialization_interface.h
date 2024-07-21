// -----------------------------------------------------------------
// (c) WGan mataprogram code generator - data_types
// -----------------------------------------------------------------
// Serailizer interface - when providing data for serialization
// of data objects (and messages) implement this interface to store
// data from serialized object
// -----------------------------------------------------------------
#pragma once

#include <cstdint>
#include <bit>

namespace MethToolbox
{
  class SerializationInterface
  {
    public:
      virtual ~SerializationInterface()
      {  }

      virtual void putByte(uint8_t byte) = 0;

      template <class INTEGER> void serializeInteger(const INTEGER& value)
      {
        if constexpr (std::endian::native == std::endian::big)
        {
          // Big-endian system
          uint8_t* bytes = reinterpret_cast<const uint8_t*>(&value);
          for (unsigned i = 0; i < sizeof(INTEGER); ++i)
          {
              putByte(bytes[i]);
          }
        }
        else
        {
          // Little endian system
          unsigned len = sizeof(INTEGER);
          const uint8_t* bytes = reinterpret_cast<const uint8_t*>(&value) + len - 1;
          while (len)
          {
            putByte(*bytes);
            --bytes;
            --len;
          }
        }
      }
  };
}
