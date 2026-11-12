# Changelog

Updates to the Sonic Mania PS1 ISO Builder, newest first. To get an update, rebuild your disc image with the new
version of the builder (same steps as in the [README](README.md)).

## Back to the version before the loading-icon work (November 2026)

The previous update froze on Chemical Plant 1's loading screen. This image goes back to the build before it: the version
that played Chemical Plant 1, its boss, the act clear and the next act without a loading stall — `v 60ef20a5`.

What this means if you tested the previous two images:

- the loading icon no longer shows while a boss fight's or Super Sonic's sprite set is read, as it did not before; those
  loads can look like a short pause, and that is the state this build restores;
- the "finish an act, leave to the main menu, start a new game" bookkeeping fixes are gone with it, so the Green Hill 1
  loading stop reported against an earlier image is unproven again — if it happens, please give the zone, the act, and
  what you did just before;
- the Super transformation's music streams from the XA track again (the CD spins it up), not from a small stream on the
  disc: the pipeline change that put it there was part of the reverted work.

The title screen shows `v 60ef20a5`.

## The loading icon back where it was missing, and stricter memory bookkeeping (November 2026)

Two items from the last tester's list:

- **The loading icon is back in the corner while a boss's or Super Sonic's sprite set loads.** The previous update had
  taken it out of those loads (its own drawing made the frame that started them lose some sprites), so they looked like
  freezes. It is drawn again, at no cost to the frame: the icon no longer takes over the memory the drawing needs.
- **Memory bookkeeping made strict** for the route "finish an act, leave to the main menu, start a new game": a sprite
  set's load is now cancelled before a scene's data is released, and the load's working area no longer borrows memory a
  scene keeps for itself. The stop on Green Hill 1's loading screen that was reported against the previous image could
  not be reproduced with it, so treat this as a correctness fix rather than a confirmed repair - and tell me if it
  happens again, with the zone, the act and what you did just before.

The title screen shows `v f259fca8`.

## The freeze when opening an act, fixed (November 2026)

A regression in the previous update: after a few boss fights the game could freeze when an act was opened, with no way
back. A boss track's sprite set was re-read a second time inside one frame, and each of those reads leaked a slice of
the engine's memory; once enough had gone, the next act could not load and the game stopped. Fixed: each set is read
once, a piece at a time, and the memory comes back. The act-clear frame that starts such a read also lost some of its
drawings to a full sprite list; that is fixed too. The title screen shows `v a1c09634`.

## A player's report fixed, and boss fights that no longer stall (November 2026)

Fixes for the list a player posted after testing the previous image:

- **The Chemical Plant 1 boss's bubble is back.** The fight's big translucent blob was drawn as a thin blue bar: the
  game draws it one scanline at a time, and on the PS1 the sprite's texture position cannot follow that.
- **Sonic no longer disappears on Chemical Plant 2's sticky platforms** - the ones that hold him by a vertical face: his
  "stuck" pose was missing from that act's sprite set.
- **The fire shield's white edge pixels are gone in Chemical Plant 1** (the shields are stored at full resolution there
  again). Chemical Plant 1 has the video memory for it; **Chemical Plant 2 does not**, and its bubble shield still shows
  the slightly blocky rim - measured, not overlooked.
- **A Blue Sphere jump has its sound.** The bonus stage's sound banks were missing Sonic's jump sound, so a jump there
  was silent.
- **A boss fight's music no longer dies while its sprite set loads.** The set the boss track needs was read in one
  frame, the read stopped the track, and the track then started straight into the next read; the set is now read a little
  at a time over several frames and the track starts when it lands. The drive's own pause for a read still costs about a
  second at Chemical Plant 2's Mean Bean Machine entrance: measured, still open, and named in the port's plan.

Nothing else got coarser: the shields' full resolution costs Chemical Plant 1 extra work at build time only, and the
effect sprites are halved exactly where they were before.

The title screen shows `v 2404f51b`.

## The Pinball table is drawn, and fixes across the game (November 2026)

The Mania Plus **Pinball** bonus stage now draws its **table**: both floors in perspective with their flippers, bumpers,
rings and the score display, plus the scrolling background and the one-colour backdrop behind them (a dark backdrop
showed under the ball before). The table's map and its scrolling layer share one page of the PS1's video RAM, so the
stage still fits in 1 MB. The target bumpers keep the colours baked into their models; their flashes are not drawn.

Fixes since the last update:

- **The endings have their music and sounds back**: the Bad, Good and True End videos played muted.
- **The credits end on the Thanks for Playing artwork**, and the normal campaign's credits reach it, as on PC (until
  now the screen showed only its background).
- **Time Attack offers Mighty and Ray** on a disc built with `--plus-characters`, and its first track (Competition)
  loads with the usual spinner instead of a silent wait.
- **Game Options no longer shows the "& Knuckles" row** that the 32 silver medals used to unlock.
- **Options → Controls draws a DualShock 1** (the PS1's own pad), not a DualShock 4.
- **Music loops no longer click**: the CD audio fades across the seam at the loop point.
- **Sharp again where the stage can afford it**: the shields (Green Hill 1, Chemical Plant 2, Press Garden 2 and Mirage
  Saloon 1K), Sonic's 18 frozen frames in Press Garden 2, Knuckles' Mirage Saloon pause labels and the art both Mirage
  Saloon bosses share, and the Main Menu's gameplay panel mask.
- **The Plus UFO stages show their rings, spheres and pause text**: their second layouts had no sprite atlas at all.
- **Sonic stays visible during the Angel Island warp**, the **Title screen holds 60 fps**, and the full-screen ruby
  flash draws through the GPU chain again.
- **Faster sprite drawing**: the common case (a full-resolution frame inside one page, no tint) now draws in one pass,
  63 % of Green Hill 1's sprites, with the frame's GPU chain identical to the previous build.
- The title screen shows the new build, `v eaf0f1d8`.

Checked with the port's automated tests in PCSX-Redux (the quick tier: 134 PASS, 0 FAIL), the port's own disc
verification, the exporter's checks (`SHA256SUMS` over the executable and every overlay), and the builder's own
byte-by-byte verification of the image (sector headers, EDC/ECC, the index and every file against its source); the
image also boots in PCSX-Redux through a retail BIOS. The image is a little larger than the previous one (545 MB): the
sharper sprites and the new Pinball and special-stage atlases add up to a few megabytes. **The image's SHA-256 changes**
(the new value is in the README's Output section), and the conversion now takes about three hours on a recent Mac (the
sprite fitting is the long part).

## Faster in every act (November 2026)

The game runs faster almost everywhere; nothing looks or plays differently (every change was checked frame by frame
against the previous build), except the Oil Ocean smog, which is now drawn in slightly coarser strips. Measured in
PCSX-Redux in CPU time per frame (a frame at 60 fps has 262 units):

- **Studiopolis Act 1**, the slowest act, now averages 244 (was 273), its worst point 272 (was 308): objects that
  wait off screen no longer retry every frame, the invisible blocks skip players out of reach, the Rock'em Sock'ems draw
  faster.
- **Hydrocity Acts 1 and 2**, **Lava Reef Act 1**, **Press Garden Act 2** and **Titanic Monarch Act 3**: the water and
  heat-haze lines are computed while drawing, and changed palette rows are uploaded directly (Hydrocity 2 averages 232,
  was 256; Press Garden 2 258, was 276; Lava Reef 1 and Titanic Monarch 3 now stay under 262 everywhere).
- **Metallic Madness Act 1** stays under 262 everywhere (its worst point was 330): its far background draws faster.
- **Spikes and bosses**: the giant Special Ring (55 → 32), the Metallic Madness sound checks, the Mirage Saloon
  RollerMKII (a 102 spike, now 23), the Flying Battery electromagnets (71 → 8), the Egg Reverie emeralds, Flying
  Battery's Tuesday network, the Stardust Speedway Funnels and Lotto Machine, Press Garden's paper rollers and crates,
  Titanic Monarch's teeter-totters, Lava Reef's palette fades and Stardust Speedway's fireflies.
- **Oil Ocean Act 2**: the smog costs 33 instead of 46, and the HUD under it 15 instead of 22.
- Memory: the rotating-background code moved out of the always-loaded part of the game, so Flying Battery Act 2 has
  twice the spare memory it had.

## Menus fit the 320-pixel screen (October 2026)

- **The corner button prompts are full size again and sit lower:** the button icon was drawn at three-quarter size (the
  GPU sampled it unevenly, so it looked pixelated). It draws at the artist's size now (19-20 px of ink instead of 12-15),
  and both rows moved down, leaving an 8-px margin above them. The second row overlaps the top of the heading banner,
  which is intended: no page content is touched (everything below y 50 is identical to the previous build).
- **The heading banner sits 18 px lower**, giving the two prompt rows the top of the screen.
- **The Extras page's choice panels moved 24 px left** (their right column was cut by the 320-pixel screen), and its
  medallion panel 16 px left.
- **The Game Options page's ON/OFF/MANIA columns moved 16 px left**, ending 22 px clear of the screen's right edge.
- **The title screen's SEGA copyright moved 52 px left**, no longer cut at the right edge (it now ends at x 305).
- Everything else is as in the previous update: the acts aim for 60 fps with no frame skip, the UFO special stages run at
  30 fps with two game steps a frame, Frameskip is the Video page's only option, and the Pinball bonus stage is in (its
  table not drawn yet).

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
