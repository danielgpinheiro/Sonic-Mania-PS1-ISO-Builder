# Changelog

Updates to the Sonic Mania PS1 ISO Builder, newest first. To get an update, rebuild your disc image with the new
version of the builder (same steps as in the [README](README.md)).

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
