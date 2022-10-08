# revengedit
A command-line editor for editing *Zuma's Revenge!* `*.dat` files' level settings.

**No, this doesn't let you edit the `*.dat` file's path. This is a *command-line
utility*, meaning you run this from a Command Prompt window.**

## Why?
In Zuma Deluxe, you could edit each levels' difficulty in a simple `levels.xml` file:

```xml
<Settings id="lvl11" speed=".5" start="35" score="1000" repeat="40" colors="4" reloaddelay="0" mergespeed=".05" firespeed="6" repeat="50" partime="25" />
<Settings id="lvl12" speed=".5" start="35" score="1000" repeat="40" colors="4" reloaddelay="0" mergespeed=".05" firespeed="6" repeat="50" partime="35"/>

<!-- ... -->

<StageProgression
    stage1 = "spiral,claw,riverbed,targetglyph,blackswirley"
    diffi1 = "lvl11,lvl12,lvl13,lvl14,lvl15"
    stage2 = "tiltspiral,underover,warshak,loopy,snakepit"
    diffi2 = "lvl21,lvl22,lvl23,lvl24,lvl25"
    ...
/>
```

However, due to the open nature of Zuma Deluxe's files, PopCap decided to archive the
game files inside a `main.pak`. Only problem is that the `*.dat` files (which contains
the curve/path for the level, one file for each path) can't be read if they are inside
the archive. Sure, they could've done it in their `levels.xml`, but one could've just
guessed which fragment of the `pak` archive is the xml file in - and xor it by `0x7F`,
which is the "encryption" method used by these files. So their possible solution was to
place these properties in the `*.dat` files themselves. Besides, every level in Zuma's
Revenge was unique (one map = one level), so I could see why they did it. Nobody was
able to figure out the way these files work back in 2009 anyway (especially the curve
itself).

<!-- remember, no big ego -->

```
Offset(h) 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F
                        
00000000  43 55 52 56 0F 00 00 00 00 37 00 00 00 00 00 00  CURV.....7......
00000010  00 28 00 00 00 06 00 00 00 06 00 00 00 CD CC 4C  .(...........ÍÌL
00000020  3F C8 00 00 00 00 00 00 00 00 00 C8 42 D8 0E 00  ?È.........ÈBØ..
00000030  00 4B 00 00 00 C2 01 00 00 4C 04 00 00 00 00 80  .K...Â...L.....€
00000040  40 05 00 00 00 0D 00 00 00 64 00 00 00 FF FF FF  @........d...ÿÿÿ
00000050  7F 64 00 00 00 FF FF FF 7F 64 00 00 00 FF FF FF  .d...ÿÿÿ.d...ÿÿÿ
00000060  7F 64 00 00 00 FF FF FF 7F 00 00 00 00 00 E1 F5  .d...ÿÿÿ......áõ
00000070  05 00 00 00 00 00 E1 F5 05 00 00 00 00 00 E1 F5  ......áõ......áõ
00000080  05 64 00 00 00 FF FF FF 7F 64 00 00 00 FF FF FF  .d...ÿÿÿ.d...ÿÿÿ
00000090  7F 64 00 00 00 FF FF FF 7F 00 00 00 00 00 E1 F5  .d...ÿÿÿ......áõ
000000A0  05 00 00 00 00 00 E1 F5 05 00 00 00 00 00 E1 F5  ......áõ......áõ
000000B0  05 26 02 00 00 01 01 01 01 01 00 01 01 00 00 00  .&..............
```

Offset `0x04` is the "version" of the curve. `0x02` is used for Zuma Deluxe,
`0x0C` / `0x0E` is for earlier builds of Zuma's Revenge (`levels/boss1`
has LOADS of leftover test files, although initially unusuable due to
likely-intentional removing of the 4th byte of each curve point) and
`0x0F` is what seems to be the "final" version.

Although the games won't really care what version the CURV file is in,
**revengedit will read this byte and if it is not `0x0E` or `0x0F` then it will not parse
the file, since Zuma Deluxe `*.dat` files do not have difficulty information
stored in them.**

Version `0x0C` has slightly different offsets.

So far, the offsets for specific properties are, taken from version `0x0F`:
- `0x09` - `start - int`
  - Where the balls arrive after the path sparkles
- `0x11` - `repeat - int`
  - Chance of next ball being the same color as the previous one
- `0x15` - `single - int`
  - Chance of ball being a single, independent of `repeat`
- `0x19` - `colors - int`
  - How much colors the level should have; minimum of 3 or the game crashes, maximum
    of 6 before the game reads "colors" from other directories other than `balls`
- `0x1D` - `speed - float`
  - How fast the balls normally are
- `0x2D` - `score - int`
  - The amount of points the player has to reach in order to fill the Zuma bar
- `0xB7` - `destroyall - bool`
  - If any remaining balls should be destroyed after the Zuma bar has been filled up
  - **This is actually an inverted boolean in Revenge;** in Deluxe, setting
    `destroyall="true"` enables it. Thus, in Revenge, a value of `01` is disabled and
	  vice versa.
- `0xB8` - `showskull - bool` (*unofficial name*)
  - If the skull should be shown at the end of the path
- `0xB9` - `dieatend - bool`
  - If set to `00`, any balls that enter the skull will not trigger a level fail. Instead,
    the ball will be destroyed (no points). The warning skulls will also not show up
	when the balls enter the danger zone.
- `0xBA` - `crashonload - bool`
  - Whatever nefarious things you would like to do with this... I won't judge.

    Seems to be a deprecated developer thing.

Zuma's Revenge is still a b!7⊂h to mod, though.

## Prerequisites
I used Python 3.8 for development, so that version is recommended.
Python =3.7 and ≥3.9 *might* work.

https://www.python.org/downloads/

**Make sure to check "Add Python (version) to PATH". This allows you to invoke
Python within a console window.**

## Installation
Clone this repository and extract it. Run this command in the directory of the
`revengedit` folder.
```
:: let's say the folder is in %HOMEDRIVE%%HOMEDIR%/revengedit
C:/Users/Name/revengedit>pip install -e .

:: or if you somehow can't run pip saying that it's not executable...
C:/Users/Name/revengedit>py -3 -m pip install -e .
```

## Usage
You can simply invoke `revengedit` if pip successfully did it's thing:
```bat
revengedit
```

else, you can do this:
```bat
:: do this in the directory with revengedit in it
:: NOT inside the revengedit directory
py -3 -m revengedit
```

### Viewing Current Values
You can inspect the current property values of a `*.dat` file:
```
> revengedit view Jungle1_hard.dat
File: Jungle1_hard.dat

 start: 55
 repeat: 40
 single: 6
 colors: 6
 speed: 0.8038985875900835
 score: 3800

 destroyallDisabled: True
 showskull: True
 dieatend: True
 crashonload: False
```
