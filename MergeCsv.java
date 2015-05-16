/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package envir;
//MergeDemo.java
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
//import java.util.Arrays;
import java.util.Iterator;
import java.util.Scanner;

public class MergeCsv {


    public static void mergeCsvFiles(String[] csvFiles) throws IOException {

        // Variables
        ArrayList<File> files = new ArrayList<File>();
        Iterator<File> iterFiles;
        File fileOutput;
        BufferedWriter fileWriter;
        BufferedReader fileReader;
        String csvFile;
        String csvFinal = "C:\\envir\\csvOut.csv";
        String[] headers = null;
        String header = null;
        int numFiles = csvFiles.length;

        // Files: Input
        for (int i = 0; i < numFiles; i++) {
            csvFile = "C:\\envir\\tojoin\\" + csvFiles[i];
            files.add(new File(csvFile));
        }
        System.out.println(files);

        // Files: Output
        fileOutput = new File(csvFinal);
        if (fileOutput.exists()) {
            fileOutput.delete();
        }
        try {
            fileOutput.createNewFile();
            // log
            // System.out.println("Output: " + fileOutput);
        } catch (IOException e) {
            // log
        }

        iterFiles = files.iterator();
        fileWriter = new BufferedWriter(new FileWriter(csvFinal, true));

        try ( // Headers
                Scanner scanner = new Scanner(files.get(0))) {
            if (scanner.hasNextLine())
                header = scanner.nextLine();
            // if (scanner.hasNextLine()) headers = scanner.nextLine().split(";");
        }

        /*
         * System.out.println(header); for(String s: headers){
         * fileWriter.write(s); System.out.println(s); }
         */

        fileWriter.write(header);
        fileWriter.newLine();

        while (iterFiles.hasNext()) {

            String line;// = null;
            String[] firstLine;// = null;

            File nextFile = iterFiles.next();
            fileReader = new BufferedReader(new FileReader(nextFile));

            if ((line = fileReader.readLine()) != null)
                firstLine = line.split(";");

            while ((line = fileReader.readLine()) != null) {
                fileWriter.write(line);
                fileWriter.newLine();
            }
            fileReader.close();
        }

        fileWriter.close();

    }

}

