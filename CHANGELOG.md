# Changelog

Updates to the Sonic Mania PS1 ISO Builder, newest first. To get an update, rebuild your disc image with the new
version of the builder (same steps as in the [README](README.md)).

## UFO stages at 30 fps, no Uncapped FPS option, Pinball in (October 2026)

- **The UFO special stages always run at a steady 30 fps with two game steps per frame**, so they keep their normal
  speed (their heavy parts ran at 30-40 fps at one step). Measured in PCSX-Redux over each stage's chase: UFO1-4 and
  UFO7 at full speed, UFO5 and UFO6 at 99 % (100 % with Frameskip On).
- **The UFO stages are lighter and look better:** many speed passes (the skies drawn from pre-rendered strips, the floor's
  far distance drawn from a coarser map, the 3D models in their lower-detail versions, the object updates and sorting in
  faster code); the floor's near tiles extend to 20 tiles with smoother 8x8 textures from 10 tiles away (mipmaps); rings
  and spheres appear farther away (a sixth of their full size); two GPU savings in UFO7. The scenery decorations and
  shadows stay off.
- **Options → Video → Uncapped FPS is gone:** the acts, Blue Spheres, Pinball and the menus always aim for 60 fps; a saved
  No from an earlier version is ignored. **Frameskip** is now the Video page's only option and works everywhere.
- **The Pinball bonus stage is in**, reached as in Mania Plus once every Blue Spheres gold medal is collected (a star
  post's bonus stars). It is enabled as-is: **its table floor and scrolling background are not drawn yet**, and the target
  bumpers keep a fixed colour. Its music and sounds are included.
- The acts are faster too (background drawing, the object update scan and the tile drawing in hand-written assembly,
  coarser far background scrolling where it doesn't show).
- The title screen shows the new build, `v 7234a48f`.
- Checked with the port's automated tests in PCSX-Redux (the full Mania set: boot, Green Hill 1, the special-stage route,
  the UFO 1 speed guard, the Flying Battery 2 memory fit) and the builder's own byte-by-byte check of the image. The
  builder's image (from `Data.rsdk`, 79 minutes) equals the port's own disc byte for byte except the two intro videos,
  which this run encoded with a newer FFmpeg (9.0.2). Not yet tested on a console.
- The image's SHA-256 changes (the new value is in the README's Output section).

## Flip-bit sprites on newer consoles, 60 fps by default (October 2026)

- **On consoles with the newer GPU (every PSone, most later PlayStations), mirrored level tiles and mirrored sprites
  are now drawn with the GPU's own flip feature** instead of as textured four-corner shapes, which costs the GPU less
  work. The game checks the GPU at start-up (nocash's GPU detection, then a tiny test drawing read back from video
  memory): on the earliest consoles, whose GPU lacks the feature, and on emulators that don't draw it, everything is
  drawn as before. The picture is the same either way (checked frame by frame in the DuckStation preview build, which
  draws the feature, against the old way of drawing); not yet tested on a console.
- **Options > Video > Uncapped FPS now defaults to Yes:** the zones and the UFO special stages run at one game step a
  frame (the 60 fps target) unless you set it to No. Saves from an earlier version are moved to Yes once.
- A second controller port that is empty is checked less often (it used to cost a little time every frame); a pad
  plugged into port 2 is still found within about half a second (Puyo Puyo's two-player mode, the menus).
- The title screen shows the new build, `v d4f959f9`.
- Checked with the port's automated tests in PCSX-Redux (boot to the menu, the GPU check, the Flying Battery 2 memory
  fit) and the builder's own byte-by-byte check of the image. Not yet tested on a console.
- The image's SHA-256 changes (the new value is in the README's Output section).

## Build stamp on the title screen (October 2026)

- **The title screen shows which build you are playing:** a small grey line in its bottom-left corner, e.g.
  `v c87bab35`. It is the commit of the RSDKv5-ps1 port the executable was built from, so a screenshot or a quick look
  tells which version runs in DuckStation, PCSX-Redux or on a console. It appears only on the title screen (not over
  the intro video) and fades with it.
- The builder writes it to a small `VERSION.TXT` file at the root of the disc (from `bin/VERSION.TXT`, which comes
  with each update together with the executable). A disc without that file shows `v unknown`.
- The executable also carries the port's stack overflow check since the previous update (port issue MA-188: a stack
  deeper than its reserve is now detected instead of silently writing into the scene's code).
- Checked with the port's automated tests in PCSX-Redux (boot to the menu, Green Hill 1, the Flying Battery 2 memory
  fit), and the builder's disc boots through the BIOS with the stamp on the title. Not yet tested on a console.
- The image's SHA-256 changes (the new value is in the README's Output section).

## The disc's executable is named after the game (October 2026)

- The disc now boots **`MANIA.EXE`** instead of `PSX.EXE` (the `BOOT` line of `SYSTEM.CNF`).
  Emulators and optical drive emulators that show a disc's executable name now show the game's. Nothing in the
  game itself changes.
- The image's SHA-256 changes with it (the new value is in the README's Output section).

## More free memory (October 2026)

- The game's debug log messages (which only an emulator's console showed) are left out of the executable: about 6 KB
  more free memory, the most needed in Flying Battery Act 2.

## Fixes from a test round (October 2026)

- **No crash after a UFO stage or a Blue Spheres stage:** returning to the zone could stop the game with an error (the
  loading icon started a second transfer to the video RAM while a load was using it).
- **Studiopolis' shop windows:** their reflections no longer smear over the screen outside the window.
- **Save select:** the zone picture in a save slot scrolls again.
- **Studiopolis' popcorn machine:** half as many popcorn kernels, so the act no longer slows down after the machine
  (about 99 % of full speed there, up from about 91 %).

## Frameskip option (October 2026)

- **Options → Video → Frameskip** (Off by default): when the PS1 can't keep up, the game keeps its normal speed by
  drawing fewer frames (down to 15 fps at worst), in the zones and the UFO special stages. Saved on the memory card with
  the other options.

## Studiopolis and 30 fps fixes (October 2026)

- Studiopolis' shop-window silhouettes and TV vans fixed; hit flashes, blinking debris and similar effects flicker again
  at 30 fps; objects no longer see themselves off-screen every other step at 30 fps; videos play in PCSX-ReARMed.

## Uncapped FPS option, CD recovery, speed fixes (October 2026)

- **Options → Video → Uncapped FPS** (No by default): No runs the zones at a steady 30 fps at full game speed;
  Yes draws up to 60 fps but slows down in busy places. The Language entry left Options (English only).
- A CD drive that stops answering no longer freezes the game when the music pauses; several zones run faster.

## First release (October 2026)

- The prebuilt PS1 executable and the tools that convert the game's data and build the disc.
