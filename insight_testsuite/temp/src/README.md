In the main() function, a list of column names is stored as follow:

    list column_header = ["header1", "header2", ...]

If a new data file has a column name (e.g., "header_new") that is not included in the list, just manually add that name into the list:

    list column_header = ["header1", "header2", ..., "header_new"]

The program should be good to run without further change.