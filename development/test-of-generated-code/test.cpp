#include "gtest/gtest.h"

#include "acoustic_outputs_flags.h"

//--------------------------------------------------------------------------------------------

TEST(TestOfGeneratedBitflagsType, TestOfBuildingBitflag)
{
  Acoustic::OutputsFlags flags;
  flags |= RADIO_TRAMSMIT;
  flags |= DRIVER_HANDPHONE;
  flags |= AUDIO_INPUT_L;
  ASSERT_EQ(flags, AUDIO_INPUT_L | RADIO_TRAMSMIT | DRIVER_HANDPHONE);
  ASSERT_NE(flags, AUDIO_INPUT_L | DRIVER_HANDPHONE);
}

TEST(TestOfGeneratedBitflagsType, TestOfDumpingToString1)
{
  Acoustic::OutputsFlags flags;
  flags |= RADIO_TRAMSMIT;
  flags |= DRIVER_HANDPHONE;
  flags |= VEHICLE_OUTHER_SPEAKER;
  ASSERT_EQ(flags.toString(), "RADIO_TRAMSMIT|DRIVER_HANDPHONE|VEHICLE_OUTHER_SPEAKER");
}

TEST(TestOfGeneratedBitflagsType, TestOfDumpingToString2)
{
  Acoustic::OutputsFlags flags2;
  ASSERT_EQ(flags2.toString(), "NONE");
}

TEST(TestOfGeneratedBitflagsType, TestOfCreationFromString1)
{
  Acoustic::OutputsFlags flags1 = Acoustic::OutputsFlags::fromString("RADIO_TRAMSMIT|DRIVER_HANDPHONE|VEHICLE_OUTHER_SPEAKER");
  ASSERT_EQ(flags1.toString(), "RADIO_TRAMSMIT|DRIVER_HANDPHONE|VEHICLE_OUTHER_SPEAKER");
}

TEST(TestOfGeneratedBitflagsType, TestOfCreationFromString2)
{
  Acoustic::OutputsFlags flags1 = Acoustic::OutputsFlags::fromString("NONE");
  ASSERT_EQ(flags1.toString(), "NONE");
}

TEST(TestOfGeneratedBitflagsType, TestOfCreationFromString3)
{
  Acoustic::OutputsFlags flags1 = Acoustic::OutputsFlags::fromString("DRIVER_HANDPHONE");
  ASSERT_EQ(flags1.toString(), "DRIVER_HANDPHONE");
}

TEST(TestOfGeneratedBitflagsType, TestOfMasking)
{
  Acoustic::OutputsFlags flags = RADIO_TRAMSMIT | DRIVER_HANDPHONE | CABIN_INNER_SPEAKER;
  flags &= !DRIVER_HANDPHONE;
  ASSERT_EQ(flags, RADIO_TRAMSMIT | CABIN_INNER_SPEAKER);
}

TEST(TestOfGeneratedBitflagsType, TestOfErasingFlag)
{
  Acoustic::OutputsFlags flags = RADIO_TRAMSMIT | DRIVER_HANDPHONE | CABIN_INNER_SPEAKER;
  flags.remove(DRIVER_HANDPHONE | CABIN_INNER_SPEAKER);
  ASSERT_EQ(flags, RADIO_TRAMSMIT);
}

TEST(TestOfGeneratedBitflagsType, TestOfCheckingFlags)
{
  Acoustic::OutputsFlags flags = RADIO_TRAMSMIT | DRIVER_HANDPHONE | CABIN_INNER_SPEAKER;
  ASSERT_TRUE(flags.isAnyOf(DRIVER_HANDPHONE | AUDIO_INPUT_R));
  ASSERT_FALSE(flags.hasAllOf(DRIVER_HANDPHONE | AUDIO_INPUT_R));
  ASSERT_TRUE(flags.hasAllOf(DRIVER_HANDPHONE | CABIN_INNER_SPEAKER));
  ASSERT_FALSE(flags.isAnyOf(AUDIO_INPUT_R | VEHICLE_OUTHER_SPEAKER));
}

TEST(TestOfGeneratedBitflagsType, TestOfSerialization)
{
  Acoustic::OutputsFlags flags = RADIO_TRAMSMIT | DRIVER_HANDPHONE | CABIN_INNER_SPEAKER;
  Serialization::BinarySerializer serializer;
  serializer << flags;
  const std::vector<uint8_t>& serialized_data = serializer.getSerialziedData();
  ASSERT_EQ(serialized_data.size(), 1);
  ASSERT_EQ(serialized_data[0], 0x34);
}

TEST(TestOfGeneratedBitflagsType, TestOfDeserialization)
{
  std::vector<uint8_t> serialized_data = { 0x34 };
  Serialization::BinaryDeserializer deserializer(serialized_data);
  Acoustic::OutputsFlags flags;
  deserializer >> flags;
  ASSERT_EQ(flags, RADIO_TRAMSMIT | DRIVER_HANDPHONE | CABIN_INNER_SPEAKER);
}

//--------------------------------------------------------------------------------------------
