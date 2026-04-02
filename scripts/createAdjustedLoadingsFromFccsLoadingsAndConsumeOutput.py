# python
import csv
from pathlib import Path
import math

# input files
fccsLoadingsPath = '/Users/briandrye/Downloads/2026_04_02ConsumeScenario/fccs_loadings.csv'
consumeOutputPath = '/Users/briandrye/Downloads/2026_04_02ConsumeScenario/consume_output2026_01_30.csv'

# output files
newFccsLoadingsPath = '/Users/briandrye/Downloads/2026_04_02ConsumeScenario/adjusted_fccs_loadings2026_04_02.csv'
inputFilePath = '/Users/briandrye/Downloads/2026_04_02ConsumeScenario/input_file_for_adjusted2026_04_02.csv'

# file for comparison
referencePath = '/Users/briandrye/Downloads/2026_04_02ConsumeScenario/SPAdjustedFCCSLoadingsFormatted3.csv'
inputReferencePath = '/Users/briandrye/Downloads/2026_04_02ConsumeScenario/input_file_reference.csv'

# log of differences between our generated file and the reference file
diffLogPath = '/Users/briandrye/Downloads/2026_04_02ConsumeScenario/diff_log.txt'
diffInputLogPath = '/Users/briandrye/Downloads/2026_04_02ConsumeScenario/diff_input_log.txt'

# small helper: convert strings to float safely, treat blank/non-numeric as 0.0
def safe_float(s):
    if s is None:
        return 0.0
    s = str(s).strip()
    if s == '':
        return 0.0
    try:
        return float(s)
    except Exception:
        try:
            s2 = s.replace(',', '').rstrip('%')
            return float(s2)
        except Exception:
            return 0.0

# Read inputs
with open(fccsLoadingsPath, 'r', newline='') as f:
    fccsLoadings = list(csv.reader(f))
    fccsColumnNames = fccsLoadings[1]  # second row has column names

with open(consumeOutputPath, 'r', newline='') as f:
    consumeOutput = list(csv.reader(f))

# minimal column maps required for the adjusted columns (use your originals if different)
fccsColumnMap = ['overstory_loading', 'midstory_loading', 'understory_loading',
               'snags_c1_foliage_loading', 'snags_c1wo_foliage_loading', 'snags_c1_wood_loading',
               'snags_c2_loading', 'snags_c3_loading', 'ladderfuels_loading',
               'shrubs_primary_loading', 'shrubs_secondary_loading',
               'nw_primary_loading', 'nw_secondary_loading',
               'pile_clean_loading',
               'w_sound_0_quarter_loading', 'w_sound_quarter_1_loading',
               'w_sound_1_3_loading',
                'w_sound_3_9_loading',
               'w_sound_9_20_loading', 'w_sound_gt20_loading',
               'w_rotten_3_9_loading', 'w_rotten_9_20_loading',
               'w_rotten_gt20_loading',
               'w_stump_sound_loading', 'w_stump_rotten_loading', 'w_stump_lightered_loading',
               'litter_loading', 'lichen_loading', 'moss_loading',
               'duff_upper_loading', 'duff_lower_loading',
               'basal_accum_loading', 'squirrel_midden_loading']
fccsColumnMap.extend(['shrubs_primary_perc_live', 'shrubs_secondary_perc_live',
                    'nw_primary_perc_live', 'nw_secondary_perc_live',
                    'litter_depth', 'lichen_depth', 'moss_depth',
                    'duff_lower_depth', 'duff_upper_depth', 'ladderfuels_loading',
                    'cover_type', 'ecoregion',
                    'pile_clean_loading', 'pile_dirty_loading', 'pile_vdirty_loading',
                    'efg_natural', 'efg_activity'])

consumeColumnMap = ['c_overstory_crown', 'c_midstory_crown', 'c_understory_crown',
    'c_snagc1f_crown', 'c_snagc1f_wood', 'c_snagc1_wood', 'c_snagc2_wood', 'c_snagc3_wood',
    'c_ladder', 'c_shrub_1live', 'c_shrub_2live',
    'c_herb_1live', 'c_herb_2live', 'c_piles',
    'c_wood_1hr', 'c_wood_10hr', 'c_wood_100hr',
    'c_wood_s1000hr', 'c_wood_s10khr', 'c_wood_s+10khr',
    'c_wood_r1000hr','c_wood_r10khr',  'c_wood_r+10khr',
    'c_stump_sound', 'c_stump_rotten', 'c_stump_lightered',
    'c_litter', 'c_lichen', 'c_moss',
    'c_upperduff', 'c_lowerduff',
    'c_basal', 'c_squirrel']


# Uncomment the desired set of fuelbeds to process.
# Each base fuelbed will automatically include all disturbance variations.
#fuelbedsOfInterest = ['52']                         # single fuelbed
#fuelbedsOfInterest = ['52', '208', '292']           # small subset
#fuelbedsOfInterest = ['52', '70', '208', '57', '308']
fuelbedsOfInterest = ['1', '6', '8', '9', '10', '13', '20', '22', '28', '48', '52', '53', '56', '57', '59', '60', '70', '95', '208', '224', '235', '237', '292', '304', '305', '308', '310', '315', '321', '331', '358', '360', '361', '483', '493', '494', '496', '497', '498', '506', '514', '529', '530', '531', '532', '1223', '1232', '1262', '1264', '1273']

# We'll iterate over the fccs_loadings rows and generate adjusted rows. use output_limit to limit how many adjusted rows are written for testing (set to 0 for no limit)
output_limit = 0
written = 0

# Write input file header BEFORE the main loop
with open(inputFilePath, 'w', newline='') as inputFile:
    input_writer = csv.writer(inputFile)
    input_writer.writerow(
        ['area', 'fm_duff', 'fm_1000hr', 'can_con_pct', 'shrub_black_pct', 'pile_black_pct', 'fuelbeds', 'units',
         'ecoregion', 'fm_litter', 'season', 'rotten_cwd_pct_available', 'duff_pct_available',
         'sound_cwd_pct_available'])

with open(newFccsLoadingsPath, 'w', newline='') as newFile:
    writer = csv.writer(newFile)
    writer.writerow(['GeneratorName=FCCS 4.0', 'GeneratorVersion=3.0.0', 'DateCreated=04/02/2026.'])
    writer.writerow(['fuelbed_number'] + ['FCCSID'] + ['filename'] + ['Total_available_fuel_loading'] + fccsColumnMap)

    # get column indices from consumeOutput header row
    consume_header = consumeOutput[0]
    fuelbeds_col_idx = consume_header.index('fuelbeds')
    filename_col_idx = consume_header.index('filename')

    # iterate over consume output data rows (skip header)
    for crow in consumeOutput[1:]:
        if not crow or len(crow) <= fuelbeds_col_idx:
            continue

        fuelbed_base = crow[fuelbeds_col_idx]  # e.g. '1011101'

        # extract fccs_lookup: the base fuelbed id (first digits before disturbance suffix)
        # fuelbeds value like '10000' -> fccs_lookup = '1', or '10111' -> fccs_lookup = '1'
        # strip trailing zeros/variation codes to get the original FCCS id
        # The consume fuelbeds column stores the consume_lookup (e.g. '10000', '10111')
        # fccs_lookup is the prefix before the '0' + variation suffix
        # e.g. '10000' -> fccs_lookup='1', '20111' -> fccs_lookup='2'
        # find fccs_row matching fccs_lookup
        consume_lookup = fuelbed_base[:-2]          # '1011101' -> '10111', '52000001' -> '520000'
        # if the consume_lookup is less than 10000, don't strip any zeros. Example, 220 should remain 220, not become 22. But if it's greater than 10000, then strip the trailing zeros. Example, 1011101 should become 10111, and 52000001 should become 52.
        # if the last 4 digits are zeros, then strip the zeros
        # only strip last 4 zeros, 200000 -> 20, 2200000 -> 220.
        if consume_lookup.isdigit() and int(consume_lookup) < 10000:
            fccs_lookup = consume_lookup
        else:
                fccs_lookup = consume_lookup[:-4] if consume_lookup.endswith('0000') else consume_lookup

        # if fccs_lookup is greater than 10000, then remove the last 4 digits to get the plain_fuelbed_number (e.g. '10111' -> '1', '520000' -> '52')
        plain_fuelbed_number = fccs_lookup
        if plain_fuelbed_number.isdigit() and int(plain_fuelbed_number) > 10000:
            plain_fuelbed_number = plain_fuelbed_number[:-4]

        # skip rows not in fuelbedsOfInterest
        if plain_fuelbed_number not in fuelbedsOfInterest:
            continue

        fccs_row = None
        fccs_row_index = None
        for row in fccsLoadings[2:]:
            if row and row[0] == fccs_lookup:
                fccs_row = row
                fccs_row_index = fccsLoadings.index(row)
                break
        if fccs_row is None:
            continue

        # recompute columnValues for this consume row
        consumeOutputRowIndex = consumeOutput.index(crow)
        columnValues = []
        for idx_col, col_name in enumerate(fccsColumnMap[:-15]):
            try:
                fccs_col_index = fccsColumnNames.index(col_name)
            except ValueError:
                original_value = 0.0
            else:
                original_value = safe_float(fccs_row[fccs_col_index])
            try:
                consume_col_index = consume_header.index(consumeColumnMap[idx_col])
                consumed_value = safe_float(crow[consume_col_index])
            except Exception:
                consumed_value = 0.0
            adjusted_value = max(original_value - consumed_value, 0.0)
            # if(col_name == 'overstory_loading'):
            #     print(f'FCCS Row {fccs_row_index}, fccs_lookup {fccs_lookup}, Consume Row {consumeOutputRowIndex}, Consume fb {fuelbed_base}: col {col_name}, original {original_value}, consumed {consumed_value}, adjusted {adjusted_value}')

            columnValues.append(
                f'{adjusted_value:.6f}'.rstrip('0').rstrip('.')
                if not math.isclose(adjusted_value, round(adjusted_value))
                else str(int(round(adjusted_value)))
            )

        extras = []
        for name in fccsColumnMap[-15:]:
            col_idx = fccsColumnNames.index(name)
            val = fccs_row[col_idx] if col_idx < len(fccs_row) else ''
            if name in ['litter_depth', 'lichen_depth', 'moss_depth', 'ladderfuels_loading',
                        'duff_lower_depth', 'duff_upper_depth',
                        'pile_clean_loading', 'pile_dirty_loading', 'pile_vdirty_loading']:
                val = ''
            extras.append(val)
        columnValues.extend(extras)

        # look up Total_available_fuel_loading from fccs_row and subtract c_total from consume
        try:
            total_fuel_col_idx_fccs = fccsColumnNames.index('Total_available_fuel_loading')
            total_fuel_original = safe_float(
                fccs_row[total_fuel_col_idx_fccs] if total_fuel_col_idx_fccs < len(fccs_row) else '')
        except ValueError:
            total_fuel_original = 0.0

        try:
            c_total_col_idx = consume_header.index('c_total')
            c_total_value = safe_float(crow[c_total_col_idx] if c_total_col_idx < len(crow) else '')
        except ValueError:
            c_total_value = 0.0

        adjusted_total = max(total_fuel_original - c_total_value, 0.0)
        total_fuel_value = (
            f'{adjusted_total:.6f}'.rstrip('0').rstrip('.')
            if not math.isclose(adjusted_total, round(adjusted_total))
            else str(int(round(adjusted_total)))
        )

        # write 7 scenario2 variations by appending 01-07 to fuelbed_base
        for jj in range(1, 8):
            fuelbed_number = fuelbed_base + str(jj).zfill(2)
            filename_value = crow[filename_col_idx] if filename_col_idx < len(crow) else ''

            import re

            # Replace '10111' -> '1_111', '1220111' -> '122_111', etc.
            # Pattern: base digits, then '0', then 3-digit disturbance code
            fccs_display = re.sub(r'^(\d+?)0(\d{3})$', r'\1_\2', fccs_lookup)

            writer.writerow([fuelbed_number, fccs_display, filename_value, total_fuel_value] + columnValues)
            written += 1

        # write 7 scenario2 rows for this fuelbed_number to input file
        # write 7 scenario rows for this fuelbed_number to input file (no jj loop)
        with open(inputFilePath, 'a', newline='') as inputFile:
            input_writer = csv.writer(inputFile)
            input_writer.writerow([100, 150, 80, 0, 50, 90, fuelbed_base + '01', 'tons', 'western', 15, 'spring', 50, 30, 0])
            input_writer.writerow([100, 150, 80, 0, 50, 90, fuelbed_base + '02', 'tons', 'western', 15, 'spring', 20, 10, 0])
            input_writer.writerow([100, 60, 25, 0, 100, 90, fuelbed_base + '03', 'tons', 'western', 12, 'fall', 100, 100, 20])
            input_writer.writerow([100, 60, 35, 0, 100, 90, fuelbed_base + '04', 'tons', 'western', 12, 'fall', 50, 50, 0])
            input_writer.writerow([100, 30, 35, 20, 100, 90, fuelbed_base + '05', 'tons', 'western', 12, 'summer', 100, 100, 100])
            input_writer.writerow([100, 30, 25, 50, 100, 90, fuelbed_base + '06', 'tons', 'western', 9, 'summer', 100, 100, 100])
            input_writer.writerow([100, 30, 10, 90, 100, 100, fuelbed_base + '07', 'tons', 'western', 3, 'summer', 100, 100, 100])


        if output_limit > 0 and written >= output_limit:
            break

print(f'Wrote {written} rows to {newFccsLoadingsPath}')

# Now compare the first 10 data rows (skip header rows) with the reference file
def _extract_header_and_skip(rows):
    """
    Return (header_row_list, skip_count) where skip_count is number of rows
    to skip before data (1 normally, 2 if a generator metadata row is present).
    """
    if not rows:
        return [], 0
    first = rows[0]
    if any(isinstance(c, str) and c.startswith('GeneratorName') for c in first):
        if len(rows) > 1:
            return rows[1], 2
        return [], 1
    return rows[0], 1

def compare_first_n_by_name(a_path, b_path, log_path, n=10):
    with open(a_path, 'r', newline='') as fa, open(b_path, 'r', newline='') as fb:
        ra = list(csv.reader(fa))
        rb = list(csv.reader(fb))

    header_a, skip_a = _extract_header_and_skip(ra)
    header_b, skip_b = _extract_header_and_skip(rb)

    idx_a = {name: i for i, name in enumerate(header_a)} if header_a else {}
    idx_b = {name: i for i, name in enumerate(header_b)} if header_b else {}

    col_order = list(header_b) if header_b else []
    for name in header_a:
        if name not in idx_b:
            col_order.append(name)

    da = ra[skip_a:] if len(ra) > skip_a else []
    db = rb[skip_b:] if len(rb) > skip_b else []

    rows_to_check = min(n, len(da), len(db))
    diffs = []

    with open(log_path, 'w') as log:
        log.write(f'Comparing {a_path}\n    vs {b_path}\n')
        log.write(f'Checking {rows_to_check} rows (a has {len(da)}, b has {len(db)})\n\n')

        for row_i in range(rows_to_check):
            row_a = da[row_i]
            row_b = db[row_i]
            row_diffs = []
            for col_name in col_order:
                va = row_a[idx_a[col_name]] if (col_name in idx_a and idx_a[col_name] < len(row_a)) else ''
                vb = row_b[idx_b[col_name]] if (col_name in idx_b and idx_b[col_name] < len(row_b)) else ''

                # Normalize both to a canonical float string to avoid scientific notation mismatches
                def normalize_val(v):
                    if v == '':
                        return v
                    try:
                        f = float(v)
                        # Use repr-style formatting: avoid scientific notation for small numbers
                        formatted = f'{f:.10g}'
                        return formatted
                    except Exception:
                        return v

                va_norm = normalize_val(va)
                vb_norm = normalize_val(vb)

                if va_norm != vb_norm:
                    reason = 'values differ'
                    try:
                        is_blank_a = (va == '')
                        is_blank_b = (vb == '')
                        if (is_blank_a and not is_blank_b) or (is_blank_b and not is_blank_a):
                            reason = 'blank vs numeric (blank likely treated as 0.0)'
                        else:
                            fa_val = None if va == '' else float(va)
                            fb_val = None if vb == '' else float(vb)
                            if fa_val is not None and fb_val is not None:
                                diff = abs(fa_val - fb_val)
                                if diff < 1e-6:
                                    reason = 'formatting difference (same numeric)'
                                else:
                                    reason = f'numeric difference (delta={diff:.6f})'
                    except Exception:
                        reason = 'string formatting difference'
                    row_diffs.append((col_name, va, vb, reason))

            if row_diffs:
                log.write(f'--- Row {row_i+1} (adjusted row {row_i+skip_a+1}, reference row {row_i+skip_b+1}) ---\n')
                for (col_name, va, vb, reason) in row_diffs:
                    log.write(f'  {col_name}: ours={va!r}  ref={vb!r}  [{reason}]\n')
                diffs.extend([(row_i+1, col_name, va, vb, reason) for (col_name, va, vb, reason) in row_diffs])

        log.write(f'\nTotal differences: {len(diffs)}\n')
        if not diffs:
            log.write('No differences found.\n')

    print(f'Diff log written to {log_path} — {len(diffs)} differences found.')

compare_first_n_by_name(newFccsLoadingsPath, referencePath, diffLogPath, n=50960)
compare_first_n_by_name(inputFilePath, inputReferencePath, diffInputLogPath, n=50960)

print('Created adjusted loadings and input files based on consumption data.')

print('Run Consume against these new files to generate emissions estimates:')
print(
    'Example: (my310env) bdxfer@SEFS-A-DRYE consume813 % python consume_batch.py -f ~/Downloads/2026_04_02ConsumeScenario/adjusted_fccs_loadings2026_04_02.csv -o ~/Downloads/2026_04_02ConsumeScenario/consume_output_after_second_run2026_04_02.csv natural ~/Downloads/2026_04_02ConsumeScenario/input_file_for_adjusted2026_04_02.csv')


