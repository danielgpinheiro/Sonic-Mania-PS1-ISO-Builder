#!/usr/bin/env python3
"""Sonic Mania PS1 ISO Builder: your Sonic Mania Plus Data.rsdk -> a PlayStation disc image.

    python3 build_iso.py --data /path/to/Data.rsdk [--plus-characters] [--license licensea.dat] [--out output]

1. checks the tools (Python packages, psxavenc, ffmpeg / ffprobe, mkpsxiso, cmake and a C++20 compiler);
2. checks that Data.rsdk is the known Sonic Mania Plus release (SHA-256), unless --force;
3. builds the mesh optimiser (builder/tools/mesh/optimizer) once;
4. converts the game's assets for the PlayStation (builder/tools/build_assets.py): sprites, tiles, sound effects, music
   (CD-XA), videos (STR), 3D meshes; lays the files out in the order the game loads them and builds the disc around
   the prebuilt executable and code overlays (bin/) with mkpsxiso;
5. verifies the image byte by byte (EDC/ECC, license sectors, file index, every file);
6. writes output/SonicMania-PS1.bin + .cue + SHA256SUMS.

--plus-characters puts Mighty and Ray in the save select (the disc carries Data/PS1Config.txt). Off by default.
No game data is included in this repository: use your own copy of the game (see README.md).
"""
import argparse, hashlib, os, shutil, subprocess, sys, time

ROOT = os.path.dirname(os.path.abspath(__file__))
BUILDER = os.path.join(ROOT, 'builder')
TOOLS = os.path.join(BUILDER, 'tools')
EXE = os.path.join(ROOT, 'bin', 'SonicMania-PS1.exe')
OVL = os.path.join(ROOT, 'bin', 'ovl')
# Sonic Mania Plus (the Steam release's Data.rsdk, 208 MB)
DATA_SHA256 = '77a904387581978222a78d2b7d6cd5944f9537cd72db0d6588577e99b683090c'


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def need(prog, env, hint):
    p = os.environ.get(env) or shutil.which(prog)
    if not p:
        sys.exit('%s not found (on PATH or %s=): %s' % (prog, env, hint))
    return p


def check_tools():
    try:
        import numpy, PIL  # noqa: F401
    except ImportError:
        sys.exit('Python packages missing: pip install -r requirements.txt')
    env = dict(os.environ)
    env['PSXAVENC'] = need('psxavenc', 'PSXAVENC', 'https://github.com/WonderfulToolchain/psxavenc')
    env['FFMPEG'] = need('ffmpeg', 'FFMPEG', 'https://ffmpeg.org (with Theora / Vorbis)')
    env['FFPROBE'] = need('ffprobe', 'FFPROBE', 'part of ffmpeg')
    env['MKPSXISO'] = need('mkpsxiso', 'MKPSXISO', 'https://github.com/Lameguy64/mkpsxiso')
    need('cmake', 'CMAKE', 'https://cmake.org (builds the mesh optimiser)')
    return env


def build_optimizer(work, env):
    exe = os.path.join(work, 'optimizer', 'mania-mesh-optimizer')
    if not os.path.exists(exe):
        src = os.path.join(TOOLS, 'mesh', 'optimizer')
        subprocess.run(['cmake', '-S', src, '-B', os.path.join(work, 'optimizer'), '-DCMAKE_BUILD_TYPE=Release'],
                       check=True, stdout=subprocess.DEVNULL)
        subprocess.run(['cmake', '--build', os.path.join(work, 'optimizer'), '--config', 'Release'], check=True,
                       stdout=subprocess.DEVNULL)
        if not os.path.exists(exe):  # multi-config generators
            alt = os.path.join(work, 'optimizer', 'Release', 'mania-mesh-optimizer')
            exe = alt if os.path.exists(alt) else exe
    env['DC_MESH_OPT'] = exe


def main():
    ap = argparse.ArgumentParser(description='Build a Sonic Mania PlayStation disc image from your own Data.rsdk.')
    ap.add_argument('--data', required=True, help='Data.rsdk from your copy of Sonic Mania Plus')
    ap.add_argument('--plus-characters', action='store_true', help='Mighty and Ray in the save select (off by default)')
    ap.add_argument('--license', help='optional Sony license file (e.g. licensea.dat, NTSC-U) for retail consoles')
    ap.add_argument('--out', default=os.path.join(ROOT, 'output'), help='output folder (default: output/)')
    ap.add_argument('--force', action='store_true', help='accept a Data.rsdk that is not the known release')
    ap.add_argument('--keep-work', action='store_true', help='keep the intermediate files (output/work)')
    a = ap.parse_args()

    if sys.version_info < (3, 8):
        sys.exit('Python 3.8 or newer is required.')
    if not os.path.isfile(a.data):
        sys.exit('Data.rsdk not found: %s' % a.data)
    if a.license and not os.path.isfile(a.license):
        sys.exit('License file not found: %s' % a.license)
    env = check_tools()
    got = sha256(a.data)
    if got != DATA_SHA256:
        msg = 'Data.rsdk is not the known Sonic Mania Plus release (SHA-256 %s).' % got
        if not a.force:
            sys.exit(msg + '\nUse the unmodified file from your copy of the game, or pass --force to try anyway.')
        print('WARNING: ' + msg + ' Continuing because of --force.')

    out = os.path.abspath(a.out)
    work = os.path.join(out, 'work')
    os.makedirs(work, exist_ok=True)
    t0 = time.time()
    build_optimizer(work, env)
    prefix = os.path.join(out, 'SonicMania-PS1')
    lic = os.path.abspath(a.license) if a.license else 'none'
    cmd = [sys.executable, os.path.join(TOOLS, 'build_assets.py'), '--rsdk', os.path.abspath(a.data), '--exe', EXE,
           '--ovl', OVL, '--work', work, '--out', prefix, '--license', lic]
    if a.plus_characters:
        cmd.append('--plus')
    subprocess.run(cmd, check=True, env=env)
    with open(os.path.join(out, 'SHA256SUMS'), 'w') as f:
        for n in ('SonicMania-PS1.bin', 'SonicMania-PS1.cue'):
            f.write('%s  %s\n' % (sha256(os.path.join(out, n)), n))
    if not a.keep_work:
        shutil.rmtree(work, ignore_errors=True)
    print('\nDone in %d min: %s.cue / .bin%s' % ((time.time() - t0 + 59) // 60, prefix, '' if a.license else
                                                   '\n(no license file: plays in emulators, on ODEs and modded consoles)'))


if __name__ == '__main__':
    main()
