# Sonic Mania PS1 ISO Builder

Build a PlayStation 1 disc image of **Sonic Mania** (running on the Retro Engine v5) from your own copy of
**Sonic Mania Plus**. The PS1 executable and its code overlays are prebuilt; this repository contains the tools that
convert the game's data for the PlayStation and put the disc together.

**No game data is included.** You need your own copy of the game's `Data.rsdk`, see [Usage](#usage).

## What does this do / why is it needed?

The PlayStation has 2 MB of RAM, 1 MB of video RAM, 512 KB of sound RAM, no floating point and a 2× CD-ROM drive.
Sonic Mania on PC decodes GIFs, Ogg music and Theora video while it runs and keeps far more in memory than a PS1 has.
So everything is converted **once, on your computer**, into formats the PS1 hardware uses directly:

- **Sprites** → one texture atlas per scene and per character (4/8-bit VRAM pages + palettes), checked pixel-exact
  against the source. Where a scene's sprites don't all fit the PS1's video RAM, some big ones are stored at half
  resolution (bosses last, and a boss shares the video RAM of level art its fight never shows).
- **Tiles** → pre-packed VRAM tile images with their palettes, the layouts compacted.
- **Sound effects** → SPU-ADPCM, one rate per file so every scene's set fits the sound RAM.
- **Music** → CD-XA audio, streamed and decoded by the CD drive, with the game's loop points.
- **Videos** → STR (MDEC) with their music, for the intro and the endings.
- **3D** → the special stages' meshes simplified for the PS1's geometry engine (GTE).
- **Disc layout** → files placed in the order the game loads them, shared files copied next to each stage, a file
  index so opening a file needs no directory reads.

## Usage

1. Copy `Data.rsdk` from your own installation of **Sonic Mania Plus** (Steam; unmodified, the builder checks its
   SHA-256).
2. Install the [requirements](#requirements).
3. Run:
   ```bash
   python3 build_iso.py --data /path/to/Data.rsdk
   ```
   Options:
   - `--plus-characters`: **Mighty and Ray** in the save select (off by default, see [Plus characters](#plus-characters));
   - `--license licensea.dat` (see [The license file](#the-license-file)), `--out folder`, `--keep-work`,
     `--force` (accept a `Data.rsdk` that isn't the known release).
4. The disc image is in `output/` after about three hours on a recent Mac (the sprite, music and video conversion is
   most of it).

## Output

- `output/SonicMania-PS1.cue` + `output/SonicMania-PS1.bin`: a Mode 2 BIN/CUE image (about 545 MB of 2352-byte
  sectors, 50 minutes; a CD-R's "650 / 700 MB" counts 2048 bytes a sector). It has to be BIN/CUE, not `.iso`: the
  CD-XA music and the videos use 2336-byte Mode 2 sectors, which a 2048-byte ISO image can't hold.
- `output/SHA256SUMS`.

Built from the known `Data.rsdk` **without** a license file and with the tool versions listed under
[Requirements](#requirements) (checked with FFmpeg 9.0.2 and psxavenc v0.3.1-3-gf6757f8), the image is
`SonicMania-PS1.bin` SHA-256 `60d60eb077dcefb8ce59df291f2b769257f0ce06e8648b25e9f631ba7195a830`. Other versions of FFmpeg or psxavenc
may encode the audio slightly differently, which changes the hash but not the game. With a license file the license
sectors differ, so the hash does too.

Before writing it, the builder verifies the image byte by byte: sector headers, EDC/ECC of every sector, the license
sectors, the file index, and every file against its source.

## What's new

Every update is listed in [CHANGELOG.md](CHANGELOG.md). Latest (November 2026): **back to the version before the
loading-icon work** — the previous update froze on Chemical Plant 1's loading screen, and this image is the build that
played the act, its boss, the act clear and the next act without a stall; title screen `v 60ef20a5`. The loading icon
therefore does not show while a boss's or Super Sonic's sprite set is read, as before that work. Before that: the
loading icon back where those loads were missing, and strict memory bookkeeping for the route "finish an act, leave to
the main menu, start a new game" (title screen `v f259fca8`). Before that: a regression fixed — the freeze that could hit
when an act was opened after a few boss fights is gone, and the act-clear frame no longer loses drawings to a full
sprite list; title screen `v a1c09634`. Before that: a player's report fixed — the
Chemical Plant 1 boss shows its bubble again, Sonic no longer disappears on Chemical Plant 2's sticky platforms, the fire
shield's white edges are gone in Chemical Plant 1, a Blue Sphere jump has its sound, and the sprite set a boss track
loads is now read a little at a time with the music waiting for it instead of starting into the drive read (the drive's
own pause still costs a moment); the title screen shows `v 2404f51b`.
Before that: the Pinball bonus stage's table is drawn, the endings have their music back, the credits end on the Thanks
for Playing artwork, and Time Attack offers Mighty and Ray. Before that: the menus fit the 320-pixel screen; faster and
nicer UFO special stages, always at 30 fps with two game steps a frame; every act faster (Studiopolis Act 1 averages 244
of the 262 units a 60 fps frame has); Frameskip in Options → Video.

## What the PS1 version can do

- **Mania Mode**, every zone from Green Hill to Titanic Monarch and Egg Reverie, with the bosses, the act transitions,
  the endings and the credits.
- Characters: **Sonic, Tails and Knuckles** (one at a time); with `--plus-characters` also **Mighty and Ray**.
- **Super forms**, the transformation included.
- **Special stages**: the UFO chases (30 fps with two logic steps a frame, so the game keeps its speed), the
  **Blue Spheres** bonus stages and, once every Blue Spheres gold medal is collected, the **Pinball** bonus stage from
  the star posts, as in Mania Plus (see [Pinball](#pinball)).
- **Time Attack** (Sonic, Tails and Knuckles; with `--plus-characters` all five), Options (Video: **Frameskip**, see
  [Frame rate and speed](#frame-rate-and-speed); Sound; Controls; Data), Extras, D.A. Garden, and **Puyo Puyo** (1P and 2P).
- **Saving** on the **memory card in slot 1** (one block, with a Mania icon): save files, Time Attack records, options.
  Without a card the game plays normally and doesn't save.

## Limitations and differences from the PC version

The PS1 is far smaller than the machines Sonic Mania was made for, so this port makes trade-offs. Everything below is
how the port behaves; it was tested in the PCSX-Redux and DuckStation emulators (DuckStation with a retail BIOS).

### Frame rate and speed

The acts, menus, cutscenes, Blue Spheres, Pinball and Puyo Puyo run at **up to 60 fps** with one game step per frame;
the **UFO special stages always run at a steady 30 fps with two game steps per frame**, so they keep their normal speed
(their busiest moments ran at 30-40 fps at one step).

- The game draws every frame and never skips one on its own, so when a frame takes longer than 1/60 s the **game itself
  runs slower** for that moment. Busy moments (many objects, several scrolling layers, big bosses) dip for a few
  seconds; a real PlayStation slows down a little more than the emulators.
- **Options → Video → Frameskip** (Off by default) keeps the game at its normal speed when the PS1 can't keep up: a slow
  moment draws fewer frames (down to 15 fps at worst) instead of slowing the game down. It works everywhere, the UFO
  and Pinball stages included (measured in PCSX-Redux: the busiest UFO stages from 99 % to 100 % of full speed). Off,
  every frame is drawn. The setting is kept on the memory card with the other options.
- The **Uncapped FPS** option of earlier versions is gone: the acts always aim for 60 fps (a saved No from an older
  version is ignored).

### Pinball

The Mania Plus **Pinball** bonus stage is in: once every Blue Spheres gold medal is collected, a star post's bonus
stars lead to Pinball instead of Blue Spheres, as in Mania Plus. The table is drawn: both floors in perspective with
their flippers, bumpers, rings and the score display, the scrolling background and the one-colour backdrop. The target
bumpers keep the colours baked into their models (their flashes are not drawn).

### Graphics

- **Some sprites are at half resolution** where a scene's art doesn't fit the PS1's 1 MB of video RAM: big effects,
  title-card and menu art in some scenes, large set pieces (Studiopolis, Press Garden, Mirage Saloon, Titanic Monarch),
  **Super Sonic** in some zones, and in a few zones the **bosses' largest parts** (Studiopolis, Press Garden Act 2,
  Mirage Saloon, Lava Reef Act 3, Titanic Monarch Act 3). Small sprites (players, badniks, rings, springs, the HUD's text)
  are always full size.
- **Fewer colours:** each player frame uses at most 15 colours, and the level art of many scenes is reduced to 15
  colours per palette block.
- **The UFO stages leave out their scenery decorations and the shadows.**
- **3D and effects are approximated by the PS1's GPU:** the giant rings (solid and wireframe), lines, gradient
  ("gouraud") shapes and some blending look close to the PC but not pixel-identical. Screen-wide tint effects other than
  the colour inversion aren't drawn; where a scene uses more than one extra palette at once (water lines), the second
  one shows the normal colours.
- **Videos** (the intro, the endings) play at 320×160 and 15 fps.

### Sound

- **Music** is CD-XA (37.8 kHz ADPCM), so it sounds slightly duller than the PC's Ogg files.
- **Sound effects** play at lower sample rates (8–44 kHz, each picked so a scene's set fits the 512 KB of sound RAM).
- **The music pauses briefly** when the game loads sprites from the disc in the middle of an act: when a boss appears,
  at the act clear and when you turn Super. The loading icon shows during these pauses (about half a second to a
  second).

### Loading

- Each act, menu and special stage loads from the CD (2× speed): a few seconds with the loading icon, longer than on PC.

### Not included

- **Encore Mode**, **Competition** (2-player versus), **replays** and Time Attack ghosts,
  online leaderboards, and the other Plus additions (the Plus title screen).
- **Sonic & Tails together** (one character at a time only; no sidekick).
- **Time Attack** with Sonic, Tails and Knuckles only (Mighty and Ray are Mania Mode characters here).
- The PC's video settings (window size, screen filter, vsync): the **Video** page holds only Frameskip. The PC's
  developer menu.
- **Languages** other than English (the Language option is not in Options).
- Controller vibration.

### Controls

Cross / Circle / Square jump (as A / B / X on PC), **Triangle** is the Super button (Y: turn Super in the air with 50 rings
and all Chaos Emeralds), L1 = C, R1 = Z, Start pauses.

## Plus characters

The engine's license (see `LICENSE.md`) requires every prebuilt executable to keep the Plus content off by default. The
executable in `bin/` offers Mighty and Ray only when the disc carries a small configuration file, which the builder
writes when you pass `--plus-characters`. Encore Mode and the other Plus features are not part of this port.

## Requirements

- Python 3.8+ with `numpy` and `Pillow` (`pip install -r requirements.txt`)
- [psxavenc](https://github.com/WonderfulToolchain/psxavenc), [FFmpeg](https://ffmpeg.org) (with Theora and Vorbis:
  `ffmpeg` and `ffprobe`), [mkpsxiso](https://github.com/Lameguy64/mkpsxiso)
- [CMake](https://cmake.org) and a C++20 compiler (to build the mesh optimiser once)

The programs are found on your `PATH`, or set `PSXAVENC`, `FFMPEG`, `FFPROBE`, `MKPSXISO`.

## The license file

Without a license file the image boots in emulators, on optical drive emulators and on modded consoles. To boot it on
an unmodified console from a burned disc it needs the license sectors of a PlayStation disc of your region
(`licensea.dat` for NTSC-U, `licensee.dat` for PAL, `licensej.dat` for NTSC-J), which you provide with `--license`.

## Credits

- **Sonic Mania**: Christian Whitehead, Headcannon, PagodaWest Games, Sonic Team, SEGA. This project is not affiliated
  with SEGA.
- **RSDKv5 decompilation** and **Sonic Mania decompilation**: Rubberduckycooly, st×tic and contributors (the code is
  theirs; see `LICENSE.md`).
- **Mesh optimiser**: Michael Fadely (mania-mesh-optimizer, MIT), with meshoptimizer by Arseny Kapoulkine (MIT).
- **PS1 SDK**: psyqo / nugget (PCSX-Redux team, MIT); ps1-bare-metal by spicyjpeg (MIT); EASTL / EABase (BSD).
- **Loading and memory-card icons**: author unknown.
- PS1 port: the RSDKv5-ps1 project.

## Licenses

`LICENSE.md` (the decompilation's license) applies to the executable and the code; the tools' licenses are in
`licenses/`. No game assets are distributed.
