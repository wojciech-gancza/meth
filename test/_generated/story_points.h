// Place your copyright here

// File generated by code metagenerator from
// - file: 	    ./test/_generated/story_points.h
// - generator: ../C:/Users/wgan/Desktop/WGan/PROGRAMOWANIE/meth/source/MAIN.py
// - template:  ./templates/simple_data_objects/simple_type.h.template

// -vvv additional includes and declarations could be written here

	// code written here will be preserved during future
	// generation of this file

// -^^^ end of manualy entered code

namespace Data
{
    class StoryPoints
	{
		public:
			StoryPoints(uint16_t value = 0) explicit
			: 	m_StoryPoints { value }
			{   }

			uint16_t getStoryPoints() const
			{
				return m_StoryPoints;
			}

			void setStoryPoints(uint16_t newValue)
			{
				m_StoryPoints = newValue;
			}

			// -vvv additional methods could be written here

				// code written here will be preserved during future
				// generation of this file

			// -^^^ end of manualy entered code

		private:
			uint16_t m_StoryPoints;
	};
}