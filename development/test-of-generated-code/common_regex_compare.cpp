#include "common_regex_compare.h"

#include <regex>

namespace Common
{
  bool RegexCompare::isEqual(const std::string& first, const std::string& second)
  {
    if (first == second)
    {
      return true;
    }
    std::regex second_re(second);
    std::cmatch match_result;
    if (std::regex_match(first.c_str(), match_result, second_re))
    {
      return true;
    }
    std::regex first_re(first);
    return std::regex_match(second.c_str(), match_result, first_re);
  }
}