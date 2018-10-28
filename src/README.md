1. In the main() function, a list of column names is stored as follow:

    list column_header = ["header1", "header2", ...]

If a new data file has a column name (e.g., "header_new") that is not included in the list, just manually add that name into the list:

    list column_header = ["header1", "header2", ..., "header_new"]

The program should be good to run without further change.

2. The number 10 (for Top 10 Occupations and Top 10 States) is not hard-coded, it can be changed to the desired value by passing a different argument to process_file().
