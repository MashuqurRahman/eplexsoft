import zipfile
import requests
from django.core.files.base import ContentFile

class RowError(Exception):
    pass


def _clean(value):
    if value is None:
        return ""
    return str(value).strip()


SL_HEADER_ALIASES = {
    "sl", "sl no", "sl no.", "sl.", "sl#", "serial no", "serial no.",
    "serial number", "si", "si no",
}


def sl_column_index(header_row):
    for i, cell in enumerate(header_row or []):
        if _clean(cell).lower() in SL_HEADER_ALIASES:
            return i
    return None


def display_row_number(row, sl_idx, fallback_row_num):
    if sl_idx is not None and sl_idx < len(row):
        val = row[sl_idx]
        if val is not None:
            if isinstance(val, float) and val.is_integer():
                return str(int(val))
            text = str(val).strip()
            if text:
                return text
    return fallback_row_num


class ImageResolver:
    def __init__(self, images_zip_file):
        self._zip = None
        if images_zip_file:
            self._zip = zipfile.ZipFile(images_zip_file)
            self._zip_names = {info.filename.split("/")[-1]: info.filename for info in self._zip.infolist() if not info.is_dir()}
        else:
            self._zip_names = {}
        self._url_cache = {}

    def resolve(self, value, field_label, required=True):
        value = _clean(value)
        if not value:
            if required:
                raise RowError(f"{field_label} cannot be left empty")
            return None

        if value.lower().startswith("http://") or value.lower().startswith("https://"):
            if value in self._url_cache:
                data, name = self._url_cache[value]
            else:
                try:
                    resp = requests.get(value, timeout=20)
                    resp.raise_for_status()
                    data = resp.content
                except requests.RequestException as e:
                    raise RowError(f"{field_label} could not be downloaded from the URL: {e}")
                name = value.split("/")[-1].split("?")[0] or "image.jpg"
                self._url_cache[value] = (data, name)
            return ContentFile(data, name=name)

        if not self._zip:
            raise RowError(f"{field_label} = '{value}' looks like a filename, but no Images ZIP was uploaded")
        real_name = self._zip_names.get(value)
        if not real_name:
            raise RowError(f"{field_label} = '{value}' file was not found inside the ZIP")
        data = self._zip.read(real_name)
        return ContentFile(data, name=value)