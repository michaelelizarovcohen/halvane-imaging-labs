# Student worksheet

Halvane Imaging Labs is a fictional company built for this OSINT and digital-forensics lab. Read the [lab notice](index.html) first.

## Ground rules

- Work only from the **original files** (gallery "Download original" buttons, or `evidence/originals/`) and the pages of this site. Previews carry no metadata.
- Verify each download against `evidence/SHA256SUMS.txt` before you start (`sha256sum -c` from inside `evidence/`).
- Record every finding with: the asset ID, the exact field name (with its group, e.g. `ExifIFD:DateTimeOriginal`), the value, and the command you used.
- Distinguish what a file *records* from what a page *claims*. Say how confident you are and why.
- Comparing files with upstream copies from the source collections is outside the scope of these exercises.

## Setup

```
# all tags, with group names, no duplicates suppressed
exiftool -a -G1 -s FILE

# numeric values (decimal GPS, raw numbers)
exiftool -n -GPSLatitude -GPSLongitude -GPSAltitude FILE

# every date/time field in a file
exiftool -a -G1 -s -time:all FILE

# a pixel-data fingerprint that ignores metadata
exiftool -ImageDataHash -api ImageHashType=SHA256 FILE
```

Useful pages: [Gallery](../gallery/index.html), [Projects](../projects/index.html), [News](../news/index.html), [Team](../team.html), [Field Kit Library](../kit-library.html).

## Beginner

### B1 - First contact
Download **HIL-2501**. Report its make, model and `DateTimeOriginal`. Which field tells you the marketing name of the camera module?

### B2 - Coordinates
(a) Extract decimal GPS latitude, longitude and altitude from **HIL-1118**. Put the coordinates into a map and name the lake and the nearest village.

(b) Download all 28 Smartphone Field Panel originals (HIL-1201 to HIL-1228). How many contain GPS coordinates? Use a single ExifTool command with `-if`.

### B3 - Model codes
Phones often record an internal model code instead of a marketing name. Identify the marketing names for the devices behind **HIL-1219**, **HIL-1214** and **HIL-1228**.

### B4 - Glass
Which lenses were used for **HIL-1311**, **HIL-1309** and **HIL-2502**? Which field(s) did you rely on, and do any files expose more than one lens field?

### B5 - Software signatures
What does the `Software` field say for **HIL-1124** and **HIL-1401**? What does that tell you about how the photos were taken?

### B6 - Formats
Without opening the files in an image viewer, identify the file type and camera maker of **HIL-1012**, **HIL-1016**, **HIL-1510**, **HIL-1019** and **HIL-1405**.

### B7 - Check the caption
The caption of **HIL-1506** says it is a Galaxy S22 Ultra test. Does the file agree? Which time zone was the device set to?

### B8 - Same afternoon?
A 2010 newsletter (News, March 2010) says **HIL-1012** and **HIL-1013** were shot "the same afternoon". Test that claim with the files.

## Intermediate

### I1 - Who held the camera?
(a) Using serial numbers and the Field Kit Library, determine who most likely photographed **HIL-1104**.

(b) Felix's "Autumn rugged-kit tour 2021" post shows **HIL-1411** and **HIL-1413**. Confirm which kit items took them, where each was taken, how many days apart, and the straight-line distance between the two positions.

### I2 - Window seat
For **HIL-1401**, compare `DateTimeOriginal` with `GPSDateTime`. What UTC offset was the phone using, what region does that suggest, and what does the GPS altitude tell you about where the photographer was?

### I3 - The rail walk
The Florence lab walked a stretch of railway on 22 August 2015 with four handsets (**HIL-1226**, **HIL-1210**, **HIL-1215**, **HIL-1225**). Put the frames in capture order, list the device used for each, and calculate the straight-line distance between the first and last GPS fixes. Which frame cannot be placed on the map, and why?

### I4 - One phone or two?
**HIL-1202** and **HIL-1225** both come from a "Galaxy S III mini". **HIL-1201** and **HIL-1210** both come from an iPhone 4S. For each pair, decide whether one physical device could have taken both photos. Use model codes, firmware/OS versions and dates.

### I5 - The Boulder walk
Owen's June 2020 post says **HIL-1501**, **HIL-1503** and **HIL-1504** were taken near the Boulder office. Test that claim with the time fields. Then explain the relationship between **HIL-1501** and **HIL-1502**, and what the location in **HIL-1502** is worth.

### I6 - Careers page
The Careers page shows **HIL-1505** as "the Boulder team's January lunchtime walk, two blocks from the office". Verify the location and time zone.

### I7 - Whose camera app?
**HIL-1121** reports an unusual maker. What is going on with this phone and its camera software? Where and in which UTC offset was it taken?

### I8 - Texture Week
The 2017 Texture Week winner (**HIL-1325**) was credited to reader "M. H. Grey". Using the file and the Field Kit Library, what can you say about who actually took it? Look for supporting clues elsewhere on the site.

## Advanced

### A1 - TIDEMARK-25: what really happened in May?
The TIDEMARK-25 report says all seven figures (**HIL-2501** to **HIL-2507**) were captured during the field week of 5-9 May 2025. For each figure, determine the most likely real capture date and whether it falls inside the field week.

### A2 - Edited timestamps
Which TIDEMARK-25 figures carry a `DateTimeOriginal` that disagrees with the file's other time fields? List every conflicting field and value. Which independent clock inside one of the files is most persuasive, and why?

### A3 - A familiar frame
One TIDEMARK-25 figure has exactly the same pixel data as an Archive Zero file. Find it, prove it, and explain what each copy's metadata says about the capture date, the camera owner and the location. Could this camera have recorded GPS on its own?

### A4 - Wrong place
Two TIDEMARK-25 figures carry coordinates in Thuringia. Map them, then compare each scene with its coordinates. Identify where each scene really is (or what kind of place it must be), using visible features. Who held the camera that took **HIL-2503**, and when?

### A5 - Wrong clock
Explain the time-zone problem in **HIL-2505**. Using the Field Kit Library and the Team page, reconstruct when and where it was most likely taken and whether its camera was part of the TIDEMARK-25 kit.

### A6 - Edit history
Extract the XMP edit history (`XMP-xmpMM:History`) from all seven figures. Group the figures by workstation and time. Combine this with the News pages to establish where Jonas Ekdahl was when each group was edited and which desk the later edits came from. Note any other field that differs between the two groups. State clearly what the evidence does and does not prove.

### A7 - Reconcile the register
Build a table for all seven TIDEMARK-25 figures: device, serial (or internal serial), Field Kit Library tag, holder on the capture date, real capture date, and whether the `Artist` field is consistent with the register.

### A8 - Clocks and quirks
(a) For **HIL-1104**, work out the camera's UTC offset and how far its clock drifted from GPS time.

(b) **HIL-1405**, **HIL-1409** and **HIL-1413** each carry a `CreateDate` far from their capture date. Is this evidence of tampering? Justify your view.

## Bonus (optional, external)

### X1 - Reference structures
The ExifTool Meta Information Repository (exiftool.org/sample_images.html) publishes real metadata from thousands of cameras with replaced pixels. Download the archive for one maker represented here (for example DJI or Canon), find a model from the same family as a Halvane file, and compare the maker-note structure. Does anything in the Halvane file look out of place? Nothing from the repository is hosted on this site.

## Reporting template

| Exercise | Asset(s) | Field(s) and values | Command(s) | Finding | Confidence |
|---|---|---|---|---|---|
| | | | | | |
