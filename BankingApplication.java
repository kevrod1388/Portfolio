import java.util.Scanner;

public class BankingApplication {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		BankAccount obj = new BankAccount("User1", "1" );
		obj.showMenu();
	}
	
}

class BankAccount{
	int balance;
	int previousTransaction;
	String customerName;
	String customerId;
	
	public BankAccount(String cname, String cid) {
		customerName = cname;
		customerId = cid;
		
	}
	
	void deposit(int amount) {
		if(amount != 0) {
			balance = balance + amount;
			previousTransaction = amount;
		}
	}
	
   void withdraw(int amount) {
	   if(amount != 0) {
			balance = balance - amount;
			previousTransaction = -amount;
		}
   }
   
   void getPreviousTransaction() {
	   if(previousTransaction > 0) {
		   System.out.println("Deposited: " + previousTransaction);
	   }
	   else if(previousTransaction < 0) {
		   System.out.println("Withdraw: " +Math.abs(previousTransaction));
	   }
	   else {
		   System.out.println("No Transaction Occured");
	   }
   }
   
   void showMenu() {
	   
	   char option = '\0';
		Scanner scanner = new Scanner(System.in);
	   
	   System.out.println("Welcome " +customerName);
	   System.out.println("Your ID " +customerId);
	   System.out.println("\n");
	   
	   System.out.println("A: Check your Balance");
	   System.out.println("B: Deposit");
	   System.out.println("C: Withdraw");
	   System.out.println("D: Previous Transaction");
	   System.out.println("E: Exit The System");
	   
	   do {
		   System.out.println("=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=");
		   System.out.println("Enter Your Options");
		   System.out.println("=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=");
		   option = scanner.next().charAt(0);
		   System.out.println("=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=");
	       
		   System.out.println("\n");
	       
	       switch(option) {
	       case 'A':
	    	   System.out.println("------------------------------------------------");
	    	   System.out.println("Balance = " +balance);
	    	   System.out.println("-------------------------------------------------");
	    	   System.out.println("\n");
	    	   break;
	    	   
	       case 'B':
	    	   System.out.println("------------------------------------------------");
	    	   System.out.println("Enter Amount to deposit");
	    	   System.out.println("-------------------------------------------------");
	    	   System.out.println("\n");
	    	   
	    	   int amount = scanner.nextInt();
	    	   deposit(amount);
	    	   System.out.println("\n");
	    	   
	    	   break;
	    	   
	    	   case 'C':
		    	   System.out.println("------------------------------------------------");
		    	   System.out.println("Enter Amount to Withdraw");
		    	   System.out.println("-------------------------------------------------");
		    	   System.out.println("\n");
		    	   
		    	   int amount2 = scanner.nextInt();
		    	   withdraw(amount2);
		    	   System.out.println("\n");
		    	   
		    	   break;
		    	   
		        case 'D':
			    	System.out.println("------------------------------------------------");
	    	        getPreviousTransaction();
			    	System.out.println("------------------------------------------------");
	    	        System.out.println("\n");
		       
	    	        break;
	    	        
		        case 'E':
		          System.out.println("=================================================================================================");
	    	          break;
	    	        
		        default:
		        	System.out.println("Invalid Option! Please Enter Correct Option...");
	    		     break;
	       }
	   }
	   while(option != 'E');
	   System.out.println("Thank You for Using our Services...");
   }

}
