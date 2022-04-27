

public class Main {
	
	public static void main ( String args []){
		
		Inventory inventory = new Inventory();
		
		Book book1 = new Book("The Doll People", "Laura Godwin", "Fiction", "Dolls come to life at night",true, 288, 1994, 12.97f, 14.4f);
		
		Book book2 = new Book("Of Mice and Men", "John Steinbeck", "Fiction", "Mentally disabled man murders woman", false, 112, 1993, 9.00f, 2.1f );
		
		Book book3 = new Book("Lord of the Flies", "William Golding", "Fiction", "A large group of young boys are stranded on a deserted island", false, 224, 1954, 5.48f, 2.1f);
		
		Book book4 = new Book("Harry Potter and the Sorcerer's Stone", "J.K Rowling", "Fiction", "A boy discovers he's destined to be a wizard", true, 309, 1998, 24.91f, 8.5f);
		
		Book book5 = new Book("American Desperado", "Evan Wright", "Non-Fiction", "The tales of a once prominent narcotics smuggler in the 1980s", true, 250, 2012, 15.23f, 7.2f);
		
		Book book6 = new Book("The Prince", "Nicolo Machiavelli", "Non-Fiction", "16th century philosophy manual", true, 82, 1513, 24.04f, 6.2f);
		
		Book book7 = new Book ("The Republic", "Plato", "Non-Fiction", "Philisophical piece about how nations should be structured", false, 206, 381, 8.97f, 15.2f);
		
		Book book8 = new Book("The Hunger Games", "Suzanne Collins", "Non-Fiction", "Children are selected as tributes to fight eachother until only one survices", true, 386, 2010, 12.42f, 11.2f);
		
		Book book9 = new Book("Creature", "John Saul", "Fiction", "The High School football team is used as lab experiments for an evil experimental laboratory.", true, 416, 1990, 12.95f, 8.00f);
		
		Book book10 = new Book("The Boxcar Children, No. 1", "Gertrude Chandler Warner", "Fiction", "Orphans discover home in an abandoned train car", false, 154, 1989, 4.99f, 10.4f);
		
		inventory.add(book1);
		inventory.add(book2);
		inventory.add(book3);
		inventory.add(book4);
		inventory.add(book5);
		inventory.add(book6);
		inventory.add(book7);
		inventory.add(book8);
		inventory.add(book9);
		inventory.add(book10);
		
		
		
		
		
		CompactDisk compactDisk1 = new CompactDisk("Disintegration", "The Cure", "The Cure", "Gothic Rock Album", 1989, 9.99f, 2.5f );
		
		CompactDisk compactDisk2 = new CompactDisk("Discovering the Waterfront", "Silverstein", "Silverstein", "Post-Hardcover", 2005, 10.00f, 2.5f);
		
		CompactDisk compactDisk3 = new CompactDisk("I like it when you sleep", "The 1975", "The 1975", "Alternative Rock", 2016, 14.99f, 2.5f);
		
		CompactDisk compactDisk4 = new CompactDisk("Wish", "The Cure", "The Cure", "Alternative Rock/Pop", 1992, 5.63f, 2.5f);
		
		CompactDisk compactDisk5 = new CompactDisk("Still Searching", "Senses Fail", "Senses Fail", "Alternative Rock", 2006, 12.99f, 2.5f);
		
		CompactDisk compactDisk6 = new CompactDisk("Boston", "Boston", "Boston", "Rock", 1976, 6.20f, 2.5f);
		
		CompactDisk compactDisk7 = new CompactDisk("Tell all your friends", "Taking Back Sunday", "Taking Back Sunday", "Alternative Rock", 2002, 5.99f, 2.5f);
		
		CompactDisk compactDisk8 = new CompactDisk("They're only chasing safety", "Underoath", "Underoath", "Post-Hardcore", 2004, 6.42f, 2.5f);
		
		CompactDisk compactDisk9 = new CompactDisk("Reckless & Relentless", "Asking Alexandria", "Asking Alexandria", "Metal", 2010, 7.00f, 2.5f);
		
		CompactDisk compactDisk10 = new CompactDisk("If only you were lonely", "Hawthorne Heights", "Hawthorne Heights", "Alternative Rock", 2006, 7.87f, 2.5f);
		
		
		inventory.add(compactDisk1);
		inventory.add(compactDisk2);
		inventory.add(compactDisk3);
		inventory.add(compactDisk4);
		inventory.add(compactDisk5);
		inventory.add(compactDisk6);
		inventory.add(compactDisk7);
		inventory.add(compactDisk8);
		inventory.add(compactDisk9);
		inventory.add(compactDisk10);
		
		System.out.println("Inventory:");
		
		for(int i = 0; i < inventory.size(); i++){
		
		System.out.println(inventory.get(i));
		}

}
}