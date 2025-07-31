# Java Implementation of COBOL Merge Sort Program

This is a Java implementation of the COBOL merge sort program from `merge_sort_test.cbl`.

## Overview

The program implements the exact same workflow as the original COBOL program:

1. **Generate test data** into two input files (`test-file-1.txt` and `test-file-2.txt`)
2. **Merge files** on ascending customerID into `merge-output.txt`
3. **Sort merged results** on descending contractID into `sorted-contract-id.txt`

## Classes

- **CustomerRecord**: Represents the customer data structure with exact field sizes matching COBOL:
  - customerID (5 digits)
  - lastName (50 chars)
  - firstName (50 chars)
  - contractID (5 digits)
  - comment (25 chars)

- **FileHandler**: Handles fixed-width record I/O matching COBOL's behavior
- **MergeSortProcessor**: Main class implementing the merge and sort operations

## File Format

The program maintains the same fixed-width record format as the original COBOL program:
- Total record length: 135 characters
- Fields are padded with spaces to maintain exact field widths
- Numbers are zero-padded on the left

## Usage

```bash
cd java-merge-sort/src/main/java
javac com/example/mergesort/*.java
java com.example.mergesort.MergeSortProcessor
```

## Test Data

The program generates the exact same test data as the COBOL version:

**test-file-1.txt** contains 6 records with customer IDs: 1, 5, 10, 50, 25, 75
**test-file-2.txt** contains 5 records with customer IDs: 999, 3, 30, 85, 24

## Output Files

- `merge-output.txt`: Records merged and sorted by customer ID (ascending)
- `sorted-contract-id.txt`: Records sorted by contract ID (descending)

## Ticket Reference

This implementation addresses ticket MBA-18.
