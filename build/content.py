"""Public, in-world content for the Halvane Imaging Labs training website.

Everything in this file is fictional and student-facing. Teaching notes and exercise keys never belong here.
"""

COMPANY = dict(
    name="Halvane Imaging Labs",
    legal="Halvane Imaging Labs ApS (fictional)",
    tagline="Field-proven imaging evaluation",
    short="Independent field and bench evaluation of cameras, phones and aerial imaging systems - and the metadata they leave behind.",
    founded=2003,
    email="studio@halvane.example",
    press="press@halvane.example",
)

OFFICES = [
    dict(city="Copenhagen", country="Denmark", role="Headquarters, colour bench and ingest desk",
         detail="Nordhavn studio (since 2019). Visits by appointment.", since=2003, email="studio@halvane.example", phone=""),
    dict(city="Florence", country="Italy", role="Mobile Imaging Lab",
         detail="Smartphone and tablet evaluation, opened September 2015.", since=2015, email="firenze@halvane.example", phone=""),
    dict(city="Boulder", country="Colorado, USA", role="Aerial & Action Systems",
         detail="Drones, action cameras and stabilisation rigs, opened May 2016.", since=2016, email="boulder@halvane.example",
         phone="+1 303 555 0142"),
]

# ----------------------------------------------------------------------------------------------- PEOPLE
PEOPLE = [
    dict(slug="maren-halvik", name="Maren Halvik", role="Co-founder & Chief Executive", office="Copenhagen", since=2003,
         bio="Maren trained as a broadcast camera engineer and spent six years repairing studio cameras before co-founding "
             "Halvane with Teodor in 2003 (the name is half Halvik, half Vane). She still carries a pocket compact everywhere, "
             "judges the occasional reader contest and insists that the only honest colour is 18% grey.",
         focus=["Strategy", "Client reviews", "Street photography"]),
    dict(slug="teodor-vane", name="Teodor Vane", role="Co-founder & Chief Scientist", office="Copenhagen", since=2003,
         bio="Teodor built the first Halvane test procedures on a kitchen table and a 5-megapixel compact during a western Norway "
             "road trip in the summer of 2003. He curates the 'museum shelf' of historic bodies, still borrows them for winter walks, "
             "and spent much of 2021 digitising his own slide archive. Pixel, his dachshund, appears in more test frames than any employee.",
         focus=["Colour science", "Sensor history", "Archive Zero"]),
    dict(slug="grace-adeyemi", name="Grace Adeyemi", role="Head of Operations & Field Kit Librarian", office="Copenhagen", since=2012,
         bio="Grace runs the Field Kit Library, the ingest desk and everything in between. Every body, lens and drone that leaves the "
             "Nordhavn store is checked out against a name and a date - a rule she introduced in 2012 and has defended ever since.",
         focus=["Operations", "Field Kit Library", "Ingest pipeline"]),
    dict(slug="felix-brandauer", name="Felix Brandauer", role="Principal Field Engineer, Alpine & Nordic", office="Copenhagen", since=2010,
         bio="Felix joined in March 2010; his first summer assignments included two sheep and a borrowed body. Since then he has led the "
             "Alpine & Nordic Light Programme: glacial lakes in 2010, the Inside Passage in 2014, and the 2021 autumn rugged-kit tour "
             "from Occitanie to the Ruhr.",
         focus=["Field campaigns", "Weather sealing", "Phone HDR"]),
    dict(slug="kenji-moriwaki", name="Kenji Moriwaki", role="Colour Bench Lead", office="Copenhagen", since=2014,
         bio="Kenji runs the colour bench: charts, targets, still lifes and the bench mascot. He is famous for labelling every body "
             "he configures - if a bench camera has an owner set in its menus, it was probably Kenji who set it.",
         focus=["Colour targets", "Profiling", "Still-life series"]),
    dict(slug="lucia-ferrante", name="Lucia Ferrante", role="Director, Florence Mobile Imaging Lab", office="Florence", since=2015,
         bio="Lucia opened the Florence lab in 2015 and ran the Smartphone Field Panel: dozens of handsets, the same scenes, no edits "
             "in camera. Her weekend field days in the Mugello hills became the panel's most-used reference set.",
         focus=["Smartphone evaluation", "Panel design", "Field days"]),
    dict(slug="dana-whitlock", name="Dana Whitlock", role="Head of Aerial & Action Systems", office="Boulder", since=2016,
         bio="Dana built the Boulder team from a borrowed garage and one quadcopter. She designed our stabiliser vibration rig and "
             "still flies every new airframe herself before it is signed out.",
         focus=["Drones", "Action cameras", "Vibration testing"]),
    dict(slug="owen-achterberg", name="Owen Achterberg", role="Mobile Systems Engineer", office="Remote (Richmond, Virginia)", since=2019,
         bio="Owen works remotely from Richmond, Virginia and joins the Boulder team on site for one week each month. He specialises "
             "in HEIF containers, phone RAW pipelines and the gap between what a spec sheet promises and what a file records.",
         focus=["HEIF/HEIC", "Phone RAW", "US field work"]),
    dict(slug="rosa-quintero", name="Rosa Quintero", role="Communications & Media", office="Copenhagen", since=2018,
         bio="Rosa edits this website, the newsletter and every press kit. She also books the conference trips nobody else wants to plan.",
         focus=["Communications", "Media kit", "Events"]),
    dict(slug="jonas-ekdahl", name="Jonas Ekdahl", role="Field Engineer, Rugged Kit", office="Copenhagen", since=2019,
         bio="Jonas leads rugged-kit evaluations and was field lead for TIDEMARK-25. He spent October 2023 testing waterproof "
             "compacts at a trade fair in Japan and is a regular speaker at imaging-assurance conferences.",
         focus=["Rugged kit", "Insurance documentation", "Drones"]),
    dict(slug="amara-osei", name="Amara Osei", role="Lead, Provenance & Metadata Assurance", office="Copenhagen", since=2021,
         bio="Amara came to Halvane from a newsroom verification desk. She leads our Provenance & Metadata Assurance practice and "
             "her rule is simple: if you cannot explain a timestamp, you cannot trust it.",
         focus=["Verification", "Metadata audits", "Training"]),
]

ALUMNI = [
    dict(name="Matteo Rinaldi", role="Field Technician, Florence (2015-2019)",
         note="Co-ran the Mugello field days with Lucia, including the August 2015 rail walk."),
    dict(name="Ida Holm", role="Imaging Intern, summer 2024",
         note="Ingest desk; back-filled the legacy compacts set into the archive."),
    dict(name="Tomas Varga", role="Imaging Intern, summer 2025 (June-August)",
         note="Ingest desk; archive digitisation and report production support."),
]

# ----------------------------------------------------------------------------------------------- SERVICES
SERVICES = [
    dict(slug="field-evaluation", name="Field evaluation",
         text="We take cameras, lenses and phones where your people will use them: harbours, glaciers, building sites and night streets. "
              "Every evaluation ships with the untouched files so you can check our working."),
    dict(slug="colour-bench", name="Colour bench & calibration",
         text="Reflective and transmissive targets, controlled still lifes and repeatable lighting. We profile bodies for archives, "
              "museums and e-commerce studios."),
    dict(slug="mobile-lab", name="Mobile imaging lab",
         text="From Florence, we benchmark smartphones and tablets as people actually use them: auto mode, default app, "
              "the scene in front of them."),
    dict(slug="aerial-action", name="Aerial & action systems",
         text="Drone and action-camera evaluations for surveyors, insurers and broadcasters, including vibration and stabilisation testing."),
    dict(slug="provenance", name="Provenance & metadata assurance",
         text="Independent audits of image metadata for newsrooms, insurers and legal teams: capture-time verification, device "
              "attribution, location checks and edit-history review."),
]

# ----------------------------------------------------------------------------------------------- PROJECTS
PROJECTS = [
    dict(slug="archive-zero", name="Archive Zero", years="2003-2010", lead="Teodor Vane", status="Complete",
         summary="The founders' reference set: the frames that defined Halvane's first test procedures.",
         body=[
             "Before Halvane had clients it had an archive. Archive Zero collects the frames Maren and Teodor used to build our "
             "first evaluation procedures: a fjord shot on a compact in 2003, a high valley on a first professional body, a "
             "harbour comparison between two very different sensors, and Pixel, the studio dog, who features in rather too many "
             "white-balance tests.",
             "The set is deliberately heterogeneous: compacts, rangefinders, DSLRs, a film scanner and a cinema camera. Some files "
             "carry rich maker notes; one carries almost nothing at all. That variety is the point - our procedures had to work "
             "on all of them.",
             "The archive is read-only. New material is never added to Archive Zero; derived copies get new asset numbers.",
         ]),
    dict(slug="alpine-nordic", name="Alpine & Nordic Light Programme", years="2010-2022", lead="Felix Brandauer", status="Ongoing",
         summary="Long-term study of low sun, snow, haze and water across mountain and northern environments.",
         body=[
             "Bright snow under low sun, haze over long lakes and the blue hour that lasts all night in a northern summer are hard "
             "on sensors and harder on phone processing. Since 2010 the Alpine & Nordic Light Programme has collected reference "
             "scenes in exactly those conditions.",
             "The programme mixes dedicated cameras with phones running stock and third-party camera apps, so we can compare what "
             "the hardware records with what the software decides to show you.",
         ]),
    dict(slug="smartphone-field-panel", name="Smartphone Field Panel", years="2014-2017", lead="Lucia Ferrante", status="Complete",
         summary="Dozens of handsets, the same kinds of scenes, auto mode only. The Florence lab's founding study.",
         body=[
             "The Smartphone Field Panel asked a simple question: what does a typical phone actually record when a typical person "
             "points it at a typical scene? We collected handsets across brands and price points and photographed campus "
             "buildings, markets, corridors, fields and vineyards around Florence and in the Mugello hills, always in auto mode, "
             "always in the default camera app.",
             "Several panel days used multiple handsets at once. On 22 August 2015 Lucia and Matteo walked a stretch of the Mugello "
             "railway with four devices - a day still used to teach multi-device timeline reconstruction.",
             "Panel files are published exactly as recorded, with descriptive and rights metadata added during ingest.",
         ]),
    dict(slug="colour-bench", name="Colour Bench & Still-Life Series", years="2014-present", lead="Kenji Moriwaki", status="Ongoing",
         summary="Charts, targets and still lifes: the repeatable half of every evaluation.",
         body=[
             "Every body that enters the bench meets the same targets: a reflective IT8, a portable colour checker, a resolution "
             "chart and a rotating cast of still lifes chosen to break demosaicing algorithms - saturated reds, metallic highlights, "
             "fine repetitive texture.",
             "Bench files are ingested on the bench workstation and keep their full maker notes. Owner fields are set in-camera "
             "where the body supports it.",
         ]),
    dict(slug="aerial-action", name="Aerial & Action Systems", years="2016-present", lead="Dana Whitlock", status="Ongoing",
         summary="Drones, action cameras and the vibration rig that keeps them honest.",
         body=[
             "Boulder evaluates the cameras that move: quadcopters, foldable drones, action cameras and phones shooting through "
             "aircraft windows. Positioning data matters as much as pixels here, so every file is checked for GPS, altitude and "
             "time consistency before it enters a report.",
             "The autumn 2021 rugged-kit tour (with Felix) ran from a lake beside a motorway in Occitanie to industrial heritage "
             "in the Ruhr, a week apart.",
         ]),
    dict(slug="tidemark-25", name="TIDEMARK-25", years="2025", lead="Jonas Ekdahl", status="Under internal review",
         client="Fellstrand Mutual",
         summary="Field-kit evaluation for claims documentation in inland flood and storm scenarios. Report imagery under review.",
         body=[
             "TIDEMARK-25 evaluated drones and rugged cameras for documenting inland flood and storm claims for Fellstrand Mutual. "
             "The field week ran from Monday 5 to Friday 9 May 2025 across Thuringia and northern Hesse, led by Jonas Ekdahl.",
             "Report v1 (two figures) was delivered on 30 May 2025. Report v2, adding figures 3 to 7 to cover days 1, 3, 4 and 5, "
             "was delivered on 20 June 2025.",
             "In October 2025 Fellstrand Mutual raised questions about the v2 imagery. The figures below are published unchanged, "
             "exactly as delivered, so that the review can be checked independently. See the statement of 28 October 2025.",
         ]),
]

# ----------------------------------------------------------------------------------------------- FIELD KIT LIBRARY
# serial column shows the last five characters of the serial (or internal serial) as recorded at check-in.
KIT = [
    ("HK-003", "Canon PowerShot G5", "not recorded", [("Teodor Vane", "2003-06-01", "2008-12-31")], "Retired. Owner name set in camera."),
    ("HK-005", "Nikon D1X", "not recorded", [("Teodor Vane", "2004-03-15", "2009-02-28")], "Retired."),
    ("HK-011", "Sigma DP1", "08620", [("Maren Halvik", "2008-05-02", "2012-12-14")], "Retired."),
    ("HK-012", "Nikon D70s", "4d740", [("Teodor Vane", "2009-01-12", "2013-06-30")], "Retired."),
    ("HK-014", "Epson R-D1", "not recorded", [("Teodor Vane", "2009-11-02", "2012-08-31")], "Museum shelf."),
    ("HK-015", "Nikon D80", "42078", [("Felix Brandauer", "2010-03-01", "2014-02-28")], "Retired."),
    ("HK-016", "Konica Minolta Dynax 7D", "not recorded", [("Felix Brandauer", "2010-07-26", "2010-08-06")], "Pool loan."),
    ("HK-021", "Canon PowerShot G12", "not recorded", [("Maren Halvik", "2015-12-18", "2016-01-08")], "Holiday loan; pool since."),
    ("HK-022", "Canon EOS 70D", "05426", [("Felix Brandauer", "2014-03-03", "2016-04-29"), ("Dana Whitlock", "2016-05-02", "2019-08-30")], ""),
    ("HK-027", "Pentax K10D", "94983", [("Kenji Moriwaki", "2014-05-05", "2018-01-31")], "Internal serial."),
    ("HK-029", "Ricoh GR", "02012", [("Maren Halvik", "2016-03-01", "present")], "Personal-use allowance."),
    ("HK-033", "Kodak DCS 760", "8056", [("Teodor Vane", "2017-04-10", "2017-04-18")], "Museum shelf. Sensor serial."),
    ("HK-035", "Canon EOS 40D", "09769", [("Kenji Moriwaki", "2017-09-04", "2019-12-20")], "Bench body."),
    ("HK-037", "Olympus E-410", "90609", [("Kenji Moriwaki", "2016-11-07", "2017-06-30")], "Bench body."),
    ("HK-038", "Sony DSLR-A100", "05000", [("Colour bench pool", "2017-01-01", "present")], "Internal serial."),
    ("HK-040", "GoPro HERO7 Black", "47612", [("Dana Whitlock", "2018-08-20", "2020-03-13")], ""),
    ("HK-042", "Autel Robotics EVO II", "not exposed", [("Dana Whitlock", "2019-04-15", "2021-10-29")], "Serial not written to files."),
    ("HK-043", "GoPro HERO8 Black", "86482", [("Felix Brandauer", "2020-02-17", "2021-05-31")], ""),
    ("HK-044", "Fujifilm X-S10", "11594", [("Kenji Moriwaki", "2020-11-23", "2023-06-30")], "Bench body."),
    ("HK-046", "DJI Mini 2", "B0A72", [("Felix Brandauer", "2021-08-30", "2023-03-31")], ""),
    ("HK-047", "GoPro HERO10 Black", "30426", [("Felix Brandauer", "2021-09-13", "2023-03-31")], ""),
    ("HK-048", "Canon EOS R6", "04357", [("Kenji Moriwaki", "2021-04-12", "2024-05-31")], "Bench body."),
    ("HK-052", "OM System TG-7", "11028", [("Jonas Ekdahl", "2023-10-02", "2024-03-28"), ("Copenhagen store (not issued)", "2024-03-28", "present")], "Rugged compact."),
    ("HK-055", "Panasonic Lumix DMC-LX7", "0069I", [("Legacy compacts shelf", "2014-01-01", "present")], "Internal serial."),
    ("HK-058", "Sigma fp", "15977", [("Owen Achterberg", "2024-01-15", "present")], ""),
    ("HK-061", "Canon EOS R5 Mark II", "03530", [("Kenji Moriwaki", "2024-08-12", "present")], "Bench body."),
    ("HK-063", "Nikon Z6III", "01011", [("Owen Achterberg", "2024-06-17", "present")], ""),
    ("HK-066", "Nikon Z5II", "01281", [("Jonas Ekdahl", "2025-04-14", "present")], ""),
    ("HK-067", "DJI Mavic 3 Pro", "A0033", [("Jonas Ekdahl", "2025-04-28", "2025-05-16")], "TIDEMARK-25 kit."),
    ("HK-068", "Samsung GX-1L", "51706", [("Copenhagen store", "2019-01-01", "2025-06-02"), ("Tomas Varga", "2025-06-02", "2025-08-29")], "Internal serial. Intern RAW-workflow loaner."),
    ("HK-069", "Minolta DiMAGE 5", "not recorded", [("Teodor Vane", "2024-12-20", "2025-01-10")], "Museum shelf."),
    ("HK-070", "Sony Alpha 7 V", "52278", [("Amara Osei", "2025-12-01", "present")], ""),
]

WORKSTATIONS_NOTE = ("Ingest workstations are named by site and desk number (for example CPH-WS-05 is the colour-bench station). "
                     "Every ingest stamps the workstation name into the file's edit history.")

# ----------------------------------------------------------------------------------------------- NEWS
NEWS = [
    dict(slug="2010-03-harbour-pair", date="2010-03-15", author="Teodor Vane", title="Archive note: the harbour pair",
         images=["HIL-1012", "HIL-1013"],
         body=["Our spring newsletter features a comparison we are rather proud of: the same winter quay, photographed the same "
               "afternoon with a layered-sensor compact and a conventional Bayer DSLR.",
               "The compact resolves the rigging of the tall ship with almost unsettling crispness; the DSLR wins on colour in the "
               "shadows. Neither wins on battery life. Both frames are now part of Archive Zero."]),
    dict(slug="2014-06-inside-passage", date="2014-06-30", author="Felix Brandauer", title="Notes from the Inside Passage",
         images=["HIL-1104"],
         body=["Three days on a coastal ferry, one wide zoom and more haze than a lens designer would like. Fjord walls make a superb "
               "flare test: bright sky, dark rock and a lot of reflected light from the water.",
               "The GPS receiver stayed on throughout, which made the later write-up much easier."]),
    dict(slug="2015-09-florence-lab", date="2015-09-14", author="Lucia Ferrante", title="The Florence Mobile Imaging Lab is open",
         images=["HIL-1201", "HIL-1214"],
         body=["Today we open our second lab, in Florence, dedicated to smartphones and tablets. Our first study, the Smartphone Field "
               "Panel, is already under way: one scene, many handsets, auto mode only.",
               "Summer field days in the Mugello hills gave us our first reference sets, including a four-handset rail walk on 22 August."]),
    dict(slug="2016-05-boulder", date="2016-05-02", author="Dana Whitlock", title="Hello from Boulder",
         images=[],
         body=["Halvane now has a team in Boulder, Colorado, focused on aerial and action systems. We start with one quadcopter, one "
               "borrowed garage and one very loud vibration rig."]),
    dict(slug="2017-02-texture-week-winner", date="2017-02-01", author="Grace Adeyemi", title="Texture Week 2017: the winner",
         images=["HIL-1325"],
         body=["Thank you to everyone who sent entries to Texture Week. The judges' choice is 'Paint memory', a close study of "
               "flaking paint on a weathered rail, credited to reader M. H. Grey.",
               "As always, entries were judged blind from the files alone. The winner receives a year of bench reports and our "
               "eternal admiration."]),
    dict(slug="2017-04-vintage-sensors", date="2017-04-24", author="Teodor Vane", title="Vintage sensors: a 2001 pro body goes to town",
         images=["HIL-1510"],
         body=["I took a 6-megapixel professional body from 2001 off the museum shelf for a long weekend city trip. It is heavy, slow "
               "and wonderful. The file records no location at all, so you will have to take my word for where I was - or work it "
               "out from the skyline."]),
    dict(slug="2019-10-nordhavn", date="2019-10-01", author="Grace Adeyemi", title="New studio, new ingest desk",
         images=["HIL-1124"],
         body=["We have moved into our new Nordhavn studio. The move also brings Ingest 3.0: every file now passes through a named "
               "ingest workstation, and the workstation name is stamped into the file's edit history.",
               "Workstations are numbered by desk. CPH-WS-02 sits with the field engineers, CPH-WS-05 is the colour bench, and "
               "CPH-WS-17, by the window, is the general ingest desk used for archive work and by our interns."]),
    dict(slug="2020-06-signage-walk", date="2020-06-02", author="Owen Achterberg", title="Signage and texture walk near the Boulder office",
         images=["HIL-1501", "HIL-1503", "HIL-1504", "HIL-1502"],
         body=["A short HEIC test on a May evening walk near the Boulder office: a no-pets sign against glass, herringbone pavers "
               "and a little free library.",
               "Curiously, one of these files came back to us from a partner portal with a location attached that none of us recognise. "
               "We have published it alongside the original upload."]),
    dict(slug="2021-03-provenance", date="2021-03-15", author="Amara Osei", title="Introducing Provenance & Metadata Assurance",
         images=[],
         body=["Halvane has spent eighteen years reading the metadata cameras leave behind. Today we are making it a service: "
               "independent audits of capture time, device, location and edit history for newsrooms, insurers and legal teams.",
               "Our first principle: a file's fields should agree with each other, with the device that made them and with the scene "
               "in the frame. When they do not, there is a story - and we find it."]),
    dict(slug="2021-10-rugged-tour", date="2021-10-04", author="Felix Brandauer", title="Autumn rugged-kit tour 2021",
         images=["HIL-1411", "HIL-1413"],
         body=["Leg one: a sub-250 g drone over a lake squeezed between a motorway and farmland in Occitanie. Leg two, six days later: "
               "an action camera at ground level among the steel and brick of the Ruhr's industrial heritage.",
               "Both files carry full positioning data - see if you can retrace the route."]),
    dict(slug="2022-09-garda", date="2022-09-20", author="Felix Brandauer", title="Phone HDR above a long alpine lake",
         images=["HIL-1118"],
         body=["A bright late-summer morning, a car park above a long lake and a phone that refuses to clip the sky. Phone RAW has come "
               "a long way since our first panel."]),
    dict(slug="2024-06-intern-ida", date="2024-06-10", author="Grace Adeyemi", title="Meet Ida, our 2024 summer intern",
         images=[],
         body=["Ida Holm joins us for the summer on the general ingest desk (CPH-WS-17), back-filling our legacy compacts into the archive."]),
    dict(slug="2025-05-tidemark-field-week", date="2025-05-12", author="Jonas Ekdahl", title="TIDEMARK-25 field week complete",
         images=["HIL-2501"],
         body=["Five days, two federal states, one tele-equipped drone and a new full-frame body. The TIDEMARK-25 field week ran from "
               "Monday 5 to Friday 9 May across Thuringia and northern Hesse.",
               "Files were ingested this morning on the field desk. Report v1 is due to Fellstrand Mutual at the end of the month."]),
    dict(slug="2025-06-welcome-tomas", date="2025-06-02", author="Grace Adeyemi", title="Welcome, Tomas!",
         images=[],
         body=["Tomas Varga joins us today as our 2025 summer intern. He will sit at the general ingest desk (CPH-WS-17), supporting "
               "archive digitisation and report production.",
               "Tomas has also been issued a loaner body from the Copenhagen store so he can learn our RAW workflow from capture to ingest."]),
    dict(slug="2025-06-lisbon", date="2025-06-12", author="Rosa Quintero", title="See us in Lisbon, 16-19 June",
         images=[],
         body=["Jonas Ekdahl and Amara Osei will represent Halvane at the European Imaging Assurance Forum in Lisbon from Monday 16 to "
               "Thursday 19 June. Jonas speaks on rugged-kit documentation for insurers; Amara runs a workshop on capture-time verification.",
               "Both fly back on Friday 20 June."]),
    dict(slug="2025-06-tidemark-v2", date="2025-06-20", author="Rosa Quintero", title="TIDEMARK-25 report v2 delivered",
         images=["HIL-2503", "HIL-2504"],
         body=["Report v2 for Fellstrand Mutual went out today. It adds five figures (3 to 7) to cover days 1, 3, 4 and 5 of the May "
               "field week, which were thin in v1.",
               "Thank you to everyone in Copenhagen who helped assemble the figures while the field team was in Lisbon."]),
    dict(slug="2025-06-ingest-41", date="2025-06-24", author="Grace Adeyemi", title="Ingest 4.1 is live",
         images=[],
         body=["Ingest 4.1 rolled out to all Copenhagen workstations in mid-June. It is faster, handles more RAW formats and still "
               "stamps every save into the edit history with the workstation name."]),
    dict(slug="2025-10-tidemark-statement", date="2025-10-28", author="Maren Halvik", title="Statement on the TIDEMARK-25 imagery review",
         images=[],
         body=["Fellstrand Mutual has raised questions about some figures in our TIDEMARK-25 report v2. We take this seriously.",
               "We have opened an internal review and, in the interest of transparency, published every report figure unchanged on the "
               "TIDEMARK-25 project page, together with our Field Kit Library records. We invite anyone to check our work.",
               "We will publish our conclusions when the review is complete."]),
    dict(slug="2025-12-year-end", date="2025-12-19", author="Maren Halvik", title="Thank you, and see you in 2026",
         images=["HIL-1511"],
         body=["A difficult autumn, a grey December walk on our year-end trip and a team I am proud of. Thank you to every client who "
               "trusted us this year - and to everyone who checked our work."]),
    dict(slug="2026-03-kit-library", date="2026-03-03", author="Grace Adeyemi", title="The Field Kit Library is now public",
         images=[],
         body=["As promised in October, our Field Kit Library register is now public: every body that appears in published work, the "
               "last characters of its serial number and who held it when.",
               "Serials are shown as recorded at check-in; where a body exposes only an internal serial in its files, that is what we list."]),
]

CAREERS = [
    dict(title="Field Engineer, Aerial Systems", office="Boulder, Colorado", type="Full-time",
         text="Plan and fly evaluation sorties, maintain the vibration rig and write reports our clients can check line by line. "
              "Part 107 certification (or willingness to obtain it) required."),
    dict(title="Metadata Assurance Analyst", office="Copenhagen", type="Full-time",
         text="Audit capture times, device attribution and edit histories for newsroom and insurance clients. You will be comfortable "
              "with ExifTool, timezones and saying 'I do not know yet'."),
    dict(title="Imaging Intern, summer 2026", office="Copenhagen", type="Internship, 12 weeks",
         text="Join the general ingest desk, learn our RAW workflow end to end and help digitise the museum shelf."),
]
