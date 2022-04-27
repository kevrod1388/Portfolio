
public class Book extends StoreItem {
	private String author;
	private String subject;
	private boolean hardcover;
	private int pages;
	
	public Book(){
		
	}
	
	public  Book(String title, String author, String subject, 
		       String description, boolean hardcover, int pages, 
		       int year,float price, float weight){
		

		// title
		//description
		// year
		// price
		// weight
		
		this.setTitle(title); 
		this.setDescription(description);
		this.setYear(year);
		this.setPrice(price);
		this.setWeight(weight);
		this.author = author;
		this.subject = subject;
		this.hardcover = hardcover;
		this.pages = pages ;
		
	}
	
	public String getAuthor(){
		return author;
	}
	
	public String setAuthor( String author){
		
		return this.author;
	}
	
	public String getSubject(){
		return subject;
	}
	
	public String setSubject( String subject){
		
		return this.subject;
	}
	
	public boolean getHardcover(){
		return hardcover;
	}
	
	public boolean setHardcover( boolean hardcover){
		return this.hardcover;
	}
	
	public int getPages(){
		return pages;
	}
	
	public int setPages( int pages ){
		return this.pages;
	}

	public String toString() {
	return "Book [title = " + getTitle()+ ", author = " + author + ", subject = " + subject
			+ ", hardcover = " + hardcover + ", description = " + getDescription() +
			", pages = " + pages + ", year = " + getYear() + ", price = $" + getPrice() +
			", weight in oz. = " + getWeight() + "]";
		
	}
	
}
