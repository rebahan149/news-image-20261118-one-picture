# Repair + gate-fit for the entrant's own 18 November front page.
#
# The entrant's generated page (assets/source-frontpage.png, 1024x1536)
# is clean in its panels, but its "31 MORE STORIES" box pads the count:
# about a third of the items repeat a panel story or are vague filler
# (Putin-Xi bilateral = panel 3, ASEAN maritime / tourism = panel 6,
# cyclone preparedness + Bay of Bengal tracking = panel 7, Canada alert
# timing = panel 9, Shenzhen APEC forum = panel 3, CSK plans = panel 8).
# This script redraws that box with distinct, verified stories from the
# day's record (the same record behind our "Daily Compass" entry):
# Nvidia's $115.8bn quarter, the EU's €45bn Ukraine loan, the Knesset
# Kahana bill, RAYE's 11 Grammy nods, the 178-company cyberattack,
# Waymo's freeway ban, Earthshot in Mumbai and more — then fits the page
# to the competition gate (<=1024x1024 px, <=1 MiB PNG).
from PIL import Image, ImageDraw, ImageFont
from collections import Counter
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, 'assets', 'source-frontpage.png')

im = Image.open(SRC).convert('RGB')
d = ImageDraw.Draw(im)
INK = (30, 27, 24)
BADGE_RED = (197, 40, 32)

def serif(size, bold=True):
    return ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSerif-%s.ttf' % ('Bold' if bold else 'Regular'), size)
def sans(size):
    return ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf', size)

# paper colour = mode of the ALSO interior in the original
region = im.crop((440, 1150, 1010, 1450)).resize((120, 120))
PAPER = Counter(region.getdata()).most_common(1)[0][0]
print('PAPER', PAPER)

# the ALSO header bar (dark navy) ends at y~1065 and the original first
# item line sits at y~1070; the box interior ends at y~1476, above the
# footer line. Cover exactly that interior.
TOP = 1066
d.rectangle((434, TOP, 1014, 1476), fill=PAPER)

LEFT = [
    "SpiceJet cancellations at Mumbai",
    "Delhi Police weighs reel-makers",
    "India's SAF plant at Panipat ready",
    "IIT Delhi in QS sustainability ranks",
    "Uttarakhand bus crash kills many",
    "India re-elected to ITU Council",
    "India joins anti-scam pledge",
    "Nvidia posts $115.8bn in revenue",
    "China–Canada tariff talks resume",
    "UK sanctions on West Bank settlers",
    "EU agrees €45bn loan for Ukraine",
    "US–Philippines defence ties",
    "Estonia closes border with Russia",
    "US loses its measles status",
    "Knesset backs far-right Kahana bill",
    "RAYE leads Grammy nods with 11",
]
RIGHT = [
    "Cyberattack hits 178 big firms",
    "Guinea jails 224 in gold crackdown",
    "Haitians back Salvadoran troops",
    "Ecuador fishermen sue US over strikes",
    "Vance: Iran must cut enrichment",
    "India GDP growth seen at 7.5%",
    "California bans Waymo from freeways",
    "Earthshot Prize hosted in Mumbai",
    "Sachin Tendulkar donates bats",
    "Australia pay gap falls under 20%",
    "Northern Ireland reach top tier",
    "Caribbean fears EU citizenship curb",
    "Ofqual: tough penalties for cheats",
    "UK climate targets at risk on EVs",
    "New Orleans boat-crash recovery",
]

fn = sans(11)

def draw_fit(x, y, text, maxw, base=15):
    size = base
    while size > 12 and d.textlength(text, font=serif(size)) > maxw:
        size -= 1
    d.text((x, y), text, font=serif(size), fill=INK)

def draw_entry(num, text, bx, tx, top, maxw):
    cy = top + 8
    d.ellipse([bx - 10, cy - 10, bx + 10, cy + 10], fill=BADGE_RED)
    s = str(num)
    tw = d.textlength(s, font=fn)
    tb = d.textbbox((0, 0), s, font=fn)
    d.text((bx - tw / 2, cy - (tb[3] - tb[1]) / 2 - tb[1]), s, font=fn, fill=(255, 255, 255))
    draw_fit(tx, top, text, maxw)

first = 1070
for i, t in enumerate(LEFT):
    draw_entry(10 + i, t, 482, 500, first + i * 25, 248)
for i, t in enumerate(RIGHT):
    draw_entry(26 + i, t, 782, 800, first + i * 27, 212)

im.save(os.path.join(ROOT, 'patched-native.png'))

# gate fit: scale to height 1024, centre on a paper-coloured square
nh = 1024
nw = round(im.width * nh / im.height)
res = im.resize((nw, nh), Image.LANCZOS)
cv = Image.new('RGB', (1024, 1024), PAPER)
cv.paste(res, ((1024 - nw) // 2, 0))
cv.save(os.path.join(ROOT, 'entry.png'))
if os.path.getsize(os.path.join(ROOT, 'entry.png')) > 1048576:
    cv.quantize(colors=256, method=Image.MEDIANCUT).save(os.path.join(ROOT, 'entry.png'), optimize=True)
cv.save(os.path.join(ROOT, 'preview.jpg'), quality=88)
print('entry.png:', cv.size, os.path.getsize(os.path.join(ROOT, 'entry.png')), 'bytes')
