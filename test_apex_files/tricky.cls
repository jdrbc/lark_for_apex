public class TestClass extends TestAbstractClass implements TestInterface1, TestInterface2 {
    
    static Integer prop = 0;
    static {
        Integer prop = 0;
    }
    
    private final Integer finalTest = 10;
    
    private Integer getTest { get { return 1; } set; }
    private Integer getTest2 { get { return 1; } set { getTest2 = value; } }
    private Integer getTest3 { get; set { getTest3 = value; }}
    
    // Assignments 
    {
        Integer x = 0;
        String s;
        Account a;
        Account[] accs;
        
    }
    
    {{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}
    
    static void sobjects() {
        {{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}
        Account a = new Account();
		Contact c = new Contact();
		System.debug(a.name);
		a.name = 'xxx';
		System.debug(c.account.name);
        Integer acctNameLength = new Account[]{new Account(Name='Acme')}[0].Name.length();
    }

    // comment
    public 
    // another weird comment
    class 
    // another weird comment
    WeirdClass 
    // weird comment
    {

    }

    private 
    // I 
    Integer 
    // can't believe
    weirdMethod
    // this is fine
    ()
    // wut
    {
        return 0; 
    }
    
    static void arrays() {
        Account[] accs1;
        Account[] accs2 = new Account[]{};
        Account[] accs3 = new Account[]{new Account()};
        Account[] accs4 = new Account[4];
        Integer[] ints1;
        Integer[] ints2 = new Integer[]{1, 2, 3};
        Integer[] ints3 = new Integer[6];
    }
    
    static void maps() {
        Account acc = [select Id from account where name = 'xxx'];
        Account[] accs = new Account[]{acc};
            Map<Account, Contact> myMap = new Map<Account,Contact> {
                new Account() => new Contact()
            };
        //System.assert(accs[acc.id] != null);
    }
    
    void instanceMethodWithSubBlocks() {
        Integer i = 0;
        {
            Integer j = 0;
            {
                // Not allowed
                // Integer i = 0;
                Integer k = 0; 
            }
        }
    }
    
    void instanceMethodWithForLoopsNoBlock() {
        for (Integer j = 0; j < 10; j++);
		for (Integer j = 0; j < 10; j++);
        for (;;);
    }
    
    void emptyWhile() {
        while(true);
    }
    
    void fullWhile() {
        while(true) { Boolean x = true; }
    }
    
    void doWhile() {
        do {
            
        } while(true);
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
    
    Exception getException() {
        return null;
    }
    
    void trycatch() {
        try {
            
        } finally {
            
        }
        
        try {
            
        } catch(Exception e) {
            
        }
    }
    
    void soqltest() {
		Id accId;
        Account a = [SELECT id FROM ACCOUNT where id = :accId or Name = 'x'];
        Integer accountCount = [SELECT Count() FROM Account];
    }
}