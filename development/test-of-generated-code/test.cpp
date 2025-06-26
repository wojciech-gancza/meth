#include "gtest/gtest.h"

#include "acoustic_selected_output_ids.h"
#include "common_severity.h"
#include "common_conversion_error.h"
#include "common_network_port_number.h"
#include "test_just_a_record.h"
#include "test_another_record.h"
#include "money_netto.h"
#include "common_text_message.h"
#include "common_event_time.h"
#include "common_delay.h"
#include "configuration_node.h"

//--------------------------------------------------------------------------------------------

TEST(TestOfGeneratedCollectionsType, TestOfCreatingDefaultValue)
{
  Configuration::Nodes root;
  ASSERT_EQ(root.toString(), "[  ]");
}

TEST(TestOfGeneratedCollectionsType, TestOfCreatingValue)
{
  Configuration::Nodes root;
  root.insertNode(Configuration::Node(Configuration::Key("A"), Configuration::Value("Hello"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("x"), Configuration::Value("Dolly"), Configuration::Nodes()));
  ASSERT_EQ(root.toString(), "[ { configuration_key: \"A\", configuration_value: \"Hello\", configuration_nodes: [  ] }, { configuration_key: \"x\", configuration_value: \"Dolly\", configuration_nodes: [  ] } ]");
}

TEST(TestOfGeneratedCollectionsType, TestOfComparision1)
{
  Configuration::Nodes root1;
  root1.insertNode(Configuration::Node(Configuration::Key("A"), Configuration::Value("Hello"), Configuration::Nodes()));
  root1.insertNode(Configuration::Node(Configuration::Key("x"), Configuration::Value("Dolly"), Configuration::Nodes()));
  Configuration::Nodes root2;
  root2.insertNode(Configuration::Node(Configuration::Key("A"), Configuration::Value("Hello"), Configuration::Nodes()));
  root2.insertNode(Configuration::Node(Configuration::Key("x"), Configuration::Value("Dolly"), Configuration::Nodes()));

  ASSERT_TRUE(root1 == root2);
  ASSERT_FALSE(root1 != root2);
  ASSERT_TRUE(root1 >= root2);
  ASSERT_FALSE(root1 > root2);
  ASSERT_TRUE(root1 <= root2);
  ASSERT_FALSE(root1 < root2);
}

TEST(TestOfGeneratedCollectionsType, TestOfComparision2)
{
  Configuration::Nodes root1;
  root1.insertNode(Configuration::Node(Configuration::Key("A"), Configuration::Value("Hello"), Configuration::Nodes()));
  root1.insertNode(Configuration::Node(Configuration::Key("x"), Configuration::Value("Dolly"), Configuration::Nodes()));
  Configuration::Nodes root2;
  root2.insertNode(Configuration::Node(Configuration::Key("A"), Configuration::Value("Hello"), Configuration::Nodes()));
  root2.insertNode(Configuration::Node(Configuration::Key("X"), Configuration::Value("Dolly"), Configuration::Nodes()));

  ASSERT_FALSE(root1 == root2);
  ASSERT_TRUE(root1 != root2);
  ASSERT_TRUE(root1 >= root2);
  ASSERT_TRUE(root1 > root2);
  ASSERT_FALSE(root1 <= root2);
  ASSERT_FALSE(root1 < root2);
}

TEST(TestOfGeneratedCollectionsType, TestOfSerialization)
{
  Configuration::Nodes root;
  root.insertNode(Configuration::Node(Configuration::Key("A"), Configuration::Value("Hello"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("x"), Configuration::Value("Dolly"), Configuration::Nodes()));
  Serialization::BinarySerializer serializer;
  serializer << root;
  const std::vector<uint8_t>& serialized_data = serializer.getSerializedData();
  ASSERT_EQ(serialized_data.size(), 24);
  ASSERT_EQ(serialized_data[0], 0x00);
  ASSERT_EQ(serialized_data[1], 0x02);
  ASSERT_EQ(serialized_data[2], 0x01);
  ASSERT_EQ(serialized_data[3], 0x41);
  ASSERT_EQ(serialized_data[4], 0x00);
  ASSERT_EQ(serialized_data[5], 0x05);
  ASSERT_EQ(serialized_data[6], 0x48);
  ASSERT_EQ(serialized_data[7], 0x65);
  ASSERT_EQ(serialized_data[8], 0x6c);
  ASSERT_EQ(serialized_data[9], 0x6c);
  ASSERT_EQ(serialized_data[10], 0x6f);
  ASSERT_EQ(serialized_data[11], 0x00);
  ASSERT_EQ(serialized_data[12], 0x00);
  ASSERT_EQ(serialized_data[13], 0x01);
  ASSERT_EQ(serialized_data[14], 0x78);
  ASSERT_EQ(serialized_data[15], 0x00);
  ASSERT_EQ(serialized_data[16], 0x05);
  ASSERT_EQ(serialized_data[17], 0x44);
  ASSERT_EQ(serialized_data[18], 0x6f);
  ASSERT_EQ(serialized_data[19], 0x6c);
  ASSERT_EQ(serialized_data[20], 0x6c);
  ASSERT_EQ(serialized_data[21], 0x79);
  ASSERT_EQ(serialized_data[22], 0x00);
  ASSERT_EQ(serialized_data[23], 0x00);
}

TEST(TestOfGeneratedCollectionsType, TestOfDeserialization)
{
  Configuration::Nodes root;
  std::vector<uint8_t> serialized_data = { 0x00, 0x02, 0x01, 0x41, 0x00, 0x05, 0x48, 0x65, 0x6c, 0x6c, 0x6f, 0x00, 0x00, 0x01, 0x78, 0x00, 0x05, 0x44, 0x6f, 0x6c, 0x6c, 0x79, 0x00, 0x00 };
  Serialization::BinaryDeserializer deserializer(serialized_data);
  deserializer >> root;
  ASSERT_EQ(root.toString(), "[ { configuration_key: \"A\", configuration_value: \"Hello\", configuration_nodes: [  ] }, { configuration_key: \"x\", configuration_value: \"Dolly\", configuration_nodes: [  ] } ]");
}

TEST(TestOfGeneratedCollectionsType, TestOfIteration)
{
  Configuration::Nodes root;
  root.insertNode(Configuration::Node(Configuration::Key("A"), Configuration::Value("Hello"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("x"), Configuration::Value("Dolly"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("klm"), Configuration::Value("Dirk"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("wx"), Configuration::Value("Epire"), Configuration::Nodes()));

  Configuration::Nodes::Iterator i = root.getNodesBegin();
  ASSERT_EQ(i->toString(), "{ configuration_key: \"A\", configuration_value: \"Hello\", configuration_nodes: [  ] }");
  ++i;
  ++i;
  ASSERT_EQ(i->toString(), "{ configuration_key: \"klm\", configuration_value: \"Dirk\", configuration_nodes: [  ] }");

  Configuration::Nodes::ReverseIterator j = root.getNodesReverseBegin();
  ASSERT_EQ(j->toString(), "{ configuration_key: \"wx\", configuration_value: \"Epire\", configuration_nodes: [  ] }");
  ++j;
  ++j;
  ASSERT_EQ(j->toString(), "{ configuration_key: \"x\", configuration_value: \"Dolly\", configuration_nodes: [  ] }");
  ++j;
  ++j;

  ASSERT_EQ(j, root.getNodesReverseEnd());
}

TEST(TestOfGeneratedCollectionsType, TestOfRemovingElements)
{
  Configuration::Nodes root;
  root.insertNode(Configuration::Node(Configuration::Key("A"), Configuration::Value("Hello"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("x"), Configuration::Value("Dolly"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("klm"), Configuration::Value("Dirk"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("wx"), Configuration::Value("Epire"), Configuration::Nodes()));

  Configuration::Nodes::Iterator i = root.getNodesBegin() + 2;
  root.removeNode(i);
  ASSERT_EQ(root.toString(), "[ { configuration_key: \"A\", configuration_value: \"Hello\", configuration_nodes: [  ] }, "
                               "{ configuration_key: \"x\", configuration_value: \"Dolly\", configuration_nodes: [  ] }, "
                               "{ configuration_key: \"wx\", configuration_value: \"Epire\", configuration_nodes: [  ] } ]");
  root.removeNode( --root.getNodesEnd() );
  ASSERT_EQ(root.toString(), "[ { configuration_key: \"A\", configuration_value: \"Hello\", configuration_nodes: [  ] }, "
                               "{ configuration_key: \"x\", configuration_value: \"Dolly\", configuration_nodes: [  ] } ]");
  root.removeNode(root.getNodesBegin());
  ASSERT_EQ(root.toString(), "[ { configuration_key: \"x\", configuration_value: \"Dolly\", configuration_nodes: [  ] } ]");
}

TEST(TestOfGeneratedCollectionsType, TestOfSearchingElements)
{
  Configuration::Nodes root;
  root.insertNode(Configuration::Node(Configuration::Key("A"), Configuration::Value("Hello1"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("x"), Configuration::Value("Dolly1"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("klm"), Configuration::Value("Dirk1"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("wx"), Configuration::Value("Epire1"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("A"), Configuration::Value("Hello2"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("x"), Configuration::Value("Dolly2"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("x"), Configuration::Value("Dirk2"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("wx"), Configuration::Value("Epire2"), Configuration::Nodes()));

  Configuration::Nodes::SearchResult found_items = root.searchNodes(Configuration::Key("x"));
  std::string string_representation = found_items.toString();

  ASSERT_EQ(string_representation, "[ { configuration_key: \"x\", configuration_value: \"Dolly1\", configuration_nodes: [  ] }, "
                                     "{ configuration_key: \"x\", configuration_value: \"Dolly2\", configuration_nodes: [  ] }, "
                                     "{ configuration_key: \"x\", configuration_value: \"Dirk2\", configuration_nodes: [  ] } ]");
}

TEST(TestOfGeneratedCollectionsType, TestOfIterationOverSearchResult)
{
  Configuration::Nodes root;
  root.insertNode(Configuration::Node(Configuration::Key("A"), Configuration::Value("Hello1"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("x"), Configuration::Value("Dolly1"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("klm"), Configuration::Value("Dirk1"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("wx"), Configuration::Value("Epire1"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("A"), Configuration::Value("Hello2"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("x"), Configuration::Value("Dolly2"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("x"), Configuration::Value("Dirk2"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("wx"), Configuration::Value("Epire2"), Configuration::Nodes()));

  Configuration::Nodes::SearchResult found_items = root.searchNodes(Configuration::Key("x"));
  Configuration::Nodes::SearchResult::Iterator found_item = found_items.getNodesBegin();

  ASSERT_EQ((*found_item).toString(), "{ configuration_key: \"x\", configuration_value: \"Dolly1\", configuration_nodes: [  ] }");
  ++found_item;
  ASSERT_EQ((*found_item).toString(), "{ configuration_key: \"x\", configuration_value: \"Dolly2\", configuration_nodes: [  ] }");
  ++found_item;
  ASSERT_EQ(found_item->toString(), "{ configuration_key: \"x\", configuration_value: \"Dirk2\", configuration_nodes: [  ] }");
  ++found_item;
  ASSERT_EQ(found_item, found_items.getNodesEnd());

  Configuration::Nodes::SearchResult found_items2 = found_items.searchNodes(Configuration::Value("Dolly2"));

  ASSERT_EQ(found_items2.toString(), "[ { configuration_key: \"x\", configuration_value: \"Dolly2\", configuration_nodes: [  ] } ]");
}

TEST(TestOfGeneratedCollectionsType, TestOfIterationOverConstSearchResult)
{
  Configuration::Nodes root;
  root.insertNode(Configuration::Node(Configuration::Key("A"), Configuration::Value("Hello1"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("x"), Configuration::Value("Dolly1"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("klm"), Configuration::Value("Dirk1"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("wx"), Configuration::Value("Epire1"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("A"), Configuration::Value("Hello2"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("x"), Configuration::Value("Dolly2"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("x"), Configuration::Value("Dirk2"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("wx"), Configuration::Value("Epire2"), Configuration::Nodes()));

  const Configuration::Nodes& root_reference = root;
  Configuration::Nodes::ConstSearchResult found_items = root_reference.searchNodes(Configuration::Key("x"));
  Configuration::Nodes::ConstSearchResult::ConstIterator found_item = found_items.getNodesBegin();

  ASSERT_EQ((*found_item).toString(), "{ configuration_key: \"x\", configuration_value: \"Dolly1\", configuration_nodes: [  ] }");
  ++found_item;
  ASSERT_EQ((*found_item).toString(), "{ configuration_key: \"x\", configuration_value: \"Dolly2\", configuration_nodes: [  ] }");
  ++found_item;
  ASSERT_EQ(found_item->toString(), "{ configuration_key: \"x\", configuration_value: \"Dirk2\", configuration_nodes: [  ] }");
  ++found_item;
  ASSERT_EQ(found_item, found_items.getNodesEnd());

  Configuration::Nodes::ConstSearchResult found_items2 = found_items.searchNodes(Configuration::Value("Dolly2"));

  ASSERT_EQ(found_items2.toString(), "[ { configuration_key: \"x\", configuration_value: \"Dolly2\", configuration_nodes: [  ] } ]");
}

TEST(TestOfGeneratedCollectionsType, TestOfRemovingItemFromSearchResult)
{
  Configuration::Nodes root;
  root.insertNode(Configuration::Node(Configuration::Key("A"), Configuration::Value("Hello1"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("x"), Configuration::Value("Dolly1"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("klm"), Configuration::Value("Dirk1"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("wx"), Configuration::Value("Epire1"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("A"), Configuration::Value("Hello2"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("x"), Configuration::Value("Dolly2"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("x"), Configuration::Value("Dirk2"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("wx"), Configuration::Value("Epire2"), Configuration::Nodes()));

  Configuration::Nodes::SearchResult found_items = root.searchNodes(Configuration::Key("x"));
  Configuration::Nodes::SearchResult::Iterator found_item = found_items.getNodesBegin();
  ++found_item;
  found_items.removeNodesIterator(found_item);

  ASSERT_EQ(found_items.toString(), "[ { configuration_key: \"x\", configuration_value: \"Dolly1\", configuration_nodes: [  ] }, "
                                      "{ configuration_key: \"x\", configuration_value: \"Dirk2\", configuration_nodes: [  ] } ]");
}

TEST(TestOfGeneratedCollectionsType, TestOfRemovingItemsByKey)
{
  Configuration::Nodes root;
  root.insertNode(Configuration::Node(Configuration::Key("A"), Configuration::Value("Hello1"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("x"), Configuration::Value("Dolly1"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("klm"), Configuration::Value("Dirk1"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("wx"), Configuration::Value("Epire1"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("A"), Configuration::Value("Hello2"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("x"), Configuration::Value("Dolly2"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("x"), Configuration::Value("Dirk2"), Configuration::Nodes()));
  root.insertNode(Configuration::Node(Configuration::Key("wx"), Configuration::Value("Epire2"), Configuration::Nodes()));

  root.removeNodes(Configuration::Key("x"));

  ASSERT_EQ(root.toString(), "[ { configuration_key: \"A\", configuration_value: \"Hello1\", configuration_nodes: [  ] }, "
                               "{ configuration_key: \"klm\", configuration_value: \"Dirk1\", configuration_nodes: [  ] }, "
                               "{ configuration_key: \"wx\", configuration_value: \"Epire1\", configuration_nodes: [  ] }, "
                               "{ configuration_key: \"A\", configuration_value: \"Hello2\", configuration_nodes: [  ] }, "
                               "{ configuration_key: \"wx\", configuration_value: \"Epire2\", configuration_nodes: [  ] } ]" );
}

//--------------------------------------------------------------------------------------------

TEST(TestOfGeneratedTimeDurationType, TestOfCreatingDefaultValue)
{
  Common::Delay delay;
  ASSERT_EQ(delay.toString(), "00:00.010");
}

TEST(TestOfGeneratedTimeDurationType, TestOfCreatingValue)
{
  Common::Delay delay = Common::Delay::fromString("34:56.789");
  ASSERT_EQ(delay.toString(), "34:56.789");
}

TEST(TestOfGeneratedTimeDurationType, TestOfComparision1)
{
  Common::Delay delay1 = Common::Delay::fromString("34:56.789");
  Common::Delay delay2 = Common::Delay::fromString("34:56.789");

  ASSERT_TRUE(delay1 == delay2);
  ASSERT_FALSE(delay1 != delay2);
  ASSERT_TRUE(delay1 >= delay2);
  ASSERT_FALSE(delay1 > delay2);
  ASSERT_TRUE(delay1 <= delay2);
  ASSERT_FALSE(delay1 < delay2);
}

TEST(TestOfGeneratedTimeDurationType, TestOfComparision2)
{
  Common::Delay delay1 = Common::Delay::fromString("34:56.789");
  Common::Delay delay2 = Common::Delay::fromString("14:56.789");

  ASSERT_FALSE(delay1 == delay2);
  ASSERT_TRUE(delay1 != delay2);
  ASSERT_TRUE(delay1 >= delay2);
  ASSERT_TRUE(delay1 > delay2);
  ASSERT_FALSE(delay1 <= delay2);
  ASSERT_FALSE(delay1 < delay2);
}

TEST(TestOfGeneratedTimeDurationType, TestOfSerialization)
{
  Common::Delay delay = Common::Delay::fromString("34:56.789");
  Serialization::BinarySerializer serializer;
  serializer << delay;
  const std::vector<uint8_t>& serialized_data = serializer.getSerializedData();
  ASSERT_EQ(serialized_data.size(), 8);
  ASSERT_EQ(serialized_data[0], 0x00);
  ASSERT_EQ(serialized_data[1], 0x00);
  ASSERT_EQ(serialized_data[2], 0x00);
  ASSERT_EQ(serialized_data[3], 0x00);
  ASSERT_EQ(serialized_data[4], 0x7c);
  ASSERT_EQ(serialized_data[5], 0xfa);
  ASSERT_EQ(serialized_data[6], 0x76);
  ASSERT_EQ(serialized_data[7], 0x08);
}

TEST(TestOfGeneratedTimeDurationType, TestOfDeserialization)
{
  Common::Delay delay;
  std::vector<uint8_t> serialized_data = { 0x00, 0x00, 0x00, 0x00, 0x7c, 0xfa, 0x76, 0x08 };
  Serialization::BinaryDeserializer deserializer(serialized_data);
  deserializer >> delay;
  ASSERT_EQ(delay.toString(), "34:56.789");
}

TEST(TestOfGeneratedTimeDurationType, TestOfAddingDurationToTime)
{
  Common::Delay delay = Common::Delay::fromString("34:56.789");
  Common::EventTime timestamp = Common::EventTime::fromString("2025-06-10 12:34:56.789");

  Common::EventTime timestamp2 = Common::EventTime(timestamp.getEventTimeAsTimePoint() + delay.getDelayAsTimeDuration());

  ASSERT_EQ(timestamp2.toString(), "2025-06-10 13:09:53.578");
}

//--------------------------------------------------------------------------------------------

TEST(TestOfGeneratedTimePointType, TestOfCreatingValue)
{
  Common::EventTime timestamp = Common::EventTime::fromString("2025-06-10 12:34:56.789");
  ASSERT_EQ(timestamp.toString(), "2025-06-10 12:34:56.789");
}

TEST(TestOfGeneratedTimePointType, TestOfComparision1)
{
  Common::EventTime timestamp1 = Common::EventTime::fromString("2025-06-10 12:34:56.789");
  Common::EventTime timestamp2 = Common::EventTime::fromString("2025-06-10 12:34:56.789");

  ASSERT_TRUE(timestamp1 == timestamp2);
  ASSERT_FALSE(timestamp1 != timestamp2);
  ASSERT_TRUE(timestamp1 >= timestamp2);
  ASSERT_FALSE(timestamp1 > timestamp2);
  ASSERT_TRUE(timestamp1 <= timestamp2);
  ASSERT_FALSE(timestamp1 < timestamp2);
}

TEST(TestOfGeneratedTimePointType, TestOfComparision2)
{
  Common::EventTime timestamp1 = Common::EventTime::fromString("2025-06-10 12:34:56.789");
  Common::EventTime timestamp2 = Common::EventTime::fromString("2025-06-10 12:24:56.789");

  ASSERT_FALSE(timestamp1 == timestamp2);
  ASSERT_TRUE(timestamp1 != timestamp2);
  ASSERT_TRUE(timestamp1 >= timestamp2);
  ASSERT_TRUE(timestamp1 > timestamp2);
  ASSERT_FALSE(timestamp1 <= timestamp2);
  ASSERT_FALSE(timestamp1 < timestamp2);
}

TEST(TestOfGeneratedTimePointType, TestOfSerialization)
{
  Common::EventTime timestamp = Common::EventTime::fromString("2025-06-10 12:34:56.789");
  Serialization::BinarySerializer serializer;
  serializer << timestamp;
  const std::vector<uint8_t>& serialized_data = serializer.getSerializedData();
  ASSERT_EQ(serialized_data.size(), 8);
  ASSERT_EQ(serialized_data[0], 0x00);
  ASSERT_EQ(serialized_data[1], 0x06);
  ASSERT_EQ(serialized_data[2], 0x37);
  ASSERT_EQ(serialized_data[3], 0x35);
  ASSERT_EQ(serialized_data[4], 0x3f);
  ASSERT_EQ(serialized_data[5], 0x67);
  ASSERT_EQ(serialized_data[6], 0x3e);
  ASSERT_EQ(serialized_data[7], 0x08);
}

TEST(TestOfGeneratedTimePointType, TestOfDeserialization)
{
  Common::EventTime timestamp;
  std::vector<uint8_t> serialized_data = { 0x00, 0x06, 0x37, 0x35, 0x3f, 0x67, 0x3e, 0x08 };
  Serialization::BinaryDeserializer deserializer(serialized_data);
  deserializer >> timestamp;
  ASSERT_EQ(timestamp.toString(), "2025-06-10 12:34:56.789");
}

//--------------------------------------------------------------------------------------------

TEST(TestOfGeneratedStringType, TestOfDefaultValue)
{
  Common::TextMessage message;
  ASSERT_EQ(message.toString(), "\"No comments.\"");
}

TEST(TestOfGeneratedStringType, TestOfConstructingValue)
{
  Common::TextMessage message("I'm \\ here");
  ASSERT_EQ(message.toString(), "\"I\\\'m \\\\ here\"");
}

TEST(TestOfGeneratedStringType, TestSettingFieldsValues)
{
  Common::TextMessage message;
  message.setTextMessage("hello");
  ASSERT_EQ(message.toString(), "\"hello\"");
}

TEST(TestOfGeneratedStringType, TestOfComparision1)
{
  Common::TextMessage message1("Abcdef");
  Common::TextMessage message2("Abcdef");

  ASSERT_TRUE(message1 == message2);
  ASSERT_FALSE(message1 != message2);
  ASSERT_TRUE(message1 >= message2);
  ASSERT_FALSE(message1 > message2);
  ASSERT_TRUE(message1 <= message2);
  ASSERT_FALSE(message1 < message2);
}

TEST(TestOfGeneratedStringType, TestOfComparision2)
{
  Common::TextMessage message1("Abcdxf");
  Common::TextMessage message2("Abcdef");

  ASSERT_FALSE(message1 == message2);
  ASSERT_TRUE(message1 != message2);
  ASSERT_TRUE(message1 >= message2);
  ASSERT_TRUE(message1 > message2);
  ASSERT_FALSE(message1 <= message2);
  ASSERT_FALSE(message1 < message2);
}

TEST(TestOfGeneratedStringType, TestOfSerialization)
{
  Common::TextMessage message("Abcdxf");
  Serialization::BinarySerializer serializer;
  serializer << message;
  const std::vector<uint8_t>& serialized_data = serializer.getSerializedData();
  ASSERT_EQ(serialized_data.size(), 8);
  ASSERT_EQ(serialized_data[0], 0x00);
  ASSERT_EQ(serialized_data[1], 0x06);
  ASSERT_EQ(serialized_data[2], 0x41);
  ASSERT_EQ(serialized_data[3], 0x62);
  ASSERT_EQ(serialized_data[4], 0x63);
  ASSERT_EQ(serialized_data[5], 0x64);
  ASSERT_EQ(serialized_data[6], 0x78);
  ASSERT_EQ(serialized_data[7], 0x66);
}

TEST(TestOfGeneratedStringType, TestOfDeserialization)
{
  Common::TextMessage message;
  std::vector<uint8_t> serialized_data = { 0x00, 0x06, 0x41, 0x62, 0x63, 0x64, 0x78, 0x66 };
  Serialization::BinaryDeserializer deserializer(serialized_data);
  deserializer >> message;
  ASSERT_EQ(message.toString(), "\"Abcdxf\"");
}

//--------------------------------------------------------------------------------------------

TEST(TestOfGeneratedFloatType, TestOfDefaultValue)
{
  Money::Netto salary;
  ASSERT_EQ(salary.toString(), "0.00");
}

TEST(TestOfGeneratedFloatType, TestOfConstructingValue)
{
  Money::Netto salary(7.977f);
  ASSERT_EQ(salary.toString(), "7.98");
}

TEST(TestOfGeneratedFloatType, TestSettingFieldsValues)
{
  Money::Netto salary;
  salary.setNetto(9.999f);
  ASSERT_EQ(salary.toString(), "10.00");
}

TEST(TestOfGeneratedFloatType, TestOfComparision1)
{
  Money::Netto salary1(9.8874f);
  Money::Netto salary2(9.8872f);

  ASSERT_TRUE(salary1 == salary2);
  ASSERT_FALSE(salary1 != salary2);
  ASSERT_TRUE(salary1 >= salary2);
  ASSERT_FALSE(salary1 > salary2);
  ASSERT_TRUE(salary1 <= salary2);
  ASSERT_FALSE(salary1 < salary2);
}

TEST(TestOfGeneratedFloatType, TestOfComparision2)
{
  Money::Netto salary1(9.8874f);
  Money::Netto salary2(9.2872f);

  ASSERT_FALSE(salary1 == salary2);
  ASSERT_TRUE(salary1 != salary2);
  ASSERT_TRUE(salary1 >= salary2);
  ASSERT_TRUE(salary1 > salary2);
  ASSERT_FALSE(salary1 <= salary2);
  ASSERT_FALSE(salary1 < salary2);
}

TEST(TestOfGeneratedFloatType, TestOfSerialization)
{
  Money::Netto salary(9.8874f);
  Serialization::BinarySerializer serializer;
  serializer << salary;
  const std::vector<uint8_t>& serialized_data = serializer.getSerializedData();
  ASSERT_EQ(serialized_data.size(), 4);
  ASSERT_EQ(serialized_data[0], 0x41);
  ASSERT_EQ(serialized_data[1], 0x1e);
  ASSERT_EQ(serialized_data[2], 0x32);
  ASSERT_EQ(serialized_data[3], 0xca);
}

TEST(TestOfGeneratedFloatType, TestOfDeserialization)
{
  Money::Netto salary;
  std::vector<uint8_t> serialized_data = { 0x41, 0x1e, 0x32, 0xca };
  Serialization::BinaryDeserializer deserializer(serialized_data);
  deserializer >> salary;
  ASSERT_EQ(salary.toString(), "9.89");
}

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
