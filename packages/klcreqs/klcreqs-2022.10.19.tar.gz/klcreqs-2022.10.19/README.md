# klcreqs
library for streamlining requests to apis

# formula_api
to make a formula api request:
1. call the class with formula_api_request()
2. necessary arguments:
   * formulas -> list
   * ep (endpoint) -> string
        For time series requests accepted values are 'ts', 'time', 'timeseries', 'time_series', 'time series'
        For cross sectional requests accepted values are 'cs', 'cross', 'crossseectional', 'cross_sectional', 'cross sectional'
3. optional arguments:
   * ids -> list
   * uni (universe) -> string
        formulas must contain ofdb reference(s) if these are not included or the request will fail.
   * batch -> boolean
        set to True to submit the request as a batch - defaults to False
   * dnames -> tuple
        optional list of column names to be returned as headers for the requested data in place of messy default FS headers - defaults to None
   * bof (batch-on-fail) -> boolean
        set to True to automatically resubmit the request as a batch if the initial request fails - defaults fo False
4. thats it! call the .df() function on the request object to return requested data as a pandas DataFrame

# ofdb_api
call the ofdb_api class with path as the single required argument
call desired method on class in same line
must pass in date (d=) to methods as integer in YYYYMMDD format
symbols and paths args must be strings
any status_code >= 400 will prompt a print of response and response.text

methods:
1. get_dates()
    * returns list of dates in specified ofdb
2. delete_date()
    * deletes specified date
    * returns nothing
3. delete_symbol(*symbol, **d)
    * deletes specified symbol, can specify date for more precision
    * returns nothing
4. parse_upload(*df)
    * must pass in pandas DataFrame, which will then be broken into a dict using predetermined symbols as the index, and the df index as the keys, then parsed into json and uploaded to ofdb symbol-wise
    * returns request and request.text
5. parse_upload_datewise(*df)
    * must pass in pandas DataFrame, which will then be broken into a dict using listed dates as the index. and the df index as the keys, then parsed into json and uploaded to ofdb date-wise
    * returns request and request.text
