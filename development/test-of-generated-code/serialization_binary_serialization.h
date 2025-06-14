#pragma once

#include <vector>
#include <cstdint>

namespace Serialization
{
  class BinarySerializer
  {
    public:
      const std::vector<uint8_t>& getSerializedData() const
      {
        return m_serialized_data;
      }

      void storeByte(uint8_t byte)
      {
        m_serialized_data.push_back(byte);
      }

      template <class INTEGER> void storeInteger(const INTEGER& value)
      {
        unsigned len = sizeof(INTEGER);
        if constexpr (std::endian::native == std::endian::big)
        {
          // Big-endian system
          uint8_t* bytes = reinterpret_cast<const uint8_t*>(&value);
          while (len--)
          {
            storeByte(*bytes++);
          }
        }
        else
        {
          // Little endian system
          const uint8_t* bytes = reinterpret_cast<const uint8_t*>(&value) + len;
          while (len--)
          {
            storeByte(*--bytes);
          }
        }
      }

  private:
      std::vector<uint8_t> m_serialized_data;
  };

  class BinaryDeserializer
  {
    public:
      BinaryDeserializer(const std::vector<uint8_t>& m_serialized_data)
        : m_serialized_data_reader(m_serialized_data.begin())
        , m_serialized_data_end(m_serialized_data.end())
      {  }

      bool is_end() const
      {
        return (m_serialized_data_reader == m_serialized_data_end);
      }

      void readByte(uint8_t& byte)
      {
        if (m_serialized_data_reader != m_serialized_data_end)
        {
          byte = *m_serialized_data_reader++;
        }  
      }

      template <class INTEGER> void readInteger(INTEGER& value)
      {
        unsigned len = sizeof(INTEGER);
        if constexpr (std::endian::native == std::endian::big)
        {
          // Big-endian system
          uint8_t* bytes = reinterpret_cast<uint8_t*>(&value);
          for (unsigned i = 0; i < sizeof(INTEGER); ++i)
          {
            readByte(*bytes++);
          }
        }
        else
        {
          // Little endian system
          uint8_t* bytes = reinterpret_cast<uint8_t*>(&value) + len;
          while (len--)
          {
            readByte(*--bytes);
          }
        }
      }
  
  private:
      std::vector<uint8_t>::const_iterator m_serialized_data_reader;
      std::vector<uint8_t>::const_iterator m_serialized_data_end;
  };
};
