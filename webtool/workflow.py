"""
workflow.py
Core pipeline logic for the consume webtool.

Implements the two-run pipeline:
  Run 1: build loadings + input from base fccs_loadings → run consume → consume_output_run1
  Run 2: build adjusted loadings + input from run1 output → run consume → consume_output_run2
"""

import csv
import logging
import math
import os
import re
import sys
from pathlib import Path

# ── paths ───────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent.parent
DEFAULT_FCCS_LOADINGS = REPO_ROOT / 'consume' / 'input_data' / 'fccs_loadings.csv'
OUTPUT_ALL_CSV = REPO_ROOT / 'output_all.csv'

# Make consume_batch importable
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import consume_batch  # noqa: E402

# ── scenario definitions ────────────────────────────────────────────────────

# ── NATURAL burn type ────────────────────────────────────────────────────────
# Columns: area, fm_duff, fm_1000hr, can_con_pct, shrub_black_pct, pile_black_pct,
#          units, ecoregion, fm_litter, season,
#          rotten_cwd_pct_available, duff_pct_available, sound_cwd_pct_available
SCENARIO_NAMES = ['SpringRx', 'SpringRxRed', 'FallRx', 'FallRxRed', 'WFLow', 'WFMod', 'WFHigh']
SCENARIO_ROWS = [
    [100, 150, 80,  0,   50,  90, 'tons', 'western', 15, 'spring', 50,  30,   0],
    [100, 150, 80,  0,   50,  90, 'tons', 'western', 15, 'spring', 20,  10,   0],
    [100,  60, 25,  0,  100,  90, 'tons', 'western', 12, 'fall',  100, 100,  20],
    [100,  60, 35,  0,  100,  90, 'tons', 'western', 12, 'fall',   50,  50,   0],
    [100,  30, 35,  20, 100,  90, 'tons', 'western', 12, 'summer', 100, 100, 100],
    [100,  30, 25,  50, 100,  90, 'tons', 'western',  9, 'summer', 100, 100, 100],
    [100,  30, 10,  90, 100, 100, 'tons', 'western',  3, 'summer', 100, 100, 100],
]

INPUT_HEADER = [
    'area', 'fm_duff', 'fm_1000hr', 'can_con_pct', 'shrub_black_pct', 'pile_black_pct',
    'fuelbeds', 'units', 'ecoregion', 'fm_litter', 'season',
    'rotten_cwd_pct_available', 'duff_pct_available', 'sound_cwd_pct_available',
]

# ── ACTIVITY burn type ───────────────────────────────────────────────────────
# Columns: area, fm_duff, fm_1000hr, can_con_pct, shrub_black_pct, pile_black_pct,
#          units, ecoregion, slope, windspeed, days_since_rain, length_of_ignition,
#          fm_type, fm_litter, fm_10hr, season,
#          duff_pct_available, sound_cwd_pct_available, rotten_cwd_pct_available
ACTIVITY_SCENARIO_NAMES = ['ActivityDefault']
ACTIVITY_SCENARIO_ROWS = [
    [100, 30, 60, 20, 80, 90, 'tons', 'western', 5, 5, 4, 30, 'MEAS-Th', 10, 10, 'fall', 100, 100, 100],
]

ACTIVITY_INPUT_HEADER = [
    'area', 'fm_duff', 'fm_1000hr', 'can_con_pct', 'shrub_black_pct', 'pile_black_pct',
    'fuelbeds', 'units', 'ecoregion', 'slope', 'windspeed', 'days_since_rain',
    'length_of_ignition', 'fm_type', 'fm_litter', 'fm_10hr', 'season',
    'duff_pct_available', 'sound_cwd_pct_available', 'rotten_cwd_pct_available',
]

# ── column maps for run-2 adjusted loadings ──────────────────────────────────
# Columns of fccs_loadings that get adjusted (original - consumed).
# Index 33 (shrubs_primary_perc_live) has no consume counterpart — copied as-is.
FCCS_ADJUSTABLE_COLS = [
    'overstory_loading', 'midstory_loading', 'understory_loading',
    'snags_c1_foliage_loading', 'snags_c1wo_foliage_loading', 'snags_c1_wood_loading',
    'snags_c2_loading', 'snags_c3_loading', 'ladderfuels_loading',
    'shrubs_primary_loading', 'shrubs_secondary_loading',
    'nw_primary_loading', 'nw_secondary_loading',
    'pile_clean_loading',
    'w_sound_0_quarter_loading', 'w_sound_quarter_1_loading', 'w_sound_1_3_loading',
    'w_sound_3_9_loading', 'w_sound_9_20_loading', 'w_sound_gt20_loading',
    'w_rotten_3_9_loading', 'w_rotten_9_20_loading', 'w_rotten_gt20_loading',
    'w_stump_sound_loading', 'w_stump_rotten_loading', 'w_stump_lightered_loading',
    'litter_loading', 'lichen_loading', 'moss_loading',
    'duff_upper_loading', 'duff_lower_loading',
    'basal_accum_loading', 'squirrel_midden_loading',
    'shrubs_primary_perc_live',   # index 33 — no consume counterpart
]

# Parallel consume output columns for each adjustable fccs column (len = 33, matches indices 0-32).
CONSUME_COUNTERPARTS = [
    'c_overstory_crown', 'c_midstory_crown', 'c_understory_crown',
    'c_snagc1f_crown', 'c_snagc1f_wood', 'c_snagc1_wood', 'c_snagc2_wood', 'c_snagc3_wood',
    'c_ladder', 'c_shrub_1live', 'c_shrub_2live',
    'c_herb_1live', 'c_herb_2live', 'c_piles',
    'c_wood_1hr', 'c_wood_10hr', 'c_wood_100hr',
    'c_wood_s1000hr', 'c_wood_s10khr', 'c_wood_s+10khr',
    'c_wood_r1000hr', 'c_wood_r10khr', 'c_wood_r+10khr',
    'c_stump_sound', 'c_stump_rotten', 'c_stump_lightered',
    'c_litter', 'c_lichen', 'c_moss',
    'c_upperduff', 'c_lowerduff',
    'c_basal', 'c_squirrel',
    # index 33 intentionally absent
]

# Extra columns that are passed through from fccs_loadings unchanged,
# except entries in ZERO_OUT_EXTRAS which are set to '0'.
FCCS_EXTRA_COLS = [
    'shrubs_secondary_perc_live', 'nw_primary_perc_live', 'nw_secondary_perc_live',
    'litter_depth', 'lichen_depth', 'moss_depth',
    'duff_lower_depth', 'duff_upper_depth', 'ladderfuels_loading',
    'cover_type', 'ecoregion',
    'pile_dirty_loading', 'pile_vdirty_loading',
    'efg_natural', 'efg_activity',
]
ZERO_OUT_EXTRAS = {
    'litter_depth', 'lichen_depth', 'moss_depth', 'ladderfuels_loading',
    'duff_lower_depth', 'duff_upper_depth', 'pile_dirty_loading', 'pile_vdirty_loading',
}

# Full column list for run-2 loadings header (= adjustable + extras)
FULL_COL_MAP = FCCS_ADJUSTABLE_COLS + FCCS_EXTRA_COLS  # 49 total


# ── helpers ──────────────────────────────────────────────────────────────────

def safe_float(s):
    if s is None:
        return 0.0
    s = str(s).strip()
    if not s:
        return 0.0
    try:
        return float(s)
    except ValueError:
        try:
            return float(s.replace(',', '').rstrip('%'))
        except ValueError:
            return 0.0


def format_float(v):
    """Format adjusted float value for CSV output."""
    if math.isclose(v, round(v)):
        return str(int(round(v)))
    return f'{v:.6f}'.rstrip('0').rstrip('.')


def make_run1_fuelbed_id(fb_str, scenario_1based):
    """
    Encode a fccs fuelbed string + scenario index (1-7) into the run-1 loadings fuelbed_number.

    For base FCCS IDs (stored as-is in fccs_loadings, e.g. '1', '52'):
      fb_str='1'  → '1000001' … '1000007'
      fb_str='52' → '52000001' … '52000007'

    For disturbance variants (e.g. '10111', '520111', already appended to fbListWithVariations):
      int(fb_str) > 1297 → fb_str + '0' + str(scenario_1based)
      e.g. '10111' → '101110001' … '101110007' (NOT used for filtering)
    """
    if not fb_str.isdigit() or int(fb_str) <= 1297:
        return fb_str + '00000' + str(scenario_1based)
    return fb_str + '0' + str(scenario_1based)


def decode_run1_fuelbed(fuelbed_base):
    """
    Reverse-map a run-1 consume output fuelbed_number back to the base FCCS id string.

    Examples (from reference files):
      '1000001'  → '1'
      '52000001' → '52'
      '1011101'  → '1'     (FCCS 1, disturbance 111, scenario 1)
      '52011101' → '52'    (FCCS 52, disturbance 111, scenario 1)
    """
    consume_lookup = fuelbed_base[:-2]  # strip last 2 chars (scenario digit + one more)
    if consume_lookup.isdigit() and int(consume_lookup) < 10000:
        fccs_lookup = consume_lookup
    else:
        fccs_lookup = consume_lookup[:-4] if consume_lookup.endswith('0000') else consume_lookup

    plain_fuelbed_number = fccs_lookup
    if plain_fuelbed_number.isdigit() and int(plain_fuelbed_number) > 10000:
        plain_fuelbed_number = plain_fuelbed_number[:-4]

    return fccs_lookup, plain_fuelbed_number


# ── pipeline step 1: build run-1 files ──────────────────────────────────────

def build_run1_files(fuelbed_list, output_dir, fccs_loadings_path=None, progress=None,
                     scenario_names=None, scenario_rows=None, burn_type='natural',
                     include_disturbance=True):
    """
    Create loadings_run1.csv and input_run1.csv in output_dir.

    For each FCCS id in fuelbed_list the function generates the base row plus
    all 3×3×3 = 27 disturbance variations (codes 111–333), then writes N
    scenario copies of each found row (N = len(scenario_rows)).

    Returns (loadings_path, input_path).
    """
    if scenario_names is None:
        scenario_names = SCENARIO_NAMES if burn_type == 'natural' else ACTIVITY_SCENARIO_NAMES
    if scenario_rows is None:
        scenario_rows = SCENARIO_ROWS if burn_type == 'natural' else ACTIVITY_SCENARIO_ROWS
    input_header = INPUT_HEADER if burn_type == 'natural' else ACTIVITY_INPUT_HEADER
    if fccs_loadings_path is None:
        fccs_loadings_path = str(DEFAULT_FCCS_LOADINGS)
    if progress is None:
        progress = print

    loadings_out = os.path.join(output_dir, 'loadings_run1.csv')
    input_out    = os.path.join(output_dir, 'input_run1.csv')

    fb_strings = [str(f) for f in fuelbed_list]

    # Build variation list: base only, or base + 27 disturbance codes per fuelbed
    fb_list_with_variations = []
    for fb in fb_strings:
        fb_list_with_variations.append(fb)
        if include_disturbance:
            for i in range(1, 4):
                for j in range(1, 4):
                    for k in range(1, 4):
                        fb_list_with_variations.append(fb + '0' + str(i) + str(j) + str(k))

    progress(f'Building run 1 files for {len(fuelbed_list)} fuelbeds '
             f'({len(fb_list_with_variations)} entries{" including disturbance variations" if include_disturbance else ", reference fuelbeds only"}, '
             f'{len(scenario_rows)} scenarios)...')

    with open(fccs_loadings_path, 'r') as f:
        raw_lines = f.read().split('\n')

    header_line0 = raw_lines[0]   # GeneratorName=... row
    header_line1 = raw_lines[1]   # column-name row

    # Build a quick lookup dict from fuelbed_number → line string, for speed
    line_lookup = {}
    for line in raw_lines[2:]:
        if line.strip():
            key = line.split(',')[0]
            line_lookup[key] = line

    found_count = 0
    not_found = []

    with open(loadings_out, 'w', newline='') as lf, \
         open(input_out,    'w', newline='') as inf:

        lf.write(header_line0 + '\n')
        lf.write(header_line1 + '\n')
        inf.write(','.join(input_header) + '\n')

        for fb_num in fb_list_with_variations:
            if fb_num not in line_lookup:
                not_found.append(fb_num)
                continue

            line = line_lookup[fb_num]
            cols = line.split(',')
            found_count += 1

            for i, scen in enumerate(scenario_rows, 1):
                fuelbed_id = make_run1_fuelbed_id(fb_num, i)
                temp_cols    = cols[:]
                temp_cols[0] = fuelbed_id
                lf.write(','.join(temp_cols) + '\n')

                # Build input row: insert fuelbeds at position 6
                row  = list(scen[:6]) + [fuelbed_id] + list(scen[6:])
                inf.write(','.join(str(x) for x in row) + '\n')

    if not_found:
        base_not_found = [x for x in not_found if '_' not in x and len(x) <= 4]
        if base_not_found:
            progress(f'Warning: base fuelbeds not found in loadings: {base_not_found}')
        progress(f'  ({len(not_found)} total variation entries not found, '
                 f'{found_count} written)')
    else:
        progress(f'  {found_count} fuelbed variations written.')

    progress(f'Run 1 loadings: {loadings_out}')
    progress(f'Run 1 input:    {input_out}')
    return loadings_out, input_out


# ── pipeline step 2: run consume ─────────────────────────────────────────────

def run_consume(loadings_path, input_path, output_path, feps_path,
                burn_type='natural', do_metric=False, progress=None):
    """
    Run consume_batch.run() with the supplied files.
    Returns True on success.
    """
    if progress is None:
        progress = print

    col_cfg = str(OUTPUT_ALL_CSV)
    progress(f'Running consume...')
    progress(f'  loadings: {loadings_path}')
    progress(f'  input:    {input_path}')
    progress(f'  output:   {output_path}')
    progress(f'  units:    {"metric" if do_metric else "imperial"}')

    consume_batch.run(
        burn_type=burn_type,
        csv_input=input_path,
        do_metric=do_metric,
        msg_level=logging.ERROR,
        outfile=output_path,
        feps_input_filename=feps_path,
        fuel_loadings=loadings_path,
        col_cfg=col_cfg,
        no_sera=False,
    )

    if os.path.exists(output_path):
        with open(output_path) as f:
            row_count = sum(1 for _ in f) - 1
        progress(f'Consume complete: {row_count} output rows written.')
        return True
    else:
        progress(f'ERROR: consume did not produce output at {output_path}')
        return False


# ── pipeline step 3: build run-2 files ──────────────────────────────────────

def build_run2_files(fccs_loadings_path, consume_output_path, output_dir,
                     fuelbed_list=None, progress=None,
                     scenario_names=None, scenario_rows=None, burn_type='natural'):
    """
    Create loadings_run2.csv and input_run2.csv in output_dir, using
    run-1 consume output to compute adjusted (post-consumption) loadings.

    Each row in the run-1 output generates 7 scenario rows in run-2.
    Returns (loadings_path, input_path).
    """
    if fccs_loadings_path is None:
        fccs_loadings_path = str(DEFAULT_FCCS_LOADINGS)
    if progress is None:
        progress = print
    if scenario_names is None:
        scenario_names = SCENARIO_NAMES if burn_type == 'natural' else ACTIVITY_SCENARIO_NAMES
    if scenario_rows is None:
        scenario_rows = SCENARIO_ROWS if burn_type == 'natural' else ACTIVITY_SCENARIO_ROWS
    input_header = INPUT_HEADER if burn_type == 'natural' else ACTIVITY_INPUT_HEADER

    loadings_out = os.path.join(output_dir, 'loadings_run2.csv')
    input_out    = os.path.join(output_dir, 'input_run2.csv')

    filter_set = {str(f) for f in fuelbed_list} if fuelbed_list else None

    # Load fccs_loadings
    with open(fccs_loadings_path, 'r', newline='') as f:
        fccs_rows = list(csv.reader(f))
    fccs_col_names = fccs_rows[1]  # second row = column headers

    # Build lookup: fuelbed_number → row
    fccs_lookup_map = {}
    for row in fccs_rows[2:]:
        if row and row[0].strip():
            fccs_lookup_map[row[0]] = row

    # Load consume output
    with open(consume_output_path, 'r', newline='') as f:
        consume_rows = list(csv.reader(f))
    consume_header  = consume_rows[0]
    fuelbeds_col_idx = consume_header.index('fuelbeds')
    filename_col_idx = consume_header.index('filename')
    c_total_col_idx  = consume_header.index('c_total')

    progress(f'Building run 2 files from {len(consume_rows) - 1} run-1 output rows...')

    written = 0

    with open(loadings_out, 'w', newline='') as lf, \
         open(input_out,    'w', newline='') as inf:

        load_writer = csv.writer(lf)
        inp_writer  = csv.writer(inf)

        load_writer.writerow(
            ['GeneratorName=FCCS 4.0', 'GeneratorVersion=3.0.0', 'DateCreated=04/02/2026.'])
        load_writer.writerow(
            ['fuelbed_number', 'FCCSID', 'filename', 'Total_available_fuel_loading']
            + FULL_COL_MAP)
        inp_writer.writerow(input_header)

        for crow in consume_rows[1:]:
            if not crow or len(crow) <= fuelbeds_col_idx:
                continue

            fuelbed_base = crow[fuelbeds_col_idx]
            fccs_lookup, plain_fuelbed_number = decode_run1_fuelbed(fuelbed_base)

            # Optional filter
            if filter_set and plain_fuelbed_number not in filter_set:
                continue

            # Locate matching row in fccs_loadings
            fccs_row = fccs_lookup_map.get(fccs_lookup)
            if fccs_row is None:
                continue

            filename_value = crow[filename_col_idx] if filename_col_idx < len(crow) else ''

            # ── compute adjusted column values ──────────────────────────────
            column_values = []
            for idx_col, col_name in enumerate(FCCS_ADJUSTABLE_COLS):
                # Original value from fccs_loadings
                try:
                    fccs_col_idx = fccs_col_names.index(col_name)
                    original = safe_float(fccs_row[fccs_col_idx])
                except (ValueError, IndexError):
                    original = 0.0

                # Consumed value (no counterpart for index 33 → consumed_val = 0)
                consumed = 0.0
                if idx_col < len(CONSUME_COUNTERPARTS):
                    try:
                        c_idx = consume_header.index(CONSUME_COUNTERPARTS[idx_col])
                        consumed = safe_float(crow[c_idx])
                    except (ValueError, IndexError):
                        consumed = 0.0

                adjusted = max(original - consumed, 0.0)
                column_values.append(format_float(adjusted))

            # ── pass-through extra columns ───────────────────────────────────
            for name in FCCS_EXTRA_COLS:
                if name in ZERO_OUT_EXTRAS:
                    column_values.append('0')
                else:
                    try:
                        col_idx = fccs_col_names.index(name)
                        val = fccs_row[col_idx] if col_idx < len(fccs_row) else ''
                    except ValueError:
                        val = ''
                    column_values.append(val)

            # ── adjusted total fuel loading ──────────────────────────────────
            try:
                total_idx     = fccs_col_names.index('Total_available_fuel_loading')
                total_orig    = safe_float(fccs_row[total_idx])
            except (ValueError, IndexError):
                total_orig = 0.0
            c_total_val   = safe_float(crow[c_total_col_idx]) if c_total_col_idx < len(crow) else 0.0
            adjusted_total = max(total_orig - c_total_val, 0.0)
            total_value    = format_float(adjusted_total)

            # Build FCCSID display (e.g. '52_111' from '520111')
            fccs_display = re.sub(r'^(\d+?)0(\d{3})$', r'\1_\2', fccs_lookup)

            # ── write N scenario variants ─────────────────────────────────
            for jj, scen in enumerate(scenario_rows, 1):
                fuelbed_number = fuelbed_base + str(jj).zfill(2)
                load_writer.writerow(
                    [fuelbed_number, fccs_display, filename_value, total_value]
                    + column_values)
                written += 1

            # ── write N input rows ───────────────────────────────────────────
            base = fuelbed_base
            for jj, scen in enumerate(scenario_rows, 1):
                fuelbed_number = base + str(jj).zfill(2)
                row = list(scen[:6]) + [fuelbed_number] + list(scen[6:])
                inp_writer.writerow(row)

    progress(f'Run 2 loadings: {loadings_out} ({written} rows)')
    progress(f'Run 2 input:    {input_out}')
    return loadings_out, input_out


# ── full pipeline ─────────────────────────────────────────────────────────────

def run_pipeline(fuelbed_list, output_dir, fccs_loadings_path=None, progress=None,
                 scenario_names=None, scenario_rows=None, burn_type='natural',
                 include_disturbance=True, num_runs=2, do_metric=False):
    """
    Execute the full two-run pipeline and return paths to all output files.

    fuelbed_list   : list of integer FCCS fuelbed IDs
    output_dir     : directory where all intermediate and final files are written
    progress       : callable(message_str) for progress reporting
    scenario_names : list of scenario name strings (default depends on burn_type)
    scenario_rows  : list of scenario value lists (default depends on burn_type)
    burn_type      : 'natural' (default) or 'activity'

    Returns dict of output file paths.
    """
    if progress is None:
        progress = print
    if fccs_loadings_path is None:
        fccs_loadings_path = str(DEFAULT_FCCS_LOADINGS)

    os.makedirs(output_dir, exist_ok=True)

    import datetime
    log_path = os.path.join(output_dir, 'run_log.txt')
    log_lines = []

    def p(msg):
        progress(msg)
        log_lines.append(msg)

    def _write_log():
        with open(log_path, 'w') as _lf:
            _lf.write('\n'.join(log_lines) + '\n')

    log_lines.append(f'Consume pipeline log — {datetime.datetime.now().isoformat(timespec="seconds")}')
    log_lines.append(f'burn_type: {burn_type}')
    log_lines.append(f'do_metric: {do_metric}')
    log_lines.append(f'num_runs: {num_runs}')
    log_lines.append(f'include_disturbance: {include_disturbance}')
    log_lines.append(f'fuelbeds: {fuelbed_list}')
    log_lines.append('')

    # ── Run 1 ───────────────────────────────────────────────────────────────
    total = num_runs * 2
    p(f'=== Step 1/{total}: Building run-1 loadings and input files ===')
    loadings1, input1 = build_run1_files(
        fuelbed_list, output_dir, fccs_loadings_path, progress=p,
        scenario_names=scenario_names, scenario_rows=scenario_rows,
        burn_type=burn_type, include_disturbance=include_disturbance)

    p(f'=== Step 2/{total}: Running consume (run 1) ===')
    output1      = os.path.join(output_dir, 'consume_output_run1.csv')
    feps1        = os.path.join(output_dir, 'feps_run1.csv')
    ok = run_consume(loadings1, input1, output1, feps1, burn_type=burn_type, do_metric=do_metric, progress=p)
    if not ok:
        raise RuntimeError('Consume run 1 failed — no output file produced.')

    if num_runs == 1:
        p('=== Pipeline complete ===')
        _write_log()
        return {
            'loadings_run1':       loadings1,
            'input_run1':          input1,
            'consume_output_run1': output1,
            'run_log':             log_path,
        }

    # ── Run 2 ───────────────────────────────────────────────────────────────
    p(f'=== Step 3/{total}: Building run-2 adjusted loadings and input files ===')
    loadings2, input2 = build_run2_files(
        fccs_loadings_path, output1, output_dir,
        fuelbed_list=fuelbed_list, progress=p,
        scenario_names=scenario_names, scenario_rows=scenario_rows,
        burn_type=burn_type)

    p(f'=== Step 4/{total}: Running consume (run 2) ===')
    output2      = os.path.join(output_dir, 'consume_output_run2.csv')
    feps2        = os.path.join(output_dir, 'feps_run2.csv')
    ok = run_consume(loadings2, input2, output2, feps2, burn_type=burn_type, do_metric=do_metric, progress=p)
    if not ok:
        raise RuntimeError('Consume run 2 failed — no output file produced.')

    p('=== Pipeline complete ===')
    _write_log()

    return {
        'loadings_run1':        loadings1,
        'input_run1':           input1,
        'consume_output_run1':  output1,
        'loadings_run2':        loadings2,
        'input_run2':           input2,
        'consume_output_run2':  output2,
        'run_log':              log_path,
    }
