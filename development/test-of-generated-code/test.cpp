#include "gtest/gtest.h"

#include "acoustic_selected_output_ids.h"
#include "common_severity.h"
#include "common_conversion_error.h"

//--------------------------------------------------------------------------------------------

TEST(TestOfGeneratedEnumType, TestOfSettingValue)
{
  Common::Severity severity;
  ASSERT_EQ(severity, Common::INFO);
  severity = Common::ARMAGEDON;
  ASSERT_EQ(severity, Common::ARMAGEDON);
}

TEST(TestOfGeneratedEnumType, TestOfDumpingToString1)
{
  Common::Severity severity;
  ASSERT_EQ(severity.toString(), "INFO");
}

TEST(TestOfGeneratedEnumType, TestOfDumpingToString2)
{
  Common::Severity severity(Common::ARMAGEDON);
  ASSERT_EQ(severity.toString(), "ARMAGEDON");
}

TEST(TestOfGeneratedEnumType, TestOfCreationFromString1)
{
  Common::Severity severity = Common::Severity::fromString("ERROR");
  ASSERT_EQ(severity.toString(), "ERROR");
}

TEST(TestOfGeneratedEnumType, TestOfCreationFromStringError)
{
  ASSERT_THROW(Common::Severity::fromString("NOONE"), Common::ConversionError);
}

TEST(TestOfGeneratedEnumType, TestOfSerialization)
{
  Serialization::BinarySerializer serializer;
  Common::Severity severity(Common::PROBLEM);
  serializer << severity;
  const std::vector<uint8_t>& serialized_data = serializer.getSerializedData();
  ASSERT_EQ(serialized_data.size(), 1);
  ASSERT_EQ(serialized_data[0], 0x08);
}

TEST(TestOfGeneratedEnumType, TestOfDeserialization)
{
  std::vector<uint8_t> serialized_data = { 0x08 };
  Serialization::BinaryDeserializer deserializer(serialized_data);
  Common::Severity severity;
  deserializer >> severity;
  ASSERT_EQ(severity, Common::PROBLEM);
}

//--------------------------------------------------------------------------------------------

TEST(TestOfGeneratedBitflagsType, TestOfBuildingBitflag)
{
  Acoustic::SelectedOutputIds flags;
  flags |= Acoustic::RADIO_TRANSMIT;
  flags |= Acoustic::DRIVER_HANDPHONE;
  flags |= Acoustic::AUDIO_INPUT_L;
  ASSERT_EQ(flags, Acoustic::AUDIO_INPUT_L | Acoustic::RADIO_TRANSMIT | Acoustic::DRIVER_HANDPHONE);
  ASSERT_NE(flags, Acoustic::AUDIO_INPUT_L | Acoustic::DRIVER_HANDPHONE);
}

TEST(TestOfGeneratedBitflagsType, TestOfDumpingToString1)
{
  Acoustic::SelectedOutputIds flags;
  flags |= Acoustic::RADIO_TRANSMIT;
  flags |= Acoustic::DRIVER_HANDPHONE;
  flags |= Acoustic::VEHICLE_OUTHER_SPEAKER;
  ASSERT_EQ(flags.toString(), "RADIO_TRANSMIT|DRIVER_HANDPHONE|VEHICLE_OUTHER_SPEAKER");
}

TEST(TestOfGeneratedBitflagsType, TestOfDumpingToString2)
{
  Acoustic::SelectedOutputIds flags2;
  ASSERT_EQ(flags2.toString(), "NONE");
}

TEST(TestOfGeneratedBitflagsType, TestOfCreationFromString1)
{
  Acoustic::SelectedOutputIds flags1 = Acoustic::SelectedOutputIds::fromString("RADIO_TRANSMIT|DRIVER_HANDPHONE|VEHICLE_OUTHER_SPEAKER");
  ASSERT_EQ(flags1.toString(), "RADIO_TRANSMIT|DRIVER_HANDPHONE|VEHICLE_OUTHER_SPEAKER");
}

TEST(TestOfGeneratedBitflagsType, TestOfCreationFromString2)
{
  Acoustic::SelectedOutputIds flags1 = Acoustic::SelectedOutputIds::fromString("NONE");
  ASSERT_EQ(flags1.toString(), "NONE");
}

TEST(TestOfGeneratedBitflagsType, TestOfCreationFromStringError1)
{
  ASSERT_THROW(Acoustic::SelectedOutputIds::fromString("VEHICLE_ALL_SPEAKERS"), Common::ConversionError);
}

TEST(TestOfGeneratedBitflagsType, TestOfCreationFromStringError2)
{
  ASSERT_THROW(Acoustic::SelectedOutputIds::fromString("A"), Common::ConversionError);
}

TEST(TestOfGeneratedBitflagsType, TestOfCreationFromString3)
{
  Acoustic::SelectedOutputIds flags1 = Acoustic::SelectedOutputIds::fromString("DRIVER_HANDPHONE");
  ASSERT_EQ(flags1.toString(), "DRIVER_HANDPHONE");
}

TEST(TestOfGeneratedBitflagsType, TestOfMasking)
{
  Acoustic::SelectedOutputIds flags = Acoustic::RADIO_TRANSMIT | Acoustic::DRIVER_HANDPHONE | Acoustic::CABIN_INNER_SPEAKER;
  flags &= !Acoustic::DRIVER_HANDPHONE;
  ASSERT_EQ(flags, Acoustic::RADIO_TRANSMIT | Acoustic::CABIN_INNER_SPEAKER);
}

TEST(TestOfGeneratedBitflagsType, TestOfErasingFlag)
{
  Acoustic::SelectedOutputIds flags = Acoustic::RADIO_TRANSMIT | Acoustic::DRIVER_HANDPHONE | Acoustic::CABIN_INNER_SPEAKER;
  flags.removeSelectedOutputIds(Acoustic::DRIVER_HANDPHONE | Acoustic::CABIN_INNER_SPEAKER);
  ASSERT_EQ(flags, Acoustic::RADIO_TRANSMIT);
}

TEST(TestOfGeneratedBitflagsType, TestOfCheckingFlags)
{
  Acoustic::SelectedOutputIds flags = Acoustic::RADIO_TRANSMIT | Acoustic::DRIVER_HANDPHONE | Acoustic::CABIN_INNER_SPEAKER;
  ASSERT_TRUE(flags.isAnyOfSelectedOutputIds(Acoustic::DRIVER_HANDPHONE | Acoustic::AUDIO_INPUT_R));
  ASSERT_FALSE(flags.hasAllOfSelectedOutputIds(Acoustic::DRIVER_HANDPHONE | Acoustic::AUDIO_INPUT_R));
  ASSERT_TRUE(flags.hasAllOfSelectedOutputIds(Acoustic::DRIVER_HANDPHONE | Acoustic::CABIN_INNER_SPEAKER));
  ASSERT_FALSE(flags.isAnyOfSelectedOutputIds(Acoustic::AUDIO_INPUT_R | Acoustic::VEHICLE_OUTHER_SPEAKER));
}

TEST(TestOfGeneratedBitflagsType, TestOfSerialization)
{
  Acoustic::SelectedOutputIds flags = Acoustic::RADIO_TRANSMIT | Acoustic::DRIVER_HANDPHONE | Acoustic::CABIN_INNER_SPEAKER;
  Serialization::BinarySerializer serializer;
  serializer << flags;
  const std::vector<uint8_t>& serialized_data = serializer.getSerializedData();
  ASSERT_EQ(serialized_data.size(), 1);
  ASSERT_EQ(serialized_data[0], 0x2c);
}

TEST(TestOfGeneratedBitflagsType, TestOfDeserialization)
{
  std::vector<uint8_t> serialized_data = { 0x2c };
  Serialization::BinaryDeserializer deserializer(serialized_data);
  Acoustic::SelectedOutputIds flags;
  deserializer >> flags;
  ASSERT_EQ(flags, Acoustic::RADIO_TRANSMIT | Acoustic::DRIVER_HANDPHONE | Acoustic::CABIN_INNER_SPEAKER);
}

//--------------------------------------------------------------------------------------------
