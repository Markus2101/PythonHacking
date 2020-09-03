# PythonHacking

The examples in this repository are mainly taken from following books:
- [Black Hat Python](https://www.amazon.de/Black-Hat-Python-Programming-Pentesters/dp/1593275900) (Justin Seitz)
- [Python Hacking](https://www.amazon.de/Python-Hacking-Lernen-Sprache-schlie%C3%9Fen-ebook/dp/B01BNV7IMM/ref=sr_1_2?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=python+hacking+t+j&qid=1599134126&sr=8-2) (T. J. O'Connor)

Though not always copied 1 to 1, the examples are very similar to the ones mentioned in above books.
However, the examples in this repository are implemented for Python versions >= 3.x.


## Internet Protocol (IPv4 header)

| 0 - 3: Version | 4 - 7: Header Length | 8 - 15: Type of Service | 16 - 31: Total Length                     |  
| 32 - 47: Identification                                         | 48 - 50: Flags | 51 - 63: Fragment Offset |  
| 64 - 71: Time to Live                 | 72 - 79: Protocol       | 80 - 95: Header Checksum                  |  
| 96 - 127: Source IP Address                                                                                 |  
| 128 - 159: Destination IP Address                                                                           |  
| 160 - 191: Options                                                                                          |  
