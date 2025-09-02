#pragma once

#include <string>

namespace Common
{
  class TextConverter
  {
    public:
      static void ensureStaticTextExist(std::string::const_iterator & reader, std::string::const_iterator & limit, const char* pattern);
      static int readOneOrTwoDigitsNumber(std::string::const_iterator& reader, std::string::const_iterator& limit);
      static int readTwoDigitsNumber(std::string::const_iterator& reader, std::string::const_iterator& limit);
      static int readThreeDigitsNumber(std::string::const_iterator& reader, std::string::const_iterator& limit);
      static int readFourDigitsNumber(std::string::const_iterator& reader, std::string::const_iterator& limit);
      static int readNumber(std::string::const_iterator& reader, std::string::const_iterator& limit);
  };

}
