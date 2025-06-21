#pragma once

namespace Common
{
  class StrcmpCompare
  {
    public:
      static bool isEqual(const std::string& first, const std::string& second)
      {
        return first == second;
      }

      static bool isNotEqual(const std::string& first, const std::string& second)
      {
        return first != second;
      }

      static bool isLower(const std::string& first, const std::string& second)
      {
        return first < second;
      }

      static bool isLowerOrEqual(const std::string& first, const std::string& second)
      {
        return first <= second;
      }

      static bool isAboveOrEqual(const std::string& first, const std::string& second)
      {
        return first >= second;
      }

      static bool isAbove(const std::string& first, const std::string& second)
      {
        return first > second;
      }
  };
}