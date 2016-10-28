# =============================================================================
#
# Author:	Kjell Swedin
# Purpose:	Compare old Consume results with new Consume results
#
# =============================================================================
import sys
import pandas as pd
import numpy as np

spaces = {
    'total consumption': 'c_total',
    'canopy consumption': 'c_canopy',
    'shrub consumption': 'c_shrub',
    'herb consumption': 'c_herb',
    'wood consumption': 'c_wood',
    'llm consumption': 'c_llm',
    'ground consumption': 'c_ground',
    'ch4 emissions': 'ch4',
    'co emissions': 'co',
    'co2 emissions': 'co2',
    'nmhc emissions': 'nmhc',
    'pm emissions': 'pm',
    'pm10 emissions': 'pm10',
    'pm25 emissions': 'pm25',
    'c_basal_accum': 'c_basal',
    'total heat release': 'heat_total',
    'flaming heat release': 'heat_flaming',
    'smoldering heat release': 'heat_smoldering',
    'residual heat release': 'heat_residual'
}



def usage():
    print('\nCompare old and new Consume results')
    print('    Supply the old file and the new file as arguments. Old first, new second\n')

def rename_columns(df_old):
    cols = {col:col.lower() for col in df_old.columns}    
    df_old.rename(columns=cols, inplace=True)
    df_old.rename(columns=spaces, inplace=True)
    return df_old
    
def compute_diff(df_old, df_new, col):
    a = df_old.get(col)
    b = df_new.get(col)
    return np.where(((a > 1) & (b > 1)),
        np.round(((a - b) / (np.maximum(a, b))) * 100, 2),
        '       --'
        )
    
def write_merged(df_old, df_new):
    df_old.fillna(0, inplace=True)
    df_new.fillna(0, inplace=True)
    df = pd.DataFrame({
        'fuelbed': df_old.fuelbeds,
        'filename': df_old.filename,
        'c_total_new': np.round(df_new.c_total, 2),
        'c_total_old': np.round(df_old.c_total, 2),
        'c_total_diff': compute_diff(df_old, df_new, 'c_total'),
        'c_canopy_new': np.round(df_new.c_canopy, 2),
        'c_canopy_old': np.round(df_old.c_canopy, 2),
        'c_canopy_diff': compute_diff(df_old, df_new, 'c_canopy'),
        'c_shrub_new': np.round(df_new.c_shrub, 2),
        'c_shrub_old': np.round(df_old.c_shrub, 2),
        'c_shrub_diff': compute_diff(df_old, df_new, 'c_shrub'),
        'c_herb_new': np.round(df_new.c_herb, 2),
        'c_herb_old': np.round(df_old.c_herb, 2),
        'c_herb_diff': compute_diff(df_old, df_new, 'c_herb'),
        'c_wood_new': np.round(df_new.c_wood, 2),
        'c_wood_old': np.round(df_old.c_wood, 2),
        'c_wood_diff': compute_diff(df_old, df_new, 'c_wood'),
        'c_llm_new': np.round(df_new.c_llm, 2),
        'c_llm_old': np.round(df_old.c_llm, 2),
        'c_llm_diff': compute_diff(df_old, df_new, 'c_llm'),
        'c_ground_new': np.round(df_new.c_ground, 2),
        'c_ground_old': np.round(df_old.c_ground,2),
        'c_ground_diff': compute_diff(df_old, df_new, 'c_ground')
    })
    df.to_csv('merged_summary_columns.csv', index=False)
    
def compare_columns(df_old, df_new):
    df = pd.DataFrame()
    for col in [c for c in df_old.columns if 'filename'!=c and 'fuelbed'!=c]:
        c_old = df_old.get(col)
        c_new = df_new.get(col)
        perc_diff = np.where(((c_new > 1) & (c_old > 1)),
            (((c_new - c_old) / np.maximum(c_new, c_old))*100),
            0)
        df[col] = np.round(perc_diff.astype('float'), 1)
        df[col].fillna(0, inplace=True)
        print('{}:'.format(col))
        top_five = sorted(perc_diff, reverse=True)[:5]
        bottom_five = sorted(perc_diff, reverse=True)[-5:]
        for i in top_five:
            print('\t{:.3f}'.format(i))
        print('\t...')
        for i in bottom_five:
            print('\t{:.3f}'.format(i))
    
    df.to_csv('column_percent_diff.csv', index=False)

def process(old, new):
    df_old = pd.read_csv(old)
    df_new = pd.read_csv(new)
    df_old = rename_columns(df_old)
    compare_columns(df_old, df_new)
    write_merged(df_old, df_new)



# ++++++++++++++++++++++++++++++++++++++++++
#   Start
# ++++++++++++++++++++++++++++++++++++++++++
if __name__ == "__main__":
    if 3 == len(sys.argv):
        old = sys.argv[1]
        new = sys.argv[2]
        process(old, new)
    else:
        usage()