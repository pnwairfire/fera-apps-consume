import sys, os, tempfile, csv, subprocess

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'webtool'))
import workflow

SCRATCH = '/Users/briandrye/Downloads/2026_04_06Scratch'
FCCS    = SCRATCH + '/fccs_loadings.csv'
REF_L1  = SCRATCH + '/loadings_for_run_1.csv'
REF_I1  = SCRATCH + '/input_file_for_run_1.csv'
REF_L2  = SCRATCH + '/loadings_for_run_2.csv'
REF_CO1 = SCRATCH + '/consume_output_run_1.csv'

fuelbed_list = [
    1, 6, 8, 9, 10, 13, 20, 22, 28, 48, 52, 53, 56, 57, 59, 60, 70, 95,
    208, 224, 235, 237, 292, 304, 305, 308, 310, 315, 321, 331, 358, 360, 361,
    483, 493, 494, 496, 497, 498, 506, 514, 529, 530, 531, 532,
    1223, 1232, 1262, 1264, 1273
]

out_dir = tempfile.mkdtemp(prefix='cw_test_')
print('Output dir:', out_dir)

def p(m): print(m)

# ── Test run-1 build ─────────────────────────────────────────────────────────
print('\n--- Testing build_run1_files ---')
l1, i1 = workflow.build_run1_files(fuelbed_list, out_dir, FCCS, progress=p)

def rowcount(path):
    return int(subprocess.check_output(['wc', '-l', path]).decode().split()[0])

r1_ours = rowcount(l1)
r1_ref  = rowcount(REF_L1)
print(f'Run1 loadings rows: ours={r1_ours}  ref={r1_ref}  match={r1_ours == r1_ref}')

ri1_ours = rowcount(i1)
ri1_ref  = rowcount(REF_I1)
print(f'Run1 input rows:    ours={ri1_ours}  ref={ri1_ref}  match={ri1_ours == ri1_ref}')

with open(l1) as f:  our_rows = {r[0]: r for r in csv.reader(f) if r}
with open(REF_L1) as f: ref_rows = {r[0]: r for r in csv.reader(f) if r}

all_ok = True
for fb in ['1000001', '52000001', '52011101', '1011101']:
    if fb in our_rows and fb in ref_rows:
        match = our_rows[fb][:10] == ref_rows[fb][:10]
        if not match:
            print(f'  MISMATCH row {fb}')
            print(f'    ours: {our_rows[fb][:10]}')
            print(f'    ref:  {ref_rows[fb][:10]}')
            all_ok = False
        else:
            print(f'  row {fb}: OK')
    else:
        print(f'  row {fb}: missing ours={fb in our_rows} ref={fb in ref_rows}')

# ── Test run-2 build (uses reference run-1 consume output) ───────────────────
print('\n--- Testing build_run2_files ---')
l2, i2 = workflow.build_run2_files(FCCS, REF_CO1, out_dir,
                                    fuelbed_list=fuelbed_list, progress=p)

r2_ours = rowcount(l2)
r2_ref  = rowcount(REF_L2)
print(f'Run2 loadings rows: ours={r2_ours}  ref={r2_ref}  match={r2_ours == r2_ref}')

with open(l2) as f:  our2 = {r[0]: r for r in csv.reader(f) if r}
with open(REF_L2) as f: ref2 = {r[0]: r for r in csv.reader(f) if r}

for fb in ['5200000101', '5201110101', '100000101', '101110101']:
    if fb in our2 and fb in ref2:
        match = our2[fb][:8] == ref2[fb][:8]
        if not match:
            print(f'  MISMATCH row {fb}')
            print(f'    ours: {our2[fb][:8]}')
            print(f'    ref:  {ref2[fb][:8]}')
        else:
            print(f'  row {fb}: OK')
    else:
        print(f'  row {fb}: missing ours={fb in our2} ref={fb in ref2}')

print('\nTest complete.')
