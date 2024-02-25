# Exif Geomapper
Returns location data from image and video files in DMS format.
## Requirements:
- FFMPEG installed on the system.
- Python libraries: 
  - ffmpeg-python==0.2.0
  - future==1.0.0
  - pillow==10.2.0
  - pillow_heif==0.15.0
## Considerations:
- Tested with MOV, JPEG, and HEIF files.
- Not all video formats will use the same location tags, so video formats other than MOV are not currently supported.
- Expects an `assets` folder containing the target files within the project's parent directory (`.../exif_geomapper/assets`). 
