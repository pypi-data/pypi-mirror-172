# Common test data for jsonurl

See http://jsonurl.org/

Format is a mapping of "test case name" to "test case". Each "test case" has a type which is one of:
* "roundtrip" (default if missing): text and data must be match perfectly on load save
* "fail": text must fail with a parsing error
* "load": text must load into exact data but save may not be exact

See [./schema.json](./schema.json)
