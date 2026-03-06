# Bruker NIR Spectrum Converter

[简体中文](README.md) | English

A tool to convert Bruker OPUS NIR spectrum `.0` format files to universal TXT format.

## Features

- ✅ Parse Bruker OPUS `.0` format spectrum files
- ✅ Auto-extract wavenumber/wavelength and absorbance data
- ✅ Batch convert all files in a directory
- ✅ Output includes wavenumber (cm⁻¹), wavelength (nm), and absorbance
- ✅ Pure Python implementation, no external dependencies (only NumPy required)

## Supported Spectrum Range

| Parameter | Value |
|-----------|-------|
| Data Points | 1899 |
| Wavenumber Range | 3948 - 11540 cm⁻¹ |
| Wavelength Range | 866.6 - 2532.9 nm |

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/bruker-nir-converter.git
cd bruker-nir-converter

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Command Line

```bash
# Convert single file
python bruker_converter.py path/to/spectrum.0

# Convert entire directory
python bruker_converter.py path/to/spectra_folder

# Specify output directory
python bruker_converter.py path/to/spectra_folder output_folder
```

### Python Code

```python
from bruker_converter import parse_bruker_spectrum, save_to_txt

# Parse spectrum file
wavenumbers, wavelengths, absorbance_data, npt = parse_bruker_spectrum('spectrum.0')

# Save to TXT
save_to_txt('output.txt', wavenumbers, wavelengths, absorbance_data, npt)
```

## Output Format

The converted TXT file format:

```txt
# ========================================
# Bruker NIR Spectrum Data Converter
# ========================================
#
# Data points: 1899
# Wavenumber range: 3948.0 - 11540.0 cm-1
# Wavelength range: 2532.9 - 866.6 nm
#
# Format: Wavenumber(cm-1) | Wavelength(nm) | Absorbance
# ========================================
11540.0000	866.5511	0.000000
11536.0000	866.8516	0.000000
...
```

## File Format Parsing

This tool parses the following parameters from Bruker OPUS `.0` format files:

| Parameter | File Offset | Data Type |
|-----------|-------------|-----------|
| Data Points (NPT) | 0x46c | int16 |
| Start Wavenumber (FXV) | 0x478 | float64 |
| End Wavenumber (LXV) | 0x488 | float64 |
| Absorbance Data | 0x24c00 | float32[] |

## Testing

The project includes a test file `test/test.0` to verify the conversion:

```bash
python bruker_converter.py test/
```

## Requirements

- Python 3.7+
- NumPy

## License

MIT License - Feel free to use and modify

## Author

Matrix Agent

## Reference

- [Matlab Parse Bruker .0 Format Spectrum File](https://blog.csdn.net/NIR_cloud/article/details/128788340)
