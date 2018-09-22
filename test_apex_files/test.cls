// comment
/*
other comment 
*/
public class TestClass extends TestAbstractClass implements TestInterface1, TestInterface2  {
	void testSoql() {
		Account a = [SELECT ID FROM ACCOUNT];
	}
	
	{
		Integer i = 0, j, k = 1;
	}

	Integer i;
	Integer j { get; }
	Integer k { get; set; }
	Integer l { get { return x; } set { Integer i; } }

	TestClass() {
		
	}
	
	public enum Color {
		TEST,
		ONE
	}

   	private class InnerClass { } 
   	// inner block
   	{ {} }

   	public class TestClass {

		public static void myMethod() {
		
		}

		public static void myOtherMethod(Parameter one) {

		}

		public abstract void myAbstractMethod(Parameter one, Parameter two);

		public virtual void myVirtualMethod() {
		
		}

		public override String toString() {
			return 'xyz';
		}
	}

	Integer i = 0;

	public static void myMethod() {
		Integer j = 1;

		while (true) {
			i++;
		}

		do {
			x++;
		} while (true);

		for(;;);

		for (Integer i = 0; i++; i++) {
			Integer j = 10;
		}

		for (Integer k = 1; k++; k++) 
			k++;

	}


	public static void expressionMethod() {
		i = true ? i : j;
		Boolean k = i && j;
		Boolean k = i || (j || k && j);
		if (i == j) { return; }
		if (i === j) { return; }
		if (i < j) { return; }
		if (i > j) { return; }
		if (i >= j) { return; }
		if (i <= j) { return; }
		if (i != j) { return; }
		if (i !== j) { return; }
		Integer x = 1 + 1;
		Integer y = 2 - 2;
		Integer z = 6 / 6;
		Integer a = 8*8;
		Integer i = ++j;
		i = -j;
		i = --j;
		i = j --;
		Boolean x = !j;
		i & k;
		i | k;
		i ^ k;
		i ^= k;
		i << k;
		i >> k;
		i >>> k;

	}

    void ifTest() {
    	if (x) y;
    	if (true) {
    		return;
    	}
    }

    void doThrow() {
    	try {
    		throw e;
    	} catch (Exception e) {
    		return;
    	} finally {
    		return;
    	}
    }

    void loop() {
	    for (;;) {
    		break;
    	}

    	for (;;) {
    		continue;
    	}
    }

	void doSwitch() {
        Integer i;
        switch on i {
           when 2 {
               System.debug('when block 2');
           }
           when -3 {
               System.debug('when block -3');
           }
           when else {
               System.debug('default');
           }
        }
    }
    
}
// comment
/*
other comment 
*/