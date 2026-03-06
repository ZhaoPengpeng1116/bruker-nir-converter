# -*- coding: utf-8 -*-
"""
Bruker NIR Spectrum Converter
Convert Bruker OPUS .0 format NIR spectrum files to TXT format
"""

import struct
import numpy as np
import os
import sys
import glob


def parse_bruker_spectrum(file_path):
    """
    Parse Bruker spectrum file
    
    Args:
        file_path: Path to .0 format spectrum file
    
    Returns:
        wavenumbers: Wavenumber array (cm-1)
        wavelengths: Wavelength array (nm)  
        absorbance_data: Absorbance array
        npt: Number of data points
    """
    
    with open(file_path, 'rb') as f:
        full_data = f.read()
    
    print(f"File: {os.path.basename(file_path)}")
    print(f"File size: {len(full_data)} bytes")
    
    # ======== Extract Parameters ========
    
    # 1. Number of points (NPT) - offset 0x46c, little-endian int16
    npt = struct.unpack('<h', full_data[0x46c:0x46e])[0]
    print(f"Data points (NPT): {npt}")
    
    # 2. Start wavenumber (FXV) - offset 0x478, little-endian float64
    start_wavenumber = struct.unpack('<d', full_data[0x478:0x480])[0]
    print(f"Start wavenumber (FXV): {start_wavenumber} cm-1")
    
    # 3. End wavenumber (LXV) - offset 0x488, little-endian float64
    end_wavenumber = struct.unpack('<d', full_data[0x488:0x490])[0]
    print(f"End wavenumber (LXV): {end_wavenumber} cm-1")
    
    # 4. Absorbance data - offset 0x24c00, single precision float array
    absorbance_start = 0x24c00
    absorbance_data = np.frombuffer(
        full_data[absorbance_start:absorbance_start+npt*4], 
        dtype=np.float32
    )
    print(f"Absorbance data points: {len(absorbance_data)}")
    
    # ======== Calculate Wavelength ========
    # Generate equidistant wavenumber array (from high to low)
    wavenumbers = np.linspace(start_wavenumber, end_wavenumber, npt)
    
    # Convert to wavelength (nm)
    # wavelength(nm) = 10000000 / wavenumber(cm-1)
    wavelengths = 10000000.0 / wavenumbers
    
    print(f"\nWavenumber range: {wavenumbers[-1]:.1f} - {wavenumbers[0]:.1f} cm-1")
    print(f"Wavelength range: {wavelengths[-1]:.1f} - {wavelengths[0]:.1f} nm")
    
    return wavenumbers, wavelengths, absorbance_data, npt


def save_to_txt(output_path, wavenumbers, wavelengths, absorbance_data, npt):
    """
    Save to TXT format
    
    Args:
        output_path: Output file path
        wavenumbers: Wavenumber array
        wavelengths: Wavelength array
        absorbance_data: Absorbance array
        npt: Number of data points
    """
    
    with open(output_path, 'w', encoding='utf-8') as f:
        # Write header
        f.write("# ========================================\n")
        f.write("# Bruker NIR Spectrum Data Converter\n")
        f.write("# ========================================\n")
        f.write("#\n")
        f.write(f"# Data points: {npt}\n")
        f.write(f"# Wavenumber range: {wavenumbers[-1]:.1f} - {wavenumbers[0]:.1f} cm-1\n")
        f.write(f"# Wavelength range: {wavelengths[-1]:.1f} - {wavelengths[0]:.1f} nm\n")
        f.write("#\n")
        f.write("# Format: Wavenumber(cm-1) | Wavelength(nm) | Absorbance\n")
        f.write("# ========================================\n")
        
        # Write data
        for i in range(npt):
            f.write(f"{wavenumbers[i]:.4f}\t{wavelengths[i]:.4f}\t{absorbance_data[i]:.6f}\n")
    
    return output_path


def convert_file(input_path, output_dir=None):
    """
    Convert single file
    
    Args:
        input_path: Input file path
        output_dir: Output directory (default: input file directory)
    
    Returns:
        output_path: Output file path
    """
    
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File not found: {input_path}")
    
    # Determine output directory
    if output_dir is None:
        output_dir = os.path.dirname(input_path)
    
    # Parse spectrum
    wavenumbers, wavelengths, absorbance_data, npt = parse_bruker_spectrum(input_path)
    
    # Generate output filename
    input_name = os.path.basename(input_path)
    base_name = os.path.splitext(input_name)[0]
    output_file = f"{base_name}.txt"
    output_path = os.path.join(output_dir, output_file)
    
    # Save
    save_to_txt(output_path, wavenumbers, wavelengths, absorbance_data, npt)
    
    print(f"\n✓ Converted: {output_path}")
    
    return output_path


def batch_convert(input_dir, output_dir=None, pattern="*.0"):
    """
    Batch convert all matching files in directory
    
    Args:
        input_dir: Input directory
        output_dir: Output directory (default: input directory)
        pattern: File matching pattern (default: *.0)
    
    Returns:
        List of successfully converted files
    """
    
    # Find all matching files
    search_pattern = os.path.join(input_dir, pattern)
    files = glob.glob(search_pattern)
    
    if not files:
        print(f"No files matching {pattern} found in {input_dir}")
        return []
    
    print(f"Found {len(files)} files to convert\n")
    
    converted = []
    for file_path in files:
        try:
            output_path = convert_file(file_path, output_dir)
            converted.append(output_path)
        except Exception as e:
            print(f"✗ Conversion failed {file_path}: {e}")
    
    print(f"\nConversion complete: {len(converted)}/{len(files)} files successful")
    
    return converted


def main():
    """Main entry point"""
    
    print("=" * 60)
    print("  Bruker NIR Spectrum Converter")
    print("=" * 60)
    print()
    
    # Determine run mode
    if len(sys.argv) > 1:
        # Command line mode
        input_path = sys.argv[1]
        
        if os.path.isfile(input_path):
            # Single file conversion
            output_dir = sys.argv[2] if len(sys.argv) > 2 else None
            convert_file(input_path, output_dir)
            
        elif os.path.isdir(input_path):
            # Directory batch conversion
            output_dir = sys.argv[2] if len(sys.argv) > 2 else None
            batch_convert(input_dir, output_dir)
        else:
            print(f"Error: Path does not exist - {input_path}")
    else:
        # Default: convert all .0 files in test directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        test_dir = os.path.join(script_dir, "test")
        
        if os.path.exists(test_dir):
            print(f"Converting files in test directory...\n")
            batch_convert(test_dir, script_dir)
        else:
            print("Usage:")
            print("  python bruker_converter.py <file_path>")
            print("  python bruker_converter.py <input_dir> [output_dir]")


if __name__ == "__main__":
    main()
