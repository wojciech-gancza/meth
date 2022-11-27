// This is example of source code generated file
// DO NOT EDIT IT (except especially prepared and marked blocks)

// ---------------------------------------------------

${#FOR nil : [ ]}
void function_${nil}
{
	// -vvv body of hunction handler No ${nil}
	// example of function body - feel free to change it
	// -^^^
}
${#END}

${#FOR item : ["XXX", 2, 3, 4, 6, 12, 55]}
void function_${item}
{
	// -vvv body of hunction handler No ${item}
	// example of function body - feel free to change it
	// -^^^
}
${#END}

${#FOR key, value : someMap}
	${key} :-> ${value}
${#END}

${#IF emitE1}

enum E1 { ${enum1.get_items_as_list()} };

const char* const enum1_names[] = {
	      ${enum1.get_items_as_list('"')} };
		  
E1 convert<E1>(const std::string& text)
{
	${enum1.code_of_convert_from_string()}
};

${#IF convert_to_string}
std::string to_strig(E1 value)
{
	return enum1_names[static_cast<unsigned>(value)];
}
${#ELSE}
This should never happen!
${#  END  }
${#ELSE}
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
${#END}

// ---------------------------------------------------

