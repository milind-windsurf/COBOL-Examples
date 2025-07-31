package com.example.mergesort;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class MergeSortProcessor {
    
    public static void main(String[] args) {
        try {
            MergeSortProcessor processor = new MergeSortProcessor();
            processor.run();
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    public void run() throws IOException {
        System.out.println("Creating test data files...");
        createTestData();
        
        System.out.println("Merging and sorting files...");
        mergeFiles();
        
        System.out.println("Sorting merged file on descending contract id....");
        sortByContractId();
        
        System.out.println("Done.");
    }
    
    private void createTestData() throws IOException {
        List<CustomerRecord> testFile1Records = new ArrayList<>();
        testFile1Records.add(new CustomerRecord(1, "last-1", "first-1", 5423, "comment-1"));
        testFile1Records.add(new CustomerRecord(5, "last-5", "first-5", 12323, "comment-5"));
        testFile1Records.add(new CustomerRecord(10, "last-10", "first-10", 653, "comment-10"));
        testFile1Records.add(new CustomerRecord(50, "last-50", "first-50", 5050, "comment-50"));
        testFile1Records.add(new CustomerRecord(25, "last-25", "first-25", 7725, "comment-25"));
        testFile1Records.add(new CustomerRecord(75, "last-75", "first-75", 1175, "comment-75"));
        
        List<CustomerRecord> testFile2Records = new ArrayList<>();
        testFile2Records.add(new CustomerRecord(999, "last-999", "first-999", 1610, "comment-99"));
        testFile2Records.add(new CustomerRecord(3, "last-03", "first-03", 3331, "comment-03"));
        testFile2Records.add(new CustomerRecord(30, "last-30", "first-30", 8765, "comment-30"));
        testFile2Records.add(new CustomerRecord(85, "last-85", "first-85", 4567, "comment-85"));
        testFile2Records.add(new CustomerRecord(24, "last-24", "first-24", 247, "comment-24"));
        
        FileHandler.writeCustomerRecords("test-file-1.txt", testFile1Records);
        FileHandler.writeCustomerRecords("test-file-2.txt", testFile2Records);
    }
    
    private void mergeFiles() throws IOException {
        List<CustomerRecord> file1Records = FileHandler.readCustomerRecords("test-file-1.txt");
        List<CustomerRecord> file2Records = FileHandler.readCustomerRecords("test-file-2.txt");
        
        List<CustomerRecord> mergedRecords = new ArrayList<>();
        mergedRecords.addAll(file1Records);
        mergedRecords.addAll(file2Records);
        
        mergedRecords.sort(Comparator.comparingInt(CustomerRecord::getCustomerID));
        
        FileHandler.writeCustomerRecords("merge-output.txt", mergedRecords);
        
        System.out.println("Merged records (sorted by customer ID ascending):");
        for (CustomerRecord record : mergedRecords) {
            System.out.println(record.toFixedWidthString());
        }
    }
    
    private void sortByContractId() throws IOException {
        List<CustomerRecord> mergedRecords = FileHandler.readCustomerRecords("merge-output.txt");
        
        mergedRecords.sort(Comparator.comparingInt(CustomerRecord::getContractID).reversed());
        
        FileHandler.writeCustomerRecords("sorted-contract-id.txt", mergedRecords);
        
        System.out.println("Records sorted by contract ID descending:");
        for (CustomerRecord record : mergedRecords) {
            System.out.println(record.toFixedWidthString());
        }
    }
}
