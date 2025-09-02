#pragma once

#include <string>

namespace Common
{
  class SizeError
  {
  public:
    SizeError(uint64_t p_requested_size, const std::string& problem)
      : requested_size(p_requested_size)
      , found_problem(problem)
    {  }

    uint64_t requested_size;
    const std::string found_problem;
  };
};
