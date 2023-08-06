from borb.pdf.document.document import Document as BorbDocument
from borb.pdf import PDF as BorbPDF

from .page import Page


class Document(BorbDocument):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def add_page(self, *args, **kwargs) -> Page:
        # (Overridden method)
        # If called with no arguments, we automatically create and return
        # a new Page object.
        # By default, the page is set to Letter sized instead of A4.
        if len(args) + len(kwargs) == 0:
            page = Page()
            self.add_page(page)
            return page
        else:
            return super().add_page(*args, **kwargs)


    def save(self, filename: str) -> None:
        # (New Warbler method that makes saving PDF files easier.)
        with open(filename, 'wb') as pdf_file_handle:
            BorbPDF.dumps(pdf_file_handle, self)

