#include "gtest/gtest.h"

#include "acoustic_selected_output_ids.h"
#include "common_severity.h"
#include "common_conversion_error.h"
#include "common_network_port_number.h"
#include "test_just_a_record.h"
#include "test_another_record.h"

//--------------------------------------------------------------------------------------------

TEST(TestOfGeneratedRecordType, TestOfDefaultValue)
{
  ::Test::JustARecord record;
  ASSERT_EQ(record.getSeverityAsEnum(), Common::Severity::E_INFO);
  ASSERT_EQ(record.getSelectedOutputIdsAsInt(), 0);
  ASSERT_EQ(record.getPortNumberAsInt(), 0);
}

TEST(TestOfGeneratedRecordType, TestOfConstructingValue)
{
  ::Test::JustARecord record(Common::ARMAGEDON, Acoustic::AUDIO_INPUT_L | Acoustic::AUDIO_INPUT_R, Common::Network::PortNumber(8099));
  ASSERT_EQ(record.getSeverityAsEnum(), Common::Severity::E_ARMAGEDON);
  ASSERT_EQ(record.getSelectedOutputIdsAsInt(), 3);
  ASSERT_EQ(record.getPortNumberAsInt(), 8099);
}

TEST(TestOfGeneratedRecordType, TestConvertingToString)
{
  ::Test::JustARecord record1(Common::ARMAGEDON, Acoustic::AUDIO_INPUT_L | Acoustic::AUDIO_INPUT_R, Common::Network::PortNumber(8099));
  ASSERT_EQ(record1.toString(), "{ common_severity: ARMAGEDON, acoustic_selected_output_ids: AUDIO_INPUT_L|AUDIO_INPUT_R, common_network_port_number: 8099 }");
  ::Test::JustARecord record2;
  ASSERT_EQ(record2.toString(), "{ common_severity: INFO, acoustic_selected_output_ids: NONE, common_network_port_number: 0 }");
}

TEST(TestOfGeneratedRecordType, TestSettingFieldsValues)
{
  ::Test::JustARecord record(Common::ARMAGEDON, Acoustic::AUDIO_INPUT_L | Acoustic::AUDIO_INPUT_R, Common::Network::PortNumber(8099));

  record.setPortNumber(997);
  record |= Acoustic::DRIVER_SPEAKER;

  ASSERT_EQ(record.toString(), "{ common_severity: ARMAGEDON, acoustic_selected_output_ids: AUDIO_INPUT_L|AUDIO_INPUT_R|DRIVER_SPEAKER, common_network_port_number: 997 }");
}

TEST(TestOfGeneratedRecordType, TestSettingFromSimpleValues)
{
  ::Test::JustARecord record(Common::ARMAGEDON, Acoustic::AUDIO_INPUT_L | Acoustic::AUDIO_INPUT_R, Common::Network::PortNumber(8099));

  record.setFrom(Acoustic::DRIVER_HANDPHONE | Acoustic::CABIN_INNER_SPEAKER);
  record.setFrom(Common::Network::PortNumber(1025));

  ASSERT_EQ(record.toString(), "{ common_severity: ARMAGEDON, acoustic_selected_output_ids: DRIVER_HANDPHONE|CABIN_INNER_SPEAKER, common_network_port_number: 1025 }");
}

TEST(TestOfGeneratedRecordType, TestSettingFromRecord1)
{
  ::Test::JustARecord record1(Common::ARMAGEDON, Acoustic::AUDIO_INPUT_L | Acoustic::AUDIO_INPUT_R, Common::Network::PortNumber(8099));
  ::Test::AnotherRecord record2(Common::ERROR, Common::Network::PortNumber(555));

  record1.setFrom(record2);

  ASSERT_EQ(record1.toString(), "{ common_severity: ERROR, acoustic_selected_output_ids: AUDIO_INPUT_L|AUDIO_INPUT_R, common_network_port_number: 555 }");
}

TEST(TestOfGeneratedRecordType, TestSettingFromRecord2)
{
  ::Test::JustARecord record1(Common::ARMAGEDON, Acoustic::AUDIO_INPUT_L | Acoustic::AUDIO_INPUT_R, Common::Network::PortNumber(8099));
  ::Test::AnotherRecord record2(Common::ERROR, Common::Network::PortNumber(555));

  record2.setFrom(record1);

  ASSERT_EQ(record2.toString(), "{ common_severity: ARMAGEDON, common_network_port_number: 8099 }");
}

TEST(TestOfGeneratedRecordType, TestOfComparision1)
{
  ::Test::JustARecord record1(Common::ARMAGEDON, Acoustic::AUDIO_INPUT_L | Acoustic::AUDIO_INPUT_R, Common::Network::PortNumber(8099));
  ::Test::JustARecord record2(Common::ARMAGEDON, Acoustic::AUDIO_INPUT_L | Acoustic::AUDIO_INPUT_R, Common::Network::PortNumber(8099));
  ASSERT_TRUE(record1 == record2);
  ASSERT_FALSE(record1 != record2);
  ASSERT_TRUE(record1 >= record2);
  ASSERT_FALSE(record1 > record2);
  ASSERT_TRUE(record1 <= record2);
  ASSERT_FALSE(record1 < record2);
}

TEST(TestOfGeneratedRecordType, TestOfComparision2)
{
  ::Test::JustARecord record1(Common::ARMAGEDON, Acoustic::AUDIO_INPUT_L | Acoustic::AUDIO_INPUT_R, Common::Network::PortNumber(8099));
  ::Test::JustARecord record2(Common::ARMAGEDON, Acoustic::AUDIO_INPUT_L | Acoustic::AUDIO_INPUT_R, Common::Network::PortNumber(9088));
  ASSERT_FALSE(record1 == record2);
  ASSERT_TRUE(record1 != record2);
  ASSERT_FALSE(record1 >= record2);
  ASSERT_FALSE(record1 > record2);
  ASSERT_TRUE(record1 <= record2);
  ASSERT_TRUE(record1 < record2);
}

TEST(TestOfGeneratedRecordType, TestOfComparision3)
{
  ::Test::JustARecord record1(Common::ARMAGEDON, Acoustic::AUDIO_INPUT_L | Acoustic::AUDIO_INPUT_R, Common::Network::PortNumber(8099));
  ::Test::JustARecord record2(Common::LOG, Acoustic::AUDIO_INPUT_L | Acoustic::AUDIO_INPUT_R, Common::Network::PortNumber(9088));
  ASSERT_FALSE(record1 == record2);
  ASSERT_TRUE(record1 != record2);
  ASSERT_TRUE(record1 >= record2);
  ASSERT_TRUE(record1 > record2);
  ASSERT_FALSE(record1 <= record2);
  ASSERT_FALSE(record1 < record2);
}

TEST(TestOfGeneratedRecordType, TestOfComparision4)
{
  ::Test::JustARecord record1(Common::ARMAGEDON, Acoustic::AUDIO_INPUT_L | Acoustic::AUDIO_INPUT_R, Common::Network::PortNumber(8099));
  ::Test::JustARecord record2(Common::ARMAGEDON, Acoustic::AUDIO_INPUT_L, Common::Network::PortNumber(8099));
  ASSERT_FALSE(record1 == record2);
  ASSERT_TRUE(record1 != record2);
  ASSERT_TRUE(record1 >= record2);
  ASSERT_FALSE(record1 > record2);
  ASSERT_TRUE(record1 <= record2);
  ASSERT_FALSE(record1 < record2);
}

TEST(TestOfGeneratedRecordType, TestOfComparision5)
{
  ::Test::JustARecord record1(Common::ARMAGEDON, Acoustic::AUDIO_INPUT_L | Acoustic::AUDIO_INPUT_R, Common::Network::PortNumber(8099));
  ::Test::JustARecord record2(Common::ARMAGEDON, Acoustic::AUDIO_INPUT_L, Common::Network::PortNumber(9099));
  ASSERT_FALSE(record1 == record2);
  ASSERT_TRUE(record1 != record2);
  ASSERT_FALSE(record1 >= record2);
  ASSERT_FALSE(record1 > record2);
  ASSERT_TRUE(record1 <= record2);
  ASSERT_TRUE(record1 < record2);
}

TEST(TestOfGeneratedRecordType, TestOfSerialization)
{
  ::Test::JustARecord record(Common::ARMAGEDON, Acoustic::AUDIO_INPUT_L | Acoustic::AUDIO_INPUT_R, Common::Network::PortNumber(8099));
  Serialization::BinarySerializer serializer;
  serializer << record;
  const std::vector<uint8_t>& serialized_data = serializer.getSerializedData();
  ASSERT_EQ(serialized_data.size(), 4);
  ASSERT_EQ(serialized_data[0], 0x0c);
  ASSERT_EQ(serialized_data[1], 0x03);
  ASSERT_EQ(serialized_data[2], 0x1f);
  ASSERT_EQ(serialized_data[3], 0xa3);
}

TEST(TestOfGeneratedRecordType, TestOfDeserialization)
{
  ::Test::JustARecord record;
  std::vector<uint8_t> serialized_data = { 0x0c, 0x03, 0x1f, 0xa3 };
  Serialization::BinaryDeserializer deserializer(serialized_data);
  deserializer >> record;
  ASSERT_EQ(record.toString(), "{ common_severity: ARMAGEDON, acoustic_selected_output_ids: AUDIO_INPUT_L|AUDIO_INPUT_R, common_network_port_number: 8099 }");
}

//--------------------------------------------------------------------------------------------

TEST(TestOfGeneratedIntegerType, TestOfSettingValue)
{
  Common::Network::PortNumber port;
  ASSERT_EQ(port.getPortNumberAsInt(), 0);
  port = Common::Network::PortNumber(8080);
  ASSERT_EQ(port.getPortNumberAsInt(), 8080);
}

TEST(TestOfGeneratedIntegerType, TestOfDumpingToString)
{
  Common::Network::PortNumber port(8080);
  ASSERT_EQ(port.toString(), "8080");
}

TEST(TestOfGeneratedIntegerType, TestOfCreationFromString)
{
  Common::Network::PortNumber severity = Common::Network::PortNumber::fromString("8089");
  ASSERT_EQ(severity.toString(), "8089");
}

TEST(TestOfGeneratedIntegerType, TestOfCreationFromStringError1)
{
  ASSERT_THROW(Common::Network::PortNumber::fromString("NOONE"), Common::ConversionError);
}

TEST(TestOfGeneratedIntegerType, TestOfCreationFromStringError2)
{
  ASSERT_THROW(Common::Network::PortNumber::fromString("990A"), Common::ConversionError);
}

TEST(TestOfGeneratedIntegerType, TestOfSerialization)
{
  Serialization::BinarySerializer serializer;
  Common::Network::PortNumber port(8080);
  serializer << port;
  const std::vector<uint8_t>& serialized_data = serializer.getSerializedData();
  ASSERT_EQ(serialized_data.size(), 2);
  ASSERT_EQ(serialized_data[0], 0x1f);
  ASSERT_EQ(serialized_data[1], 0x90);
}

TEST(TestOfGeneratedIntegerType, TestOfDeserialization)
{
  std::vector<uint8_t> serialized_data = { 0x1f, 0x99 };
  Serialization::BinaryDeserializer deserializer(serialized_data);
  Common::Network::PortNumber port;
  deserializer >> port;
  ASSERT_EQ(port.getPortNumberAsInt(), 8089);
}

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
