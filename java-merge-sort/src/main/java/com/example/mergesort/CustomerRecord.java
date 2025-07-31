package com.example.mergesort;

public class CustomerRecord {
    private int customerID;
    private String lastName;
    private String firstName;
    private int contractID;
    private String comment;
    
    public CustomerRecord() {
    }
    
    public CustomerRecord(int customerID, String lastName, String firstName, int contractID, String comment) {
        this.customerID = customerID;
        this.lastName = lastName;
        this.firstName = firstName;
        this.contractID = contractID;
        this.comment = comment;
    }
    
    public int getCustomerID() {
        return customerID;
    }
    
    public void setCustomerID(int customerID) {
        this.customerID = customerID;
    }
    
    public String getLastName() {
        return lastName;
    }
    
    public void setLastName(String lastName) {
        this.lastName = lastName;
    }
    
    public String getFirstName() {
        return firstName;
    }
    
    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }
    
    public int getContractID() {
        return contractID;
    }
    
    public void setContractID(int contractID) {
        this.contractID = contractID;
    }
    
    public String getComment() {
        return comment;
    }
    
    public void setComment(String comment) {
        this.comment = comment;
    }
    
    public String toFixedWidthString() {
        return String.format("%05d%-50s%-50s%05d%-25s", 
            customerID, 
            padRight(lastName, 50), 
            padRight(firstName, 50), 
            contractID, 
            padRight(comment, 25));
    }
    
    public static CustomerRecord fromFixedWidthString(String line) {
        if (line.length() < 135) {
            throw new IllegalArgumentException("Line too short for customer record: " + line.length());
        }
        
        int customerID = Integer.parseInt(line.substring(0, 5));
        String lastName = line.substring(5, 55).trim();
        String firstName = line.substring(55, 105).trim();
        int contractID = Integer.parseInt(line.substring(105, 110));
        String comment = line.substring(110, 135).trim();
        
        return new CustomerRecord(customerID, lastName, firstName, contractID, comment);
    }
    
    private static String padRight(String str, int length) {
        if (str == null) str = "";
        if (str.length() >= length) {
            return str.substring(0, length);
        }
        return str + " ".repeat(length - str.length());
    }
    
    @Override
    public String toString() {
        return toFixedWidthString();
    }
}
