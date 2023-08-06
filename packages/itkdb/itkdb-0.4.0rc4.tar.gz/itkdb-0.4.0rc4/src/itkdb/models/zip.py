from io import BytesIO
import zipfile
import re
import logging
import html

log = logging.getLogger(__name__)


class ZipFile(zipfile.ZipFile):
    def __init__(self, content=None, filename=None):
        self._content = content
        super(ZipFile, self).__init__(BytesIO(self._content))
        self.filename = filename
        self.format = filename.split(".")[-1].lower()

    def save(self, filename=None, mode="wb"):
        filename = filename or self.filename
        nbytes = len(self._content)
        with open(filename, mode) as f:
            f.write(self._content)
        log.info("Written {0:d} bytes to {1:s}".format(nbytes, filename))
        return nbytes

    def _repr_html_(self):
        return (
            html.escape(repr(self))
            + "<ul><li>"
            + "</li><li>".join(map(lambda x: html.escape(repr(x)), self.filelist))
            + "</li></ul>"
        )

    @classmethod
    def from_response(cls, response):
        filename = re.findall(
            "filename=(.+)", response.headers.get("content-disposition")
        )[0]
        return cls(content=response.content, filename=filename)
