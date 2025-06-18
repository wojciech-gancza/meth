#pragma once

namespace Common
{
  template <class T> bool is_record_field_equal(const T& a, const T& b)
  {
    if constexpr (T::is_compareable)
    {
      return (a == b);
    }
    else
    {
      return true;
    }
  }

  template <class T> bool is_record_field_not_equal(const T& a, const T& b)
  {
    if constexpr (T::is_compareable)
    {
      return (a != b);
    }
    else
    {
      return false;
    }
  }

  template <class T> bool is_ordered_record_field_not_equal(const T& a, const T& b)
  {
    if constexpr (T::is_ordered)
    {
      return (a != b);
    }
    else
    {
      return false;
    }
  }

  template <class T> bool is_record_field_less(const T& a, const T& b)
  {
    if constexpr (T::is_ordered)
    {
      return (a < b);
    }
    else
    {
      return false;
    }
  }

  template <class T> bool is_record_field_greater(const T& a, const T& b)
  {
    if constexpr (T::is_ordered)
    {
      return (a > b);
    }
    else
    {
      return false;
    }
  }
}
