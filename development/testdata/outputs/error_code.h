  
  class ErrorCode
  {
  public:
    explicit ErrorCode(uint16_t error_code) noexcept;
    ErrorCode() noexcept;
    ErrorCode(const ErrorCode& error_code) noexcept;

    uint16_t getErrorCodeAsInteger() const noexcept;
    void setErrorCode(uint16_t error_code) noexcept;

    ErrorCode& operator=(const ErrorCode& error_code) noexcept;

    bool operator==(const ErrorCode& other) const noexcept;
    bool operator!=(const ErrorCode& other) const noexcept;
    bool operator<(const ErrorCode& other) const noexcept;
    bool operator>(const ErrorCode& other) const noexcept;
    bool operator<=(const ErrorCode& other) const noexcept;
    bool operator>=(const ErrorCode& other) const noexcept;

    friend std::ostream& operator<<(std::ostream& out, 
                                    const ErrorCode& error_code);

    friend SerializationInterface& operator<<(SerializationInterface& serializer, 
                                              const ErrorCode& error_code);
    friend DeserializationInterface& operator>>(DeserializationInterface& deserializer, 
                                              ErrorCode& error_code);

    std::string toString() const;
    static ErrorCode fromString(const std::string& text);

  private:
    uint16_t m_error_code;
  };


