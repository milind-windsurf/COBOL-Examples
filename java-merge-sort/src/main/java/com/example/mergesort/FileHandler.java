package com.example.mergesort;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class FileHandler {
    
    public static void writeCustomerRecords(String filename, List<CustomerRecord> records) throws IOException {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filename))) {
            for (CustomerRecord record : records) {
                writer.write(record.toFixedWidthString());
                writer.newLine();
            }
        }
    }
    
    public static List<CustomerRecord> readCustomerRecords(String filename) throws IOException {
        List<CustomerRecord> records = new ArrayList<>();
        
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = reader.readLine()) != null) {
                if (!line.trim().isEmpty()) {
                    records.add(CustomerRecord.fromFixedWidthString(line));
                }
            }
        }
        
        return records;
    }
}
