import os
import argparse
import pandas as pd
from opentimspy.opentims import OpenTIMS


def get_args():
    arguments = argparse.ArgumentParser()
    arguments.add_argument('--input',
                           help='Input Bruker *.d directory containing timsTOF fleX raw data.',
                           required=True,
                           type=str)
    arguments.add_argument('--mz',
                           help='m/z value used to generate EIC/EIM.',
                           required=True,
                           nargs='+',
                           type=float)
    arguments.add_argument('--mz_tolerance',
                           help='m/z tolerance value used to generate EIC/EIM. m/z window is created for '
                                'm/z +/- mz_tolerance.',
                           default=0.05,
                           type=float)
    arguments.add_argument('--mz_tolerance_mode',
                           help='Whether m/z tolerance is absolute units ("Da") or relative units ("ppm").',
                           default='Da',
                           type=str)
    arguments.add_argument('--outdir',
                           help='Output directory for *.csv file containing extracted ion chromatogram or mobilogram.',
                           default='',
                           type=str)
    return vars(arguments.parse_args())


# Copied from TsfImagingDataViewer
# https://github.com/gtluu/TSFImagingDataViewer
def get_ppm_tolerance(mz, ppm):
    return ppm * (mz / (10**6))


# Modified from TIMSCONVERT
# https://github.com/gtluu/timsconvert
def dot_d_detection(input_directory):
    return [os.path.join(dirpath, directory) for dirpath, dirnames, filenames in os.walk(input_directory)
            for directory in dirnames if directory.endswith('.d')]


def export_chromatogram():
    args = get_args()
    if args['input'].endswith('.d'):
        list_of_input_files = [args['input']]
    else:
        list_of_input_files = dot_d_detection(args['input'])
    for infile in list_of_input_files:
        for mz in args['mz']:
            outfile = os.path.splitext(os.path.split(infile)[-1])[0]
            outfile = f"{outfile}_EIC_mz_{str(mz)}_tol_{args['mz_tolerance']}{args['mz_tolerance_mode']}"
            data = OpenTIMS(infile)
            data_df = pd.DataFrame(data.query(columns=data.all_columns))
            if args['mz_tolerance_mode'] == 'ppm':
                args['mz_tolerance'] = get_ppm_tolerance(mz, args['mz_tolerance'])
            data_df_subset = data_df[(data_df['mz'] >= mz - args['mz_tolerance']) &
                                     (data_df['mz'] <= mz + args['mz_tolerance'])]
            data_df_subset = data_df_subset[['retention_time', 'intensity']]
            data_df_subset = data_df_subset.groupby(by='retention_time', as_index=False).aggregate(func='sum')
            data_df_subset.to_csv(os.path.join(args['outdir'], f'{outfile}.csv'), header=False, index=False)


def export_mobilogram():
    args = get_args()
    if args['input'].endswith('.d'):
        list_of_input_files = [args['input']]
    else:
        list_of_input_files = dot_d_detection(args['input'])
    for infile in list_of_input_files:
        for mz in args['mz']:
            outfile = os.path.splitext(os.path.split(infile)[-1])[0]
            outfile = f"{outfile}_EIM_mz_{str(mz)}_tol_{args['mz_tolerance']}{args['mz_tolerance_mode']}"
            data = OpenTIMS(infile)
            data_df = pd.DataFrame(data.query(columns=data.all_columns))
            if args['mz_tolerance_mode'] == 'ppm':
                args['mz_tolerance'] = get_ppm_tolerance(mz, args['mz_tolerance'])
            data_df_subset = data_df[(data_df['mz'] >= mz - args['mz_tolerance']) &
                                     (data_df['mz'] <= mz + args['mz_tolerance'])]
            data_df_subset = data_df_subset[['inv_ion_mobility', 'intensity']]
            data_df_subset = data_df_subset.groupby(by='inv_ion_mobility', as_index=False).aggregate(func='sum')
            data_df_subset.to_csv(os.path.join(args['outdir'], f'{outfile}.csv'), header=False, index=False)
