from PyPDF2 import PdfFileReader
import sys


def print_meta(filepath):
    """ extract all meta data which can be found in the given file and print it to console """
    try:
        pdf_file = PdfFileReader(filepath, 'rb')
        doc_info = pdf_file.getDocumentInfo()
        print("[*] PDF meta data for: " + filepath)
        print("[*] Number of pages in file: {}".format(pdf_file.getNumPages()))

        for meta_item in doc_info:
            print("[+] " + meta_item + ':' + doc_info[meta_item])

        xmp_info = pdf_file.getXmpMetadata()
        for meta_xmp in xmp_info:
            print("[+] " + meta_xmp + ':' + xmp_info[meta_item])

    except FileNotFoundError:
        print("[!] Couldn't open '{}'! Make sure that the file exists.".format(filepath))
    except:
        pass

def print_help():
    print("Usage: python read_pdf_meta_data.py <pdf-filepath>")
    print("--- <pdf-filepath>: Path to the pdf-file which from which to extract the meta data")


if __name__ == "__main__":
    if (len(sys.argv) != 2): # 2 because [0] is script name
        print("Error: Number of given input parameters ({}) does not match expected one (2):".format(len(sys.argv)))
        print_help()
        sys.exit(1)

    # get filepath and print meta data
    pdf_filepath = sys.argv[1]
    print_meta(pdf_filepath)
