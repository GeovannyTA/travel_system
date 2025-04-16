from PIL import Image, ExifTags
from fractions import Fraction
from datetime import datetime
from django.utils import timezone

def extract_metadata(file_obj):
    try:
        image = Image.open(file_obj)
        exif_data = image._getexif()
        if not exif_data:
            return None

        exif = {ExifTags.TAGS.get(tag, tag): value for tag, value in exif_data.items()}

        gps_info = exif.get("GPSInfo")
        if not gps_info:
            return None

        gps_data = {ExifTags.GPSTAGS.get(k, k): gps_info[k] for k in gps_info.keys()}

        lat = convert_to_degrees(gps_data["GPSLatitude"])
        if gps_data["GPSLatitudeRef"] != "N":
            lat = -lat

        lon = convert_to_degrees(gps_data["GPSLongitude"])
        if gps_data["GPSLongitudeRef"] != "E":
            lon = -lon

        alt = gps_data.get("GPSAltitude")
        alt = float(Fraction(alt)) if alt else None

        raw_fecha = clean_exif_string(exif.get("DateTimeOriginal", ""))
        fecha = None
        if raw_fecha:
            fecha = timezone.make_aware(
                datetime.strptime(raw_fecha, "%Y:%m:%d %H:%M:%S")
            )

        return {
            "lat": lat,
            "lon": lon,
            "alt": alt,
            "fecha": fecha,
            "marca": clean_exif_string(exif.get("Make", "No disponible")),
            "model": clean_exif_string(exif.get("Model", "No disponible")),
            "software": clean_exif_string(exif.get("Software", "No disponible")),
            "orientacion": exif.get("Orientation", 1),
            "direccion": clean_exif_string(exif.get("GPSImgDirection", 0)),
        }
    except Exception as e:
        print(f"Error extrayendo metadatos: {e}")
        return None


def convert_to_degrees(value):
    d = float(Fraction(value[0]))
    m = float(Fraction(value[1]))
    s = float(Fraction(value[2]))
    return d + (m / 60.0) + (s / 3600.0)


# Limpia los caracteres nulos de la cadena EXIF
def clean_exif_string(value):
    if isinstance(value, str):
        return value.replace("\x00", "").strip()
    return value
