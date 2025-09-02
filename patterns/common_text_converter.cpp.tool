#include "common_text_converter.h"
#include "common_conversion_error.h"

namespace Common
{
  void TextConverter::ensureStaticTextExist(std::string::const_iterator& reader, std::string::const_iterator& limit, const char* pattern)
  {
    while (*pattern)
    {
      if (reader == limit || *reader != *pattern)
      {
        throw Common::ConversionError(pattern, "Expect constand pattern.");
      }
      ++reader;
      ++pattern;
    }
  }

  int TextConverter::readOneOrTwoDigitsNumber(std::string::const_iterator& reader, std::string::const_iterator& limit)
  {
    if (reader == limit)
    {
      throw Common::ConversionError("", "Expect one or two digits.");
    }
    char digit = *reader++;
    if (!isdigit(digit))
    {
      throw Common::ConversionError("", "Expect one or two digits.");
    }
    int value = digit - '0';
    if (reader != limit)
    {
      digit = *reader;
      if (isdigit(digit))
      {
        value = 10 * value + digit - '0';
        ++reader;
      }
      else
      {
        throw Common::ConversionError("", "Expect one or two digits.");
      }
    }
    return value;
  }

  int TextConverter::readTwoDigitsNumber(std::string::const_iterator& reader, std::string::const_iterator& limit)
  {
    if (reader == limit)
    {
      throw Common::ConversionError("", "Expect two digits.");
    }
    char digit = *reader++;
    if (!isdigit(digit) || reader == limit)
    {
      throw Common::ConversionError("", "Expect two digits.");
    }
    int value = digit - '0';
    digit = *reader++;
    if (!isdigit(digit))
    {
      throw Common::ConversionError("", "Expect two digits.");
    }
    value = 10 * value + digit - '0';

    return value;
  }

  int TextConverter::readThreeDigitsNumber(std::string::const_iterator& reader, std::string::const_iterator& limit)
  {
    if (reader == limit)
    {
      throw Common::ConversionError("", "Expect three digits.");
    }
    char digit = *reader++;
    if (!isdigit(digit) || reader == limit)
    {
      throw Common::ConversionError("", "Expect three digits.");
    }
    int value = digit - '0';
    digit = *reader++;
    if (!isdigit(digit) || reader == limit)
    {
      throw Common::ConversionError("", "Expect three digits.");
    }
    value = 10 * value + digit - '0';
    digit = *reader++;
    if (!isdigit(digit))
    {
      throw Common::ConversionError("", "Expect three digits.");
    }
    value = 10 * value + digit - '0';

    return value;
  }

  int TextConverter::readFourDigitsNumber(std::string::const_iterator& reader, std::string::const_iterator& limit)
  {
    if (reader == limit)
    {
      throw Common::ConversionError("", "Expect four digits.");
    }
    char digit = *reader++;
    if (!isdigit(digit) || reader == limit)
    {
      throw Common::ConversionError("", "Expect four digits.");
    }
    int value = digit - '0';
    digit = *reader++;
    if (!isdigit(digit) || reader == limit)
    {
      throw Common::ConversionError("", "Expect four digits.");
    }
    value = 10 * value + digit - '0';
    digit = *reader++;
    if (!isdigit(digit) || reader == limit)
    {
      throw Common::ConversionError("", "Expect four digits.");
    }
    value = 10 * value + digit - '0';
    digit = *reader++;
    if (!isdigit(digit))
    {
      throw Common::ConversionError("", "Expect four digits.");
    }
    value = 10 * value + digit - '0';

    return value;
  }

  int TextConverter::readNumber(std::string::const_iterator& reader, std::string::const_iterator& limit)
  {
    if (reader == limit || !isdigit(*reader))
    {
      Common::ConversionError("", "Expect number.");
    }

    int result = (*reader++) - '0';

    while (reader != limit)
    {
      if (isdigit(*reader))
      {
        result = 10 * result + (*reader++) - '0';
      }
      else
      {
        break;
      }
    }

    return result;
  }
}