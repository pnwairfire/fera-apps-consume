"""
app.py  —  Flask web application for the consume webtool.

Routes:
  GET  /                    → main UI
  POST /run                 → start pipeline job, returns {job_id}
  GET  /stream/<job_id>     → Server-Sent Events progress stream
  GET  /download/<job_id>/<filename>  → download a result file
  GET  /status/<job_id>     → JSON job status (for polling fallback)
"""

import os
import sys
import tempfile
import threading
import traceback
import uuid
from pathlib import Path

from flask import Flask, Response, jsonify, render_template, request, send_file

# Allow importing workflow from same directory
sys.path.insert(0, str(Path(__file__).parent))
import workflow  # noqa: E402

app = Flask(__name__)

# ── in-memory job store ──────────────────────────────────────────────────────
# jobs[job_id] = {
#   'status':   'running' | 'done' | 'error',
#   'messages': [str, ...],    # append-only log
#   'files':    {name: abs_path},
#   'error':    str | None,
#   'output_dir': str,
# }
jobs: dict = {}
jobs_lock = threading.Lock()


def _record(job_id, msg):
    with jobs_lock:
        jobs[job_id]['messages'].append(msg)


def _run_job(job_id, fuelbed_list, fccs_loadings_path, scenario_names, scenario_rows):
    output_dir = jobs[job_id]['output_dir']
    try:
        def progress(msg):
            _record(job_id, msg)

        files = workflow.run_pipeline(
            fuelbed_list,
            output_dir,
            fccs_loadings_path=fccs_loadings_path or None,
            progress=progress,
            scenario_names=scenario_names,
            scenario_rows=scenario_rows,
        )

        with jobs_lock:
            jobs[job_id]['files']  = {os.path.basename(p): p for p in files.values()}
            jobs[job_id]['status'] = 'done'
        _record(job_id, '__DONE__')

    except Exception as exc:
        tb = traceback.format_exc()
        with jobs_lock:
            jobs[job_id]['status'] = 'error'
            jobs[job_id]['error']  = str(exc)
        _record(job_id, f'ERROR: {exc}')
        _record(job_id, tb)
        _record(job_id, '__DONE__')


# ── routes ───────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/run', methods=['POST'])
def start_run():
    try:
        return _start_run_inner()
    except Exception:
        import traceback as _tb
        err = _tb.format_exc()
        print(err, flush=True)
        return jsonify({'error': err}), 500


def _start_run_inner():
    data = request.get_json(force=True)

    # Parse fuelbed list
    raw = data.get('fuelbeds', '')
    if isinstance(raw, list):
        parts = [str(x).strip() for x in raw]
    else:
        import re
        parts = re.split(r'[\s,;]+', str(raw).strip())
    parts = [p for p in parts if p]

    fuelbed_list = []
    bad = []
    for p in parts:
        try:
            fuelbed_list.append(int(p))
        except ValueError:
            bad.append(p)

    if bad:
        return jsonify({'error': f'Non-integer fuelbed IDs: {bad}'}), 400
    if not fuelbed_list:
        return jsonify({'error': 'No fuelbed IDs provided.'}), 400

    fccs_loadings_path = (data.get('fccs_loadings_path') or '').strip() or None

    # Validate custom loadings path if provided
    if fccs_loadings_path and not os.path.isfile(fccs_loadings_path):
        return jsonify({'error': f'Loadings file not found: {fccs_loadings_path}'}), 400

    # Parse optional scenarios
    _SCEN_FIELDS = [
        'area', 'fm_duff', 'fm_1000hr', 'can_con_pct', 'shrub_black_pct', 'pile_black_pct',
        'units', 'ecoregion', 'fm_litter', 'season',
        'rotten_cwd_pct_available', 'duff_pct_available', 'sound_cwd_pct_available',
    ]
    scenarios_raw = data.get('scenarios')
    if scenarios_raw and isinstance(scenarios_raw, list) and len(scenarios_raw) > 0:
        scenario_names = [str(s.get('name', f'Scenario{i+1}')) for i, s in enumerate(scenarios_raw)]
        scenario_rows  = [
            [s.get(f, '') for f in _SCEN_FIELDS]
            for s in scenarios_raw
        ]
    else:
        scenario_names = None
        scenario_rows  = None

    # Create temp output directory
    output_dir = tempfile.mkdtemp(prefix='consume_webtool_')

    job_id = str(uuid.uuid4())
    with jobs_lock:
        jobs[job_id] = {
            'status':     'running',
            'messages':   [],
            'files':      {},
            'error':      None,
            'output_dir': output_dir,
        }

    thread = threading.Thread(
        target=_run_job, args=(job_id, fuelbed_list, fccs_loadings_path, scenario_names, scenario_rows),
        daemon=True)
    thread.start()

    return jsonify({'job_id': job_id})


@app.route('/stream/<job_id>')
def stream(job_id):
    """Server-Sent Events stream of job progress messages."""
    if job_id not in jobs:
        return Response('data: Job not found\n\n', mimetype='text/event-stream')

    def generate():
        last_idx = 0
        while True:
            with jobs_lock:
                msgs   = jobs[job_id]['messages']
                status = jobs[job_id]['status']
                new    = msgs[last_idx:]
                last_idx = len(msgs)

            for msg in new:
                # Escape newlines inside a single SSE data field
                safe = msg.replace('\n', '\ndata: ')
                yield f'data: {safe}\n\n'

            if status in ('done', 'error') and last_idx >= len(msgs):
                yield 'event: end\ndata: done\n\n'
                break

            import time
            time.sleep(0.4)

    return Response(generate(), mimetype='text/event-stream',
                    headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})


@app.route('/status/<job_id>')
def status(job_id):
    if job_id not in jobs:
        return jsonify({'error': 'Unknown job'}), 404
    with jobs_lock:
        j = jobs[job_id]
        return jsonify({
            'status':   j['status'],
            'messages': j['messages'],
            'files':    list(j['files'].keys()),
            'error':    j['error'],
        })


@app.route('/download/<job_id>/<filename>')
def download(job_id, filename):
    if job_id not in jobs:
        return jsonify({'error': 'Unknown job'}), 404
    with jobs_lock:
        files = jobs[job_id]['files']
    if filename not in files:
        return jsonify({'error': f'File not available: {filename}'}), 404
    path = files[filename]
    if not os.path.isfile(path):
        return jsonify({'error': 'File no longer on disk'}), 404
    return send_file(path, as_attachment=True, download_name=filename)


@app.route('/download-zip/<job_id>')
def download_zip(job_id):
    if job_id not in jobs:
        return jsonify({'error': 'Unknown job'}), 404
    with jobs_lock:
        files = dict(jobs[job_id]['files'])
    if not files:
        return jsonify({'error': 'No files available'}), 404

    import io
    import zipfile
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        for fname, path in files.items():
            if os.path.isfile(path):
                zf.write(path, fname)
    buf.seek(0)
    return send_file(buf, mimetype='application/zip',
                     as_attachment=True, download_name='consume_results.zip')


# ── entry point ──────────────────────────────────────────────────────────────

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    print(f'Starting consume webtool on http://localhost:{port}')
    app.run(debug=False, port=port, threaded=True)
