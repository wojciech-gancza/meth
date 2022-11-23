// This is example of source code generated file
// DO NOT EDIT IT (except especially prepared and marked blocks)

enum E1 { ${enum1.get_items_as_list()} };

const char* const enum1_names[] = {
	      ${enum1.get_items_as_list('"')} };
		  
E1 convert<E1>(const std::string& text)
{
	${enum1.code_of_convert_from_string()}
};

std::string to_strig(E1 value)
{
	return enum1_names[static_cast<unsigned>(value)];
}

// ---------------------------------------------------

enum E2 { ${enum2.get_items_as_list()} };

const char* const enum2_names[] = {
	      ${enum2.get_items_as_list('"')} };
		  
E2 convert<E2>(const std::string& text)
{
	${enum2.code_of_convert_from_string()}
};

std::string to_strig(E2 value)
{
	return enum2_names[static_cast<unsigned>(value)];
}

