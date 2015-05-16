/**
 * getCsvList takes pathName to give list of filtered CSV files
 * listToArray takes list length to initialise csvArray.
 * csvArray is sorted by date
 */
package envir;

import java.io.File;
import java.io.FilenameFilter;
import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

public class DirToList{
        
    public static List<String> getCsvList(String dirPath) {
        File dir = new File(dirPath);
        
        List<String> list = Arrays.asList(dir.list(
            new FilenameFilter() {
                @Override public boolean accept(File dir, String name) {
                return name.endsWith(".csv");
                }
            }
        ));
        return list;
    }
    public static String[] listToArray(List<String> fList, int fLen) {
        String[] csvArray = new String[fLen];
        for (int i = 0; i < fLen; i++) {
            csvArray[i] = fList.get(i);
        }
        return csvArray;
    }
    public static void main(String[] args) {
        String dPath = "C:/envir/toJoin";
        int fLen = getCsvList(dPath).size();
        String[] csvSeq = listToArray(getCsvList(dPath), fLen);
        Arrays.sort(csvSeq);
        try {
            MergeCsv.mergeCsvFiles(csvSeq);
        //        for (int i = 0; i < fLen; i++) {
          //        System.out.println(csvSeq[i]+" "+i);
            //}
        } catch (IOException ex) {
            Logger.getLogger(DirToList.class.getName()).log(Level.SEVERE, null, ex);
        }
        SensorSelect.csvFilter("C:/envir/csvOut.csv", 0);
    }   
}
