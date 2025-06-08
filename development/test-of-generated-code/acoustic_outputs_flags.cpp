#include <sstream>

#include "acoustic_outputs_flags.h"
#include "common_conversion_error.h"

namespace Acoustic
{
  std::string OutputsFlags::toString() const
  {
    std::ostringstream string_representation;
    string_representation << *this;
    return string_representation.str();
  }

  OutputsFlags OutputsFlags::fromString(std::string text)
  {
    OutputsFlags output_flags;
    if (text == "" || text == "NONE")
    {
      return output_flags;
    }
    else
    {
      for (size_t separator_position = text.find_first_of("|"); 
           separator_position != std::string::npos; 
           separator_position = text.find_first_of("|"))
      {
        output_flags |= OutputsFlags::convertTextToSingleFlag(text.substr(0, separator_position));
        text = text.substr(separator_position + 1);
      }
      output_flags |= OutputsFlags::convertTextToSingleFlag(text);
      return output_flags;
    }
  }

  std::ostream& operator<<(std::ostream& output, const OutputsFlags& outputs_flags)
  {
    if (outputs_flags.m_outputs_flags)
    {
      const char* separator = "";
      uint8_t string_index = 0;
      for (uint8_t mask = OutputsFlags::first_flag_value; mask <= OutputsFlags::last_flag_value; mask *= 2, ++string_index)
      {
        if (mask & outputs_flags.m_outputs_flags)
        {
          output << separator << OutputsFlags::m_acoustic_outputs_names[string_index];
          separator = "|";
        }
      }
    }
    else
    {
      output << "NONE";
    }
    return output;
  }

  Serialization::BinarySerializer& operator<<(Serialization::BinarySerializer& output, const OutputsFlags& outputs_flags)
  {
    output.storeInteger(outputs_flags.m_outputs_flags);
    return output;
  }

  Serialization::BinaryDeserializer& operator>>(Serialization::BinaryDeserializer& input, OutputsFlags& outputs_flags)
  {
    input.readInteger(outputs_flags.m_outputs_flags);
    return input;
  }

  const char* OutputsFlags::m_acoustic_outputs_names[] = {
    "AUDIO_INPUT_L",
    "AUDIO_INPUT_R",
    "RADIO_TRAMSMIT",
    "DRIVER_SPEAKER",
    "DRIVER_HANDPHONE",
    "CABIN_INNER_SPEAKER",
    "VEHICLE_OUTHER_SPEAKER"
  };

  OutputsFlags::Output OutputsFlags::convertTextToSingleFlag(const std::string& text)
  {
    if (text == "AUDIO_INPUT_L")
    {
      return E_AUDIO_INPUT_L;
    }
    if (text == "AUDIO_INPUT_R")
    {
      return E_AUDIO_INPUT_R;
    }
    if (text == "RADIO_TRAMSMIT")
    {
      return E_RADIO_TRAMSMIT;
    }
    if (text == "DRIVER_SPEAKER")
    {
      return E_DRIVER_SPEAKER;
    }
    if (text == "DRIVER_HANDPHONE")
    {
      return E_DRIVER_HANDPHONE;
    }
    if (text == "CABIN_INNER_SPEAKER")
    {
      return E_CABIN_INNER_SPEAKER;
    }
    if (text == "VEHICLE_OUTHER_SPEAKER")
    {
      return E_VEHICLE_OUTHER_SPEAKER;
    }
    throw Common::ConversionError(text, "cannot be interpreted as Acoustic::OutputsFlags::Output");
  }
}
