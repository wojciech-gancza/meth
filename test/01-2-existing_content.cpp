class X
{
	code to overwritte with template
	
	// -vvv implementation of user defined function

	void f()
	{
		cout << "AAA";
	}

	// -^^^ and of user defined code block

	void a_function
	{
	    // -vvv a_function user code
	    f();
		cout << "BBB";
	    // -^^^ end of user code. do not modify
	}
};
