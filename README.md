# PythonHacking

The examples in this repository are mainly taken from following books:
- Black Hat Python (Justin Seitz)
- Python Hacking (T. J. O'Connor)

Though not always copied 1 to 1, the examples are very similar to the ones mentioned in above books.


## Internet Protocol (IPv4 header)

| 0 - 3: Version | 4 - 7: Header Length | 8 - 15: Type of Service | 16 - 31: Total Length                     |  
| 32 - 47: Identification                                         | 48 - 50: Flags | 51 - 63: Fragment Offset |  
| 64 - 71: Time to Live                 | 72 - 79: Protocol       | 80 - 95: Header Checksum                  |  
| 96 - 127: Source IP Address                                                                                 |  
| 128 - 159: Destination IP Address                                                                           |  
| 160 - 191: Options                                                                                          |  
