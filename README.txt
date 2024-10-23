tdf_batch_chromatogram_mobilogram_export

About
This package is a simple script to batch export extracted ion chromatograms and extracted ion mobilograms from Bruker
timsTOF *.d directories containing TDF files.

Installation
1. If not installed, install Anaconda from https://www.anaconda.com/download.
2. Open Anaconda Prompt.
3. Create a new conda virtual environment: conda create -n tdf_batch_chromatogram_mobilogram_export python=3.12
4. Activate the venv: conda activate tdf_batch_chromatogram_mobilogram_export
5. Install this package: pip install git+https://github.com/gtluubruker/tdf_batch_chromatogram_mobilogram_export.git

Usage
Two commands are available: export_chromatogram and export_mobilogram. For a list of all parameters and descriptsions,
run one of the following commands:

export_chromatogram --help
export_mobilogram --help

Examples

Single *.d directory and Single m/z Values
export_chromatogram --input data.d --outdir D:\chromatograms --mz 622.0 --mz_tolerance 0.05 --mz_tolerance_mode Da
export_mobilogram --input data.d --outdir D:\mobilograms --mz 622.0 --mz_tolerance 20 --mz_tolerance_mode ppm

Multiple *.d directories and Multiple m/z Values
export_chromatogram --input path_to_folder_with_data --outdir D:\chromatograms --mz 622.0 922.0 --mz_tolerance 20 --mz_tolerance_mode ppm
export_mobilogram --input path_to_folder_with_data --outdir D:\mobilograms --mz 622.0 922.0 --mz_tolerance 0.05 --mz_tolerance_mode Da
