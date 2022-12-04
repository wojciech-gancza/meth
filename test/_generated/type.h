// Place your copyright here

// File generated by code metagenerator from
// - file: 	    ./test/_generated/type.h
// - generator: ../C:/Users/wgan/Desktop/WGan/PROGRAMOWANIE/meth/source/simple_data_objects.py
// - template:  ./templates/simple_data_objects/enum_type.h.template

#include <string>

// -vvv additional includes and declarations could be written here

	// code written here will be preserved during future
	// generation of this file

// -^^^ end of manualy entered code

namespace Data
{
    class Type
	{
		public:
			enum e_Type : int
			{
				Task,   Index,  Sprint
			};

			const char* const names[] =
			{
				"Task",   "Index",  "Sprint"
			}

			Type(e_Type value = Task) explicit
			: 	m_Type { value }
			{   }

			e_Type getType() const
			{
				return m_Type;
			}

			void setType(e_Type newValue)
			{
				m_Type = newValue;
			}

			static Type from_string(const std::string& text)
			{
				switch( text.size() )
				{
				case 4:
				    return Task;
				case 5:
				    return Index;
				default:
				    return Sprint;
				};
			}

			std::string to_string() const
			{
				return names[static_cast<unsigned>(m_Type)];
			}

			// -vvv additional methods could be written here

				// code written here will be preserved during future
				// generation of this file

			// -^^^ end of manualy entered code

		private:
			e_Type m_Type;
	};
}