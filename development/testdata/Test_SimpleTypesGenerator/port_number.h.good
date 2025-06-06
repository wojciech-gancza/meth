  
  class PortNumber
  {
  public:
    explicit PortNumber(uint16_t port_number) noexcept;
    PortNumber() noexcept;
    PortNumber(const PortNumber& port_number) noexcept;

    uint16_t getPortNumberAsInteger() const noexcept;
    void setPortNumber(uint16_t port_number) noexcept;

    PortNumber& operator=(const PortNumber& port_number) noexcept;

    bool operator==(const PortNumber& other) const noexcept;
    bool operator!=(const PortNumber& other) const noexcept;
    bool operator<(const PortNumber& other) const noexcept;
    bool operator>(const PortNumber& other) const noexcept;
    bool operator<=(const PortNumber& other) const noexcept;
    bool operator>=(const PortNumber& other) const noexcept;

    friend std::ostream& operator<<(std::ostream& out, 
                                    const PortNumber& port_number);

    friend SerializationInterface& operator<<(SerializationInterface& serializer, 
                                              const PortNumber& port_number);
    friend DeserializationInterface& operator>>(DeserializationInterface& deserializer, 
                                              PortNumber& port_number);

    std::string toString() const;
    static PortNumber fromString(const std::string& text);

  private:
    uint16_t m_port_number;
  };


