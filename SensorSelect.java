package envir;
 
import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;
import java.util.logging.Level;
import java.util.logging.Logger;
 
public class SensorSelect
{
    public static void csvFilter(String wholeFile, int selected) {
    //    int selected = 2;
        
        Scanner scanner = null;
        try {
            scanner = new Scanner(new File(wholeFile));
        } catch (FileNotFoundException ex) {
            Logger.getLogger(SensorSelect.class.getName()).log(Level.SEVERE, null, ex);
        }        
        //Set the delimiter used in file
        scanner.useDelimiter(",");
         
        //Get column headers
        String topLine = scanner.nextLine();
        // Create ArrayList
        List<String> header = Arrays.asList(topLine.split(",")); 
        int sensor = header.indexOf("sensor");
        System.out.println("Index of sensor=" + sensor);
        while (scanner.hasNextLine())
        {
            List<String> csvLine = Arrays.asList(scanner.nextLine().split(",")); 
            if(csvLine.size() > 1) 
            {
                int sNum;
                sNum = Integer.valueOf(csvLine.get(sensor));
             
                if(sNum == selected )
                {    
                System.out.println("sNum=" + sNum + " " + csvLine);
                }
            }                   
        }  
        //Do not forget to close the scanner 
        scanner.close();          
    }
/*    public static void main(String[] args)// throws FileNotFoundException
    {
        SensorSelect.csvFilter("C:/envir/csvOut.csv", 0);
    }  */
}