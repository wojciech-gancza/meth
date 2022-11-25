// This is example of source code generated file
// DO NOT EDIT IT (except especially prepared and marked blocks)

// ---------------------------------------------------

enum E1 { E1X223,         BETA,
          SOMETHONG_ELSE, X,
          KULA314,        MOVIE,
          DDS,            MDF,
          XRAYMACHINE,    FOXTROT };

const char* const enum1_names[] = {
	      "E1X223",         "BETA",
	      "SOMETHONG_ELSE", "X",
	      "KULA314",        "MOVIE",
	      "DDS",            "MDF",
	      "XRAYMACHINE",    "FOXTROT" };

E1 convert<E1>(const std::string& text)
{
	switch( text.size() )
	{
	case 1:
	    return X;
	case 3:
	    if( text[0] == 'D' )
	        return DDS;
	    else
	        return MDF;
	    };
	case 4:
	    if( text[1] == '5' )
	        return B554;
	    else
	        return BETA;
	    };
	case 5:
	    return MOVIE;
	case 6:
	    return E1X223;
	case 7:
	    if( text[0] == 'F' )
	        return FOXTROT;
	    else
	        return KULA314;
	    };
	case 11:
	    return XRAYMACHINE;
	default:
	    return SOMETHONG_ELSE;
	};
};

std::string to_strig(E1 value)
{
	return enum1_names[static_cast<unsigned>(value)];
}

// ---------------------------------------------------

enum E2 { X0, X1, X2, X3,
          X4, X5, X6, X7,
          X8, X9, XA, XB };

const char* const enum2_names[] = {
	      "X0", "X1", "X2", "X3",
	      "X4", "X5", "X6", "X7",
	      "X8", "X9", "XA", "XB" };

E2 convert<E2>(const std::string& text)
{
	switch( text[1] )
	{
	case '0':
	    return X0;
	case '1':
	    return X1;
	case '2':
	    return X2;
	case '3':
	    return X3;
	case '4':
	    return X4;
	case '5':
	    return X5;
	case '6':
	    return X6;
	case '7':
	    return X7;
	case '8':
	    return X8;
	case '9':
	    return X9;
	case 'A':
	    return XA;
	case 'B':
	    return XB;
	case 'C':
	    return XC;
	case 'D':
	    return XD;
	case 'E':
	    return XE;
	default:
	    return XF;
	};
};

std::string to_strig(E2 value)
{
	return enum2_names[static_cast<unsigned>(value)];
}

// ---------------------------------------------------
