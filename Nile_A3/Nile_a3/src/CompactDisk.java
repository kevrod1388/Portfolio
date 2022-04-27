

public class CompactDisk extends StoreItem {
	private String composer;
	private String artist;
	
	public CompactDisk(){
		
	}
	
	public CompactDisk(String title, String composer, 
		       String artist, String description, int year, 
		       float price, float weight){
		
		this.setTitle(title); 
		this.setDescription(description);
		this.setYear(year);
		this.setPrice(price);
		this.setWeight(weight);
		this.composer = composer;
		this.artist = artist;
		
	}
	
	
	


	public String getComposer() {
		return composer;
	}

	public void setComposer(String composer) {
		this.composer = composer;
	}

	public String getArtist() {
		return artist;
	}

	public void setArtist(String artist) {
		 this.artist = artist;
	}

	@Override
	public String toString() {
		return "CompactDisk [title = " + getTitle() + ", composer = " + composer + ", artist = " + artist
				+ ", description = " + getDescription() + ", Year = " + getYear() + ", Price = $"
				+ getPrice() + ",  Weight in oz. = " + getWeight() + "]";
	
	
	/*public String toString() {
		return "CompactDisk [title=" + getTitle() + ", composer=" + composer + ", artist=" + artist + "]";
	}*/
	
	

}
}
