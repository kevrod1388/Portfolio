import java.util.ArrayList;
 
public class Inventory {
    
     private ArrayList <StoreItem> inventory = new
                   ArrayList<>();
    
     public Inventory () {
         
     }
    
     public void add (StoreItem item) {
          inventory.add(item);
     }
    
     public StoreItem get(int index) {
          if ((index >= 0) && (index < inventory.size())) {
              return inventory.get(index);
          }
          return null;
     }
 
   public int size () {
           return inventory.size();
     }
 
}