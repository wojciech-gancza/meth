#pragma once

#include <string>

namespace Common
{
  class ConversionError
  {
    public:
      ConversionError(const std::string& text, const std::string& problem)
        : converting_text(text)
        , found_problem(problem)
      {  }

      const std::string converting_text;
      const std::string found_problem;
  };
};
