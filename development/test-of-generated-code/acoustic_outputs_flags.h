#pragma once

#include <cstdint>
#include <string>
#include <iostream>

#include "binary_serialization.h"

namespace Acoustic
{
  class OutputsFlags
  {
    public:
      // type traits
      static constexpr const char* class_name = { "Acoustinc::OutputsFlags" };
      static constexpr bool is_compareable = { true };
      static constexpr bool is_ordered = { false };
      static constexpr bool size_in_bytes = { 1 };
      static constexpr uint8_t first_flag_value = { 0x01 };
      static constexpr uint8_t last_flag_value = { 0x40 } ;

      // flags values (internal)
      enum Output {
        E_AUDIO_INPUT_L          = 0x01,
        E_AUDIO_INPUT_R          = 0x02,
        E_RADIO_TRAMSMIT         = 0x04,
        E_DRIVER_SPEAKER         = 0x08,
        E_DRIVER_HANDPHONE       = 0x10,
        E_CABIN_INNER_SPEAKER    = 0x20,
        E_VEHICLE_OUTHER_SPEAKER = 0x40
      };

      OutputsFlags()
        : m_outputs_flags(0)
      {  }

      OutputsFlags(OutputsFlags::Output output)
        : m_outputs_flags(output)
      {  }

      OutputsFlags(const OutputsFlags& outputs_flags)
        : m_outputs_flags(outputs_flags.m_outputs_flags)
      {  }

      OutputsFlags& operator=(const OutputsFlags& outputs_flags)
      {
        m_outputs_flags = outputs_flags.m_outputs_flags;
        return *this;
      }

      OutputsFlags operator|=(const OutputsFlags& outputs_flags)
      {
        m_outputs_flags |= outputs_flags.m_outputs_flags;
        return *this;
      }

      OutputsFlags operator|(const OutputsFlags& outputs_flags) const
      {
        return OutputsFlags(m_outputs_flags | outputs_flags.m_outputs_flags);
      }

      OutputsFlags operator&=(const OutputsFlags& outputs_flags)
      {
        m_outputs_flags &= outputs_flags.m_outputs_flags;
        return *this;
      }

      OutputsFlags operator&(const OutputsFlags& outputs_flags) const
      {
        return OutputsFlags(m_outputs_flags & outputs_flags.m_outputs_flags);
      }

      OutputsFlags operator!() const
      {
        return OutputsFlags(m_outputs_flags ^ (2 * last_flag_value - 1));
      }

      bool operator==(const OutputsFlags& outputs_flags) const
      {
        return (m_outputs_flags == outputs_flags.m_outputs_flags);
      }

      bool operator!=(const OutputsFlags& outputs_flags) const
      {
        return (m_outputs_flags != outputs_flags.m_outputs_flags);
      }
       
      bool isAnyOf(const OutputsFlags& outputs_flags) const
      {
        return (outputs_flags.m_outputs_flags & m_outputs_flags);
      }

      bool hasAllOf(const OutputsFlags& outputs_flags) const
      {
        return (outputs_flags.m_outputs_flags & m_outputs_flags) == outputs_flags.m_outputs_flags;
      }

      void remove(const OutputsFlags& outputs_flags)
      {
        m_outputs_flags &= ~outputs_flags.m_outputs_flags;
      }

      std::string toString() const;
      static OutputsFlags fromString(std::string text);

      friend std::ostream& operator<<(std::ostream& output, const OutputsFlags& outputs_flags);

      friend Serialization::BinarySerializer& operator<<(Serialization::BinarySerializer& output, const OutputsFlags& outputs_flags);
      friend Serialization::BinaryDeserializer& operator>>(Serialization::BinaryDeserializer& input, OutputsFlags& outputs_flags);

    private:
      uint8_t m_outputs_flags;

      static const char* m_acoustic_outputs_names[];

      OutputsFlags(uint8_t acoustic_outputs)
        : m_outputs_flags(acoustic_outputs)
      {  }

      static Output convertTextToSingleFlag(const std::string& text);
  };
}

// constants-like definitinos to allow simple use of Acoustic::OutputsFlags bitflags 
#define AUDIO_INPUT_L Acoustic::OutputsFlags(Acoustic::OutputsFlags::E_AUDIO_INPUT_L)
#define AUDIO_INPUT_R Acoustic::OutputsFlags(Acoustic::OutputsFlags::E_AUDIO_INPUT_R)
#define RADIO_TRAMSMIT Acoustic::OutputsFlags(Acoustic::OutputsFlags::E_RADIO_TRAMSMIT)
#define DRIVER_SPEAKER Acoustic::OutputsFlags(Acoustic::OutputsFlags::E_DRIVER_SPEAKER)
#define DRIVER_HANDPHONE Acoustic::OutputsFlags(Acoustic::OutputsFlags::E_DRIVER_HANDPHONE)
#define CABIN_INNER_SPEAKER Acoustic::OutputsFlags(Acoustic::OutputsFlags::E_CABIN_INNER_SPEAKER)
#define VEHICLE_OUTHER_SPEAKER Acoustic::OutputsFlags(Acoustic::OutputsFlags::E_VEHICLE_OUTHER_SPEAKER)
