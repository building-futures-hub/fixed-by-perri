#!/usr/bin/env python3
"""Builds the Fixed by Perri static site into ./site (Cloudflare Pages ready)."""
import json, os, html
from pathlib import Path

ROOT = Path(__file__).parent / "site"
DOMAIN = "https://fixedbyperri.com"
BIZ = "Fixed by Perri"
PHONE = "(520) 954-5559"
TEL = "+15209545559"
EMAIL = "fixedbyperri@gmail.com"
YEAR = 2026

# ---------------------------------------------------------------- icons
I = {
 "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>',
 "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>',
 "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>',
 "home": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 10 9-7 9 7v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/></svg>',
 "tag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L2 12V2h10l8.6 8.6a2 2 0 0 1 0 2.8z"/><circle cx="7" cy="7" r="1.5"/></svg>',
 "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
 "wrench": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9z"/></svg>',
 "star": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/></svg>',
 "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
 "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>',
 # appliance icons
 "fridge": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="3" width="16" height="26" rx="2.5"/><path d="M8 13h16M12 7v3M12 17v4"/></svg>',
 "washer": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="3" width="22" height="26" rx="2.5"/><path d="M5 9h22"/><circle cx="16" cy="19" r="6"/><path d="M12.5 19.5c1.5 1 2.5-1 3.5 0s2 1 3.5 0"/><circle cx="9" cy="6" r=".6" fill="currentColor"/><circle cx="12" cy="6" r=".6" fill="currentColor"/></svg>',
 "dryer": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="3" width="22" height="26" rx="2.5"/><path d="M5 9h22"/><circle cx="16" cy="19" r="6"/><path d="M14 16.5c1 1-1 2 0 3s1 2 0 3M18 16.5c1 1-1 2 0 3s1 2 0 3"/><circle cx="22" cy="6" r="1.2"/></svg>',
 "dishwasher": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="3" width="22" height="26" rx="2.5"/><path d="M5 9h22M12 6h8"/><path d="M10 16h12M10 21h12"/><path d="M13 16v-2M16 16v-2M19 16v-2"/></svg>',
 "oven": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="3" width="22" height="26" rx="2.5"/><path d="M5 9h22"/><rect x="9" y="13" width="14" height="11" rx="1.5"/><circle cx="10" cy="6" r="1"/><circle cx="14" cy="6" r="1"/><circle cx="18" cy="6" r="1"/><circle cx="22" cy="6" r="1"/></svg>',
 "microwave": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="7" width="26" height="18" rx="2.5"/><rect x="6" y="10" width="15" height="12" rx="1.5"/><path d="M24.5 11h1M24.5 14h1M24.5 17h1M24.5 21h1"/></svg>',
}

def ic(name): return I[name]
def esc(s): return html.escape(s, quote=True)

# ---------------------------------------------------------------- data
AREAS = [
 {"slug":"florence","map":"Florence, AZ 85132","zoom":12,"name":"Florence","zips":["85132"],
  "intro":'Fixed by Perri is based in Florence, the Pinal County seat, so Florence homes are the shortest drive on the schedule. Perri repairs refrigerators, washers, dryers, dishwashers, ovens and ranges, and microwaves in homes across Florence, from the older streets near the historic downtown to newer communities like Anthem at Merrill Ranch.',
  "local":'Florence has a real mix of housing: older homes near the historic downtown and much newer construction in master-planned communities. That means a wide spread of appliance ages and types, from older mechanical models to newer appliances run by electronic control boards. Either way, Perri diagnoses the problem first and gives you the price before any work starts.',
  "communities":['Historic Downtown Florence', 'Anthem at Merrill Ranch'],
  "nearby":['coolidge', 'casa-grande']},
 {"slug":"coolidge","map":"Coolidge, AZ","zoom":13,"name":"Coolidge","zips":["85128"],
  "intro":"Fixed by Perri provides in-home appliance repair in Coolidge, the city just south of Perri's Florence base. Refrigerators, washers, dryers, dishwashers, ovens and ranges, and microwaves are all covered, with an upfront estimate before any work begins.",
  "local":'Coolidge sits in the farm country of central Pinal County, home to Casa Grande Ruins National Monument. Dust is a fact of life here, and dust is hard on appliances: it clogs dryer vents and coats refrigerator condenser coils, which makes both run hotter and work harder. Those are two of the first things worth checking when a dryer runs long or a fridge struggles to stay cold.',
  "communities":['Downtown Coolidge', 'Areas near Casa Grande Ruins National Monument'],
  "nearby":['florence', 'casa-grande']},
 {"slug":"casa-grande","map":"Casa Grande, AZ","zoom":12,"name":"Casa Grande","zips":["85122","85193","85194"],
  "intro":'Fixed by Perri provides in-home appliance repair in Casa Grande, the largest city in Pinal County, halfway between Phoenix and Tucson along I-10. Perri repairs refrigerators, washers, dryers, dishwashers, ovens and ranges, and microwaves, and gives you the price before any work begins.',
  "local":'Casa Grande has grown quickly, and a large share of its homes were built in the last twenty years, so many builder-installed appliances are now reaching the age when parts like drain pumps, igniters, door gaskets and control boards start to wear out. The city also has a lot of manufactured homes, which often use different appliance sizes and mounting than site-built houses, so it helps to mention your home type when you request service.',
  "communities":['Mission Royale', 'Villago', 'Central Casa Grande'],
  "nearby":['coolidge', 'maricopa']},
 {"slug":"maricopa","map":"Maricopa, AZ 85138","zoom":12,"name":"Maricopa","zips":["85138","85139"],
  "intro":'Fixed by Perri repairs household appliances in the City of Maricopa, which is in Pinal County, not to be confused with Maricopa County. If your refrigerator, washer, dryer, dishwasher, oven, range or microwave is acting up, Perri will come to you, diagnose it, and tell you the cost before he starts.',
  "local":"Most of Maricopa's neighborhoods were built from the early 2000s on, which puts a lot of its appliances in the 7-to-15-year window when the first major repairs show up. At that age a repair often makes more financial sense than a replacement, and you'll have the diagnosis and the price in hand to decide.",
  "communities":['Rancho El Dorado', 'Province', 'Glennwilde', 'Tortosa', 'Senita'],
  "nearby":['casa-grande', 'florence']},
]
AREA = {a["slug"]: a for a in AREAS}

BRANDS = ["Samsung","LG","Whirlpool","GE","Bosch"]

SERVICES = [
 {"slug":"refrigerator-repair","noun":"Refrigerator","name":"Refrigerator Repair","short":"Refrigerators","icon":"fridge",
  "blurb":"Not cooling, leaking, frosting up, or the ice maker quit. We repair fridges and freezers of all styles.",
  "h1":"Refrigerator & Freezer Repair",
  "intro":"When the fridge stops cooling, the clock starts ticking on everything inside it. Fixed by Perri repairs refrigerators and freezers in Florence, Coolidge, Casa Grande and Maricopa: French-door, side-by-side, top- and bottom-freezer models, standalone freezers, and the spare fridge in the garage.",
  "problems":["Fridge or freezer not cooling","Freezer cold but fridge section warm","Ice maker not making ice","Water dispenser not working","Water leaking on the floor or inside","Frost or ice building up","Running constantly or cycling too often","Loud buzzing, clicking or fan noise"],
  "checks":["Make sure the temperature dial or setting didn't get bumped.","Check that the doors close and seal, and that food isn't blocking the vents inside.","Confirm the outlet has power and the breaker hasn't tripped.","If you can reach the condenser coils (bottom front or back), unplug the fridge and vacuum the dust off.","For ice and water problems, make sure the water supply valve behind the fridge is fully open."],
  "warn":None,
  "az":("Arizona heat and hard water","Garage refrigerators work extremely hard in a Pinal County summer, and many units aren't built for a 110°F garage. Dust-covered condenser coils make it worse. Central Arizona's hard water also clogs water filters and inlet valves, which is a common cause of slow or failed ice makers."),
  "faq":[("Is my refrigerator worth repairing?","It depends on the age of the fridge and what's wrong with it. Perri will diagnose the problem and give you the repair price upfront, so you can compare it against replacement before you spend anything."),
         ("How long will my food stay safe while the fridge is down?","Per USDA guidance, a closed refrigerator keeps food safe for about 4 hours. A full freezer holds for about 48 hours (24 if half full) if you keep the door shut. Coolers with ice buy you more time."),
         ("Do you fix ice makers and water dispensers?","Yes. Ice makers, water inlet valves, dispensers and water lines are some of the most common refrigerator repairs we do.")]},
 {"slug":"washer-repair","noun":"Washer","name":"Washer Repair","short":"Washers","icon":"washer",
  "blurb":"Won't drain, won't spin, leaking, or walking across the floor. Front-load and top-load washers.",
  "h1":"Washing Machine Repair",
  "intro":"A broken washer backs up the whole house fast. Fixed by Perri repairs front-load and top-load washing machines in Florence, Coolidge, Casa Grande and Maricopa, including washers that won't drain, won't spin, leak, or shake like they're about to take off.",
  "problems":["Won't drain or leaves standing water","Won't spin or clothes come out soaking","Leaking from the bottom or door","Loud banging, grinding or shaking","Won't start or door won't lock","Won't fill or fills very slowly","Error codes on the display","Musty smell in a front-loader"],
  "checks":["Check the drain hose for kinks, especially if the washer was recently moved.","Front-loaders have a drain pump filter (coin trap) behind a small panel at the bottom front. A sock or coin there is a common cause of drain problems.","For shaking, make sure the load is balanced and the washer sits level on all four feet.","For fill problems, confirm both water valves behind the washer are fully open."],
  "warn":None,
  "az":("Hard water is hard on washers","Mineral scale from central Arizona's hard water builds up in inlet screens, valves and heating parts over time. If your washer fills slowly or you see white residue, scale is a likely suspect."),
  "faq":[("Should I repair or replace my washer?","Many washer problems (drain pumps, lid switches, door locks, belts, inlet valves) are very fixable. You'll get the diagnosis and price before work starts, so you can decide."),
         ("Do you work on front-load and top-load washers?","Yes, both, from most major brands including Samsung, LG, Whirlpool, GE and Bosch."),
         ("Why does my front-load washer smell?","Moisture trapped in the door gasket and drain area grows mildew. Wiping the gasket, leaving the door cracked between loads, and using HE detergent help. If the smell persists, the drain filter or pump may need attention.")]},
 {"slug":"dryer-repair","noun":"Dryer","name":"Dryer Repair","short":"Dryers","icon":"dryer",
  "blurb":"No heat, takes forever, won't tumble, or squealing. Gas and electric dryers.",
  "h1":"Dryer Repair",
  "intro":"When the dryer stops heating, laundry piles up fast. Fixed by Perri repairs gas and electric dryers in Florence, Coolidge, Casa Grande and Maricopa, from no-heat problems to broken belts, noisy drums and dryers that shut off early.",
  "problems":["Dryer runs but doesn't heat","Clothes take two or more cycles to dry","Won't start or drum won't turn","Squeaking, thumping or grinding","Shuts off before clothes are dry","Overheating or too hot to the touch","Gas and electric models"],
  "checks":["Clean the lint screen. A clogged screen alone can double drying time.","Check the vent hose behind the dryer for crushing or kinks, and make sure the outside vent flap opens when the dryer runs.","Electric dryers use a double breaker. If one half trips, the drum can spin with no heat, so check the panel."],
  "warn":("Burning smell? Stop the dryer.","If you smell burning or the dryer is unusually hot, turn it off and unplug it. Lint buildup in the vent is a leading cause of home dryer fires. Don't keep running it while you wait for a repair."),
  "az":("Dust and long vent runs","Desert dust and monsoon storms add to lint buildup, and many Arizona homes vent dryers up through the roof with long runs. Restricted airflow is one of the most common reasons a dryer takes forever or overheats."),
  "faq":[("Why does my dryer run but not heat?","Common causes are a failed heating element or thermal fuse on electric dryers, a bad igniter or gas valve coils on gas dryers, or a half-tripped breaker. Perri will find the actual cause before replacing anything."),
         ("Do you repair gas dryers?","Yes, both gas and electric dryers."),
         ("Can a clogged vent damage my dryer?","Yes. Restricted airflow makes the dryer run hot, which can blow thermal fuses and wear out heating parts early. It's also a fire risk.")]},
 {"slug":"dishwasher-repair","noun":"Dishwasher","name":"Dishwasher Repair","short":"Dishwashers","icon":"dishwasher",
  "blurb":"Not draining, not cleaning, leaking, or won't start. Built-in dishwashers from major brands.",
  "h1":"Dishwasher Repair",
  "intro":"Fixed by Perri repairs built-in dishwashers in Florence, Coolidge, Casa Grande and Maricopa, whether it won't drain, leaves dishes dirty or spotty, leaks onto the floor, or won't start at all.",
  "problems":["Water left in the bottom after a cycle","Dishes still dirty or gritty","Cloudy film or spots on glasses","Leaking under the door or onto the floor","Won't start or stops mid-cycle","Not drying","Grinding, humming or loud noises","Door latch problems"],
  "checks":["Pull out and rinse the filter in the bottom of the tub. A clogged filter is a top cause of poor cleaning and slow draining.","If you just installed a new garbage disposal, the knockout plug in the disposal's dishwasher inlet may never have been removed.","Run the kitchen faucet until it's hot before starting a cycle.","Check the spray arm holes for food or mineral buildup."],
  "warn":None,
  "az":("Hard water and dishwashers","That white film on your glasses is usually hard water minerals. Rinse aid helps, but over time scale also builds up in spray arms, valves and heating parts, which can cause poor cleaning and drain problems."),
  "faq":[("Why won't my dishwasher drain?","Usually a clogged filter, a blocked drain hose or air gap, a disposal issue, or a failing drain pump. Perri checks the simple causes first."),
         ("Is a leaking dishwasher urgent?","A slow leak can damage cabinets and subfloor without being obvious. If you see water, stop using it and turn off the water supply under the sink until it's checked."),
         ("Which dishwasher brands do you repair?","Most major brands, including Bosch, Samsung, LG, Whirlpool and GE.")]},
 {"slug":"oven-range-repair","noun":"Oven & range","name":"Oven & Range Repair","short":"Ovens & Ranges","icon":"oven",
  "blurb":"Won't heat, burner won't light, uneven baking. Gas and electric ranges, cooktops and wall ovens.",
  "h1":"Oven, Range & Cooktop Repair",
  "intro":"Fixed by Perri repairs gas and electric ranges, wall ovens and cooktops in Florence, Coolidge, Casa Grande and Maricopa: ovens that won't heat or bake unevenly, burners that won't light, and controls that won't respond.",
  "problems":["Oven won't heat or heats slowly","Uneven baking or wrong temperature","Gas burner won't light or keeps clicking","Electric burner or element not heating","Control panel or clock not responding","Self-clean problems","Door won't close or seal properly","Gas and electric models"],
  "checks":["On a gas cooktop, make sure each burner cap is seated correctly and completely dry after cleaning.","Check the breaker. Electric ranges run on a double breaker, and half can trip.","If the display shows an error code, write it down. It helps speed up the diagnosis."],
  "warn":("Smell gas? Leave first, call second.","Don't use light switches, the stove or your phone inside. Get everyone out of the house, then call your gas utility or 911 from outside. Call us once the gas company has made it safe."),
  "az":None,
  "faq":[("Do you repair gas ranges?","Yes. We repair both gas and electric ranges, cooktops and wall ovens."),
         ("My oven temperature seems off. Can that be fixed?","Often, yes. A failing temperature sensor, bake or broil element, or igniter can cause slow or uneven heating. We'll test and confirm the cause."),
         ("Is it safe to use my oven while it's acting up?","If you smell gas, see sparking, or the oven won't shut off, stop using it and call. For slow heating or uneven baking, it's usually safe to use carefully until the repair.")]},
 {"slug":"microwave-repair","noun":"Microwave","name":"Microwave Repair","short":"Microwaves","icon":"microwave",
  "blurb":"Not heating, sparking, dead display, or turntable stuck. Over-the-range and built-in models.",
  "h1":"Microwave Repair",
  "intro":"Fixed by Perri repairs over-the-range and built-in microwaves in Florence, Coolidge, Casa Grande and Maricopa, including ones that run but don't heat, spark, have a dead display, or won't spin.",
  "problems":["Runs but doesn't heat food","Sparking or arcing inside","No power or dead display","Turntable not spinning","Buttons or keypad not responding","Light or vent fan not working","Door won't latch or start"],
  "checks":["Check the breaker and outlet first.","Make sure the turntable and its roller ring are seated correctly.","Never run a microwave empty, and remove any metal, foil or twist ties."],
  "warn":("Don't open the case yourself.","Microwaves store dangerous high voltage in internal parts even when unplugged. If it's sparking or smells burnt, unplug it and leave the repair to a technician."),
  "az":None,
  "faq":[("Is it worth fixing a microwave?","Over-the-range and built-in microwaves are often worth repairing because replacement means installation work too. A small countertop microwave is usually cheaper to replace, and we'll tell you honestly if that's the case."),
         ("Why is my microwave sparking?","Usually metal in the cavity, food splatter, or a damaged waveguide cover. Stop using it until it's checked."),
         ("Do you repair over-the-range microwaves?","Yes, over-the-range and built-in models from most major brands.")]},
]
SVC = {s["slug"]: s for s in SERVICES}

# ---------------------------------------------------------------- schema
def biz_schema():
    return {
     "@context":"https://schema.org","@type":"HomeAndConstructionBusiness","@id":DOMAIN+"/#business",
     "name":BIZ,"url":DOMAIN+"/","telephone":"+1-520-954-5559","email":EMAIL,
     "logo":DOMAIN+"/img/logo.png","image":[DOMAIN+"/img/perri-kitchen.jpg",DOMAIN+"/img/og-cover.jpg"],
     "description":"Locally owned in-home appliance repair in Pinal County, Arizona, serving Florence, Coolidge, Casa Grande and Maricopa. Refrigerator, washer, dryer, dishwasher, oven, range and microwave repair.",
     "address":{"@type":"PostalAddress","addressLocality":"Florence","addressRegion":"AZ","postalCode":"85132","addressCountry":"US"},
     "areaServed":[{"@type":"City","name":f"{a['name']}, AZ"} for a in AREAS],
     "founder":{"@type":"Person","name":"Perri","jobTitle":"Owner"},
     "knowsAbout":[s["name"] for s in SERVICES],
     "hasOfferCatalog":{"@type":"OfferCatalog","name":"Appliance repair services","itemListElement":[
        {"@type":"Offer","itemOffered":{"@type":"Service","name":s["name"],"url":f"{DOMAIN}/services/{s['slug']}/"}} for s in SERVICES]},
    }

def crumbs_schema(trail):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":i+1,"name":n,"item":DOMAIN+u} for i,(n,u) in enumerate(trail)]}

def faq_schema(faqs):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}

def ld(*objs):
    return "\n".join(f'<script type="application/ld+json">{json.dumps(o,ensure_ascii=False)}</script>' for o in objs)

# ---------------------------------------------------------------- chrome
RIDGE = '''<svg class="ridge" viewBox="0 0 1440 110" preserveAspectRatio="none" aria-hidden="true">
<path d="M0 110V78l90-22 70 14 110-46 80 30 60-18 120 52 90-36 70 20 130-58 90 40 70-16 110 46 90-30 80 24 120-40 60 18v66z" fill="#E7C9A4"/>
<path d="M0 110V92l120-14 100 10 140-30 120 26 90-12 150 22 110-18 130 16 120-26 110 20 100-8 150 14v40z" fill="{fill}"/></svg>'''

def ridge(fill="#FBF5EC"): return RIDGE.replace("{fill}", fill)

def header(active):
    svc_links = "".join(f'<a href="/services/{s["slug"]}/">{s["name"]}</a>' for s in SERVICES)
    area_links = "".join(f'<a href="/service-areas/{a["slug"]}/">{a["name"]}</a>' for a in AREAS)
    def cur(k): return ' aria-current="page"' if active==k else ''
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap"><span>Locally owned appliance repair in <span class="hide-sm">Florence, Coolidge, Casa Grande, Maricopa &amp; </span>Pinal County, AZ</span><a href="tel:{TEL}">Call {PHONE}</a></div></div>
<header class="site-header"><div class="wrap">
 <a class="brand" href="/"><img src="/img/logo-180.png" alt="Fixed by Perri logo" width="54" height="54"><span><b>Fixed by Perri</b><small>Appliance Repair</small></span></a>
 <nav class="nav" id="nav" aria-label="Main">
  <a href="/"{cur("home")}>Home</a>
  <div class="dd"><button type="button" aria-haspopup="true">Services ▾</button><div class="dd-menu"><a href="/services/"><b>All services</b></a><hr>{svc_links}</div></div>
  <div class="dd"><button type="button" aria-haspopup="true">Service Areas ▾</button><div class="dd-menu"><a href="/service-areas/"><b>All areas</b></a><hr>{area_links}</div></div>
  <a href="/about/"{cur("about")}>About Perri</a>
  <a href="/contact/"{cur("contact")}>Contact</a>
 </nav>
 <a class="btn btn-primary header-call" href="tel:{TEL}">{ic("phone")}{PHONE}</a>
 <button class="menu-toggle" type="button" aria-controls="nav" aria-expanded="false">Menu</button>
</div></header>'''

def footer():
    sv = "".join(f'<li><a href="/services/{s["slug"]}/">{s["name"]}</a></li>' for s in SERVICES)
    ar = "".join(f'<li><a href="/service-areas/{a["slug"]}/">{a["name"]}, AZ</a></li>' for a in AREAS)
    return f'''<footer class="site-footer"><div class="wrap">
 <div class="foot-grid">
  <div><div class="foot-brand"><img src="/img/logo-180.png" alt="" width="64" height="64"><b>Fixed by Perri</b></div>
   <p>Locally owned and operated in-home appliance repair, based in Florence and serving Coolidge, Casa Grande and Maricopa in Pinal County.</p>
   <p><a class="foot-call" href="tel:{TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
  <div><h4>Services</h4><ul>{sv}</ul></div>
  <div><h4>Service Areas</h4><ul>{ar}</ul></div>
  <div><h4>Company</h4><ul><li><a href="/about/">About Perri</a></li><li><a href="/contact/">Request Service</a></li><li><a href="/services/">All Services</a></li><li><a href="/privacy/">Privacy Policy</a></li></ul></div>
 </div>
 <div class="foot-bottom"><span>© {YEAR} Fixed by Perri. All rights reserved.</span><span>Website by <a href="https://buildingfuturesai.com">Building Futures AI</a></span></div>
</div></footer>
<div class="callbar"><a href="tel:{TEL}">{ic("phone")}Call Perri</a><a href="/contact/">{ic("chat")}Request Service</a></div>
<script src="/js/site.js" defer></script>'''

def page(path, title, desc, body, active="", schema=()):
    canonical = DOMAIN + path
    doc = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Fixed by Perri">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}"><meta property="og:image" content="{DOMAIN}/img/og-cover.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="675"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#2A1C14">
<link rel="icon" type="image/png" href="/img/favicon.png"><link rel="apple-touch-icon" href="/img/logo-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Public+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/site.css">
{ld(biz_schema(), *schema)}
</head><body>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
</body></html>'''
    out = ROOT / path.strip("/") / "index.html" if path.endswith("/") else ROOT / path.lstrip("/")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc)
    return path

# ---------------------------------------------------------------- blocks
from urllib.parse import quote_plus
def gmap(query, zoom, title):
    return f'<iframe class="map" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="{esc(title)}" src="https://www.google.com/maps?q={quote_plus(query)}&z={zoom}&output=embed"></iframe>'
GENERAL_MAP = lambda: gmap("Pinal County, AZ", 9, "Fixed by Perri service area: Florence, Coolidge, Casa Grande and Maricopa, AZ")

def faq_block(faqs, heading="Common questions"):
    items = "".join(f'<details><summary>{esc(q)}</summary><div><p>{esc(a)}</p></div></details>' for q,a in faqs)
    return f'<h2>{heading}</h2><div class="faq">{items}</div>'

def cta(h="Appliance acting up? Let's get it fixed.", p="Call Perri directly, or send a request and we'll get back to you to schedule."):
    return f'''<section class="cta"><div class="wrap"><div><h2>{h}</h2><p>{p}</p></div>
<div class="btns"><a class="btn btn-light" href="tel:{TEL}">{ic("phone")}{PHONE}</a><a class="btn btn-ghost" href="/contact/">Request service {ic("arrow")}</a></div></div></section>'''

def service_cards():
    return '<div class="cards">' + "".join(
        f'<a class="card" href="/services/{s["slug"]}/"><span class="ico">{ic(s["icon"])}</span><h3>{s["name"]}</h3><p>{s["blurb"]}</p><span class="more">Learn more →</span></a>'
        for s in SERVICES) + '</div>'

def area_tiles(exclude=None):
    return '<div class="areas">' + "".join(
        f'<a class="area" href="/service-areas/{a["slug"]}/"><div>{a["name"]}<span>{", ".join(a["zips"])}</span></div>→</a>'
        for a in AREAS if a["slug"]!=exclude) + '</div>'

def callcard(h="Need it fixed?", p="Talk to Perri directly. You'll get an upfront estimate before any work starts."):
    return f'<div class="callcard"><h3>{h}</h3><p>{p}</p><a class="btn btn-primary" href="tel:{TEL}">{ic("phone")}{PHONE}</a><a class="btn btn-light" href="/contact/">Request service online</a></div>'

def page_hero(crumbs, eyebrow, h1, lede, side=None, dark=False):
    cr = " / ".join(f'<a href="{u}">{esc(n)}</a>' if i < len(crumbs)-1 else esc(n) for i,(n,u) in enumerate(crumbs))
    side = side if side is not None else callcard()
    cls = "page-hero hero-dark" if dark else "page-hero"
    return f'''<section class="{cls}"><div class="wrap"><div class="grid"><div>
<nav class="crumbs" aria-label="Breadcrumb">{cr}</nav><span class="eyebrow">{eyebrow}</span><h1>{h1}</h1><p class="lede">{lede}</p></div>
<div>{side}</div></div></div>{ridge()}</section>'''

STRIP = f'''<div class="strip"><div class="wrap"><ul>
<li>{ic("home")}<div><b>Locally owned</b>Based in Florence, serving Pinal County</div></li>
<li>{ic("tag")}<div><b>Upfront estimates</b>You know the price before work starts</div></li>
<li>{ic("clock")}<div><b>Prompt scheduling</b>Same-day or next-day when available</div></li>
<li>{ic("wrench")}<div><b>Major brands</b>Samsung, LG, Whirlpool, GE, Bosch &amp; more</div></li>
</ul></div></div>'''

STEPS = '''<div class="steps">
<div class="step"><h3>Tell us what's wrong</h3><p>Call or send the request form with your appliance type, brand and what it's doing.</p></div>
<div class="step"><h3>Get a time &amp; upfront estimate</h3><p>We'll set an appointment window. Perri diagnoses the problem and gives you the price before any work starts.</p></div>
<div class="step"><h3>Get it fixed</h3><p>Perri completes the repair, tests the appliance, and shares tips to help keep it running.</p></div>
</div>'''

def form(source="contact"):
    opts = "".join(f"<option>{s['short']}</option>" for s in SERVICES)
    cities = "".join(f"<option>{a['name']}</option>" for a in AREAS)
    return f'''<form class="form-card" id="lead-form" action="/api/lead" method="post" novalidate>
<input type="hidden" name="source" value="{source}">
<div class="hp" aria-hidden="true"><label>Leave blank<input name="company_website" tabindex="-1" autocomplete="off"></label></div>
<div class="form-grid">
 <div><label for="f-first">First name <span class="req">*</span></label><input id="f-first" name="first_name" autocomplete="given-name" required></div>
 <div><label for="f-last">Last name</label><input id="f-last" name="last_name" autocomplete="family-name"></div>
 <div><label for="f-phone">Phone <span class="req">*</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
 <div><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email"></div>
 <div><label for="f-appl">Appliance <span class="req">*</span></label><select id="f-appl" name="appliance" required><option value="">Choose one</option>{opts}<option>Other</option></select></div>
 <div><label for="f-brand">Brand</label><input id="f-brand" name="brand" placeholder="e.g. Samsung, Whirlpool"></div>
 <div class="full"><label for="f-addr">Street address</label><input id="f-addr" name="address" autocomplete="street-address"></div>
 <div><label for="f-city">City</label><select id="f-city" name="city"><option value="">Choose one</option>{cities}<option>Other / not sure</option></select></div>
 <div><label for="f-zip">ZIP</label><input id="f-zip" name="zip" inputmode="numeric" autocomplete="postal-code"></div>
 <div class="full"><label for="f-msg">What's it doing? <span class="req">*</span></label><textarea id="f-msg" name="message" required placeholder="e.g. Fridge isn't cooling, freezer is fine. Started yesterday."></textarea></div>
</div>
<button class="btn btn-primary" type="submit">Send service request {ic("arrow")}</button>
<p class="form-fine">By submitting, you agree Fixed by Perri may contact you about your request by phone, text or email. See our <a href="/privacy/">privacy policy</a>. In a hurry? Call <a href="tel:{TEL}">{PHONE}</a>.</p>
<div class="form-status" role="status" aria-live="polite"></div>
</form>'''

# ---------------------------------------------------------------- pages
pages = []

# HOME
home_faq = [
 ("What appliances does Fixed by Perri repair?","Refrigerators and freezers, washers, dryers, dishwashers, ovens, ranges and cooktops, and over-the-range and built-in microwaves."),
 ("What areas do you serve?","Florence, Coolidge, Casa Grande and Maricopa, Arizona. If you're nearby and not sure, give us a call."),
 ("Will I know the price before the repair?","Yes. Perri diagnoses the problem and gives you an upfront estimate before starting any work. No hidden fees or surprises."),
 ("Which brands do you work on?","Most major brands, including Samsung, LG, Whirlpool, GE and Bosch."),
 ("How soon can you come out?","We offer same-day or next-day appointments when the schedule allows. Call for the fastest answer."),
]
home = f'''<section class="hero hero-dark"><div class="wrap">
<div>
 <span class="eyebrow">Appliance repair · Pinal County, AZ</span>
 <h1>Broken appliance? <em>Perri</em> will fix it.</h1>
 <p class="lede">Fridges, washers, dryers, dishwashers, ovens and microwaves, repaired in your home by a local tech who gives you the price before he starts.</p>
 <div class="hero-ctas"><a class="btn btn-primary" href="tel:{TEL}">{ic("phone")}Call {PHONE}</a><a class="btn btn-ghost" href="/contact/">Request service online</a></div>
 <ul class="checks"><li>{ic("check")}Locally owned &amp; operated</li><li>{ic("check")}Upfront estimates</li><li>{ic("check")}Gas &amp; electric</li></ul>
</div>
<div class="hero-photo"><div class="sun"></div><img class="pic" src="/img/perri-kitchen.jpg" alt="Perri, owner of Fixed by Perri, in a customer's kitchen" width="900" height="868"><img class="badge" src="/img/logo.png" alt="Fixed by Perri Appliance Repair logo" width="400" height="400"></div>
</div>{ridge("#2A1C14")}</section>
{STRIP}
<section><div class="wrap">
 <div class="sec-head"><span class="eyebrow">What we fix</span><h2>In-home repair for the appliances you use every day</h2><p class="lede">Most major brands, gas and electric. Pick your appliance to see common problems and a few quick things you can check first.</p></div>
 {service_cards()}
</div></section>
<section class="band-white"><div class="wrap owner">
 <div class="owner-photo"><img src="/img/perri.jpg" alt="Perri, owner of Fixed by Perri" width="506" height="504" loading="lazy"><div class="tag">Perri<small>Owner &amp; repair tech</small></div></div>
 <div>
  <span class="eyebrow">Meet the owner</span>
  <h2>You'll know exactly who's coming to your door.</h2>
  <p class="lede">Fixed by Perri isn't a national dispatch service. It's Perri. He's lived in the Valley for the past 8 years, grew up as the 5th of 10 kids, and built his business on showing up prepared and treating people with respect.</p>
  <ul class="facts">
   <li>{ic("star")}<span>Won a state robotics innovation award for creative problem-solving and technical skill</span></li>
   <li>{ic("chat")}<span>Served a two-year church mission in the Carolinas, where he learned patience and clear communication</span></li>
   <li>{ic("tag")}<span>Honest recommendations: you get the diagnosis and the price before any work starts</span></li>
  </ul>
  <a class="btn btn-ghost" href="/about/">More about Perri {ic("arrow")}</a>
 </div>
</div></section>
<section class="band-ink"><div class="wrap">
 <div class="sec-head"><span class="eyebrow" style="color:var(--amber)">How it works</span><h2>Simple, upfront, and built around your schedule</h2></div>
 {STEPS}
</div></section>
<section><div class="wrap">
 <div class="sec-head"><span class="eyebrow">Service areas</span><h2>Serving homeowners across Pinal County</h2><p class="lede">Based in Florence and serving Coolidge, Casa Grande and Maricopa.</p></div>
 {area_tiles()}
</div></section>
<section class="band-white"><div class="wrap">{faq_block(home_faq, "Questions homeowners ask")}</div></section>
{cta()}'''
pages.append(page("/", "Appliance Repair in Pinal County, AZ | Fixed by Perri",
  "Locally owned in-home appliance repair in Florence, Coolidge, Casa Grande & Maricopa, AZ. Fridge, washer, dryer, dishwasher, oven & microwave repair. Call (520) 954-5559.",
  home, "home", (faq_schema(home_faq),)))

# ABOUT
about = page_hero([("Home","/"),("About Perri","/about/")], "About Fixed by Perri", "Hey, I'm Perri.",
  "Fixed by Perri is a locally owned appliance repair business based in Florence, Arizona. When you call, you're talking to the person who will actually show up and do the work.",
  side='<img class="about-photo" src="/img/perri.jpg" alt="Perri, owner of Fixed by Perri, smiling on a mountain overlook above the Valley" width="800" height="792">') + f'''
<section><div class="wrap content-grid"><div class="prose">
<h2>My story</h2>
<p>I've called the Valley home for the past 8 years, and in that time I've built a deep appreciation for hard work, community, and doing things the right way. As the 5th of 10 kids, I learned early on the value of responsibility, problem-solving, and teamwork. Those skills still guide me every day.</p>
<p>I also spent two years serving a mission for my church in the Carolinas. That experience strengthened my work ethic, my communication skills, and my commitment to serving others with patience and integrity.</p>
<p>My passion for understanding how things work started young and led me to win a state robotics innovation award, recognizing creative problem-solving and technical skill. That same curiosity is what I bring to every appliance I work on: figure out what's really wrong, explain it clearly, and fix it right.</p>
<p>Whether it's work, service, or life, I believe in showing up prepared, treating people with respect, and always striving to improve.</p>
<h2>What you can expect</h2>
<ul class="ticklist">
<li>{ic("check")}<span>A clear diagnosis, explained in plain English</span></li>
<li>{ic("check")}<span>An upfront estimate before any work starts</span></li>
<li>{ic("check")}<span>No hidden fees or surprises</span></li>
<li>{ic("check")}<span>Same-day or next-day appointments when available</span></li>
<li>{ic("check")}<span>Respect for your home and your time</span></li>
<li>{ic("check")}<span>Preventive maintenance tips to keep it running</span></li>
</ul>
</div>
<aside class="aside">{callcard("Ready to get it fixed?","Call Perri directly or send a quick request online.")}
<div class="box"><h3>Areas served</h3><ul>{"".join(f'<li><a href="/service-areas/{a["slug"]}/">{a["name"]}, AZ</a></li>' for a in AREAS)}</ul></div></aside>
</div></section>
{cta()}'''
pages.append(page("/about/", "About Perri | Fixed by Perri Appliance Repair, Florence AZ",
  "Meet Perri, owner of Fixed by Perri, a locally owned appliance repair business based in Florence, AZ serving Pinal County.",
  about, "about", (crumbs_schema([("Home","/"),("About","/about/")]),)))

# SERVICES HUB
hub = page_hero([("Home","/"),("Services","/services/")], "Our services", "Appliance repair services",
  "In-home repair for refrigerators, washers, dryers, dishwashers, ovens and ranges, and microwaves across Florence, Coolidge, Casa Grande and Maricopa.", dark=True) + f'''
<section><div class="wrap">{service_cards()}
<div class="note" style="margin-top:36px"><b>Brands we work on</b><p>Most major brands, including {", ".join(BRANDS[:-1])} and {BRANDS[-1]}, in both gas and electric models. Don't see your brand? Call and ask.</p></div>
</div></section>
<section class="band-white"><div class="wrap"><div class="sec-head"><span class="eyebrow">Where we work</span><h2>Serving Pinal County, Arizona</h2><p class="lede">In-home repair in Florence, Coolidge, Casa Grande and Maricopa.</p></div>{GENERAL_MAP()}<div style="margin-top:24px">{area_tiles()}</div></div></section>
<section class="band-ink"><div class="wrap"><div class="sec-head"><span class="eyebrow" style="color:var(--amber)">How it works</span><h2>From "it's broken" to fixed</h2></div>{STEPS}</div></section>
{cta()}'''
pages.append(page("/services/", "Appliance Repair Services | Fixed by Perri, Pinal County AZ",
  "Refrigerator, washer, dryer, dishwasher, oven & range, and microwave repair in Florence, Coolidge, Casa Grande and Maricopa, AZ.",
  hub, "", (crumbs_schema([("Home","/"),("Services","/services/")]),)))

# SERVICE PAGES
area_names = ", ".join(a["name"] for a in AREAS[:-1]) + " and " + AREAS[-1]["name"]
for s in SERVICES:
    path = f"/services/{s['slug']}/"
    probs = "".join(f'<li>{ic("check")}<span>{p}</span></li>' for p in s["problems"])
    checks = "".join(f"<li>{c}</li>" for c in s["checks"])
    warn = f'<div class="note warn"><b>{s["warn"][0]}</b><p>{s["warn"][1]}</p></div>' if s["warn"] else ""
    az = f'<h2>{s["az"][0]}</h2><p>{s["az"][1]}</p>' if s["az"] else ""
    others = "".join(f'<li><a href="/services/{o["slug"]}/">{o["name"]}</a></li>' for o in SERVICES if o["slug"]!=s["slug"])
    areas_li = "".join(f'<li><a href="/service-areas/{a["slug"]}/">{a["name"]}</a></li>' for a in AREAS)
    body = page_hero([("Home","/"),("Services","/services/"),(s["name"],path)], f"{s['name']} · Pinal County, AZ",
        f'{s["h1"]} in Pinal County, AZ', s["intro"], dark=True) + f'''
<section><div class="wrap content-grid"><div class="prose">
<h2>{s["noun"]} problems we fix</h2>
<ul class="ticklist">{probs}</ul>
{warn}
<h2>Quick checks before you call</h2>
<p>These take a few minutes and sometimes solve the problem. If they don't, you've ruled out the easy stuff, which helps the diagnosis.</p>
<ul>{checks}</ul>
{az}
<h2>Brands we repair</h2>
<ul class="chips">{"".join(f"<li>{b}</li>" for b in BRANDS)}<li>and more</li></ul>
<h2>How the repair works</h2>
<p>Call or <a href="/contact/">send a request</a> with your brand and what the appliance is doing. Perri will set an appointment window, diagnose the problem in your home, and give you the price before starting any work. You decide whether to go ahead.</p>
{faq_block(s["faq"])}
<h2>{s["name"]} near you</h2>
<p>Fixed by Perri provides {s["name"].lower()} in {area_names}, Arizona.</p>
<ul class="chips">{"".join(f'<li><a href="/service-areas/{a["slug"]}/">{a["name"]}</a></li>' for a in AREAS)}</ul>
<div style="margin-top:20px">{GENERAL_MAP()}</div>
</div>
<aside class="aside">{callcard(f'{s["noun"]} giving you trouble?')}
<div class="box"><h3>Other services</h3><ul>{others}</ul></div></aside>
</div></section>
{cta(f"Get your {s['noun'].lower()} fixed.")}'''
    svc_schema = {"@context":"https://schema.org","@type":"Service","name":s["name"],"serviceType":s["name"],
        "url":DOMAIN+path,"provider":{"@id":DOMAIN+"/#business"},
        "areaServed":[{"@type":"City","name":f"{a['name']}, AZ"} for a in AREAS],"description":s["intro"]}
    pages.append(page(path, f"{s['name']} in Pinal County, AZ | Fixed by Perri",
        f"{s['name']} in Florence, Coolidge, Casa Grande & Maricopa, AZ. {s['blurb']} Upfront estimates. Call (520) 954-5559.",
        body, "", (svc_schema, faq_schema(s["faq"]), crumbs_schema([("Home","/"),("Services","/services/"),(s["name"],path)]))))

# AREAS HUB
areas_hub = page_hero([("Home","/"),("Service Areas","/service-areas/")], "Service areas", "Appliance repair across Pinal County",
  "Fixed by Perri is based in Florence, Arizona and provides in-home appliance repair in Florence, Coolidge, Casa Grande and Maricopa.") + f'''
<section><div class="wrap">{area_tiles()}
<div style="margin-top:32px">{GENERAL_MAP()}</div>
<p style="margin-top:18px;color:var(--ink-2)">Not sure if you're in our area? <a href="tel:{TEL}">Call {PHONE}</a> and we'll let you know.</p>
</div></section>{cta()}'''
pages.append(page("/service-areas/", "Service Areas | Fixed by Perri Appliance Repair, Pinal County AZ",
  "Fixed by Perri serves Florence, Coolidge, Casa Grande and Maricopa, AZ with in-home appliance repair.",
  areas_hub, "", (crumbs_schema([("Home","/"),("Service Areas","/service-areas/")]),)))

# CITY PAGES
for a in AREAS:
    path = f"/service-areas/{a['slug']}/"
    n = a["name"]
    faqs = [
     (f"Do you offer appliance repair in {n}, AZ?", f"Yes. Fixed by Perri provides in-home repair for refrigerators, washers, dryers, dishwashers, ovens, ranges and microwaves throughout {n}."),
     (f"Which ZIP codes in {n} do you cover?", f"We serve {n} ZIP codes {', '.join(a['zips'])}. If you're on the edge of town, call and we'll confirm."),
     ("Will I get a price before the repair?","Yes. Perri diagnoses the problem and gives you an upfront estimate before any work begins."),
    ]
    svc = "".join(f'<a class="card" href="/services/{s["slug"]}/"><span class="ico">{ic(s["icon"])}</span><h3>{s["name"]}</h3><p>{s["blurb"]}</p></a>' for s in SERVICES)
    near = "".join(f'<li><a href="/service-areas/{x}/">{AREA[x]["name"]}</a></li>' for x in a["nearby"])
    body = page_hero([("Home","/"),("Service Areas","/service-areas/"),(n,path)], f"{n}, Arizona",
        f"Appliance Repair in {n}, AZ", a["intro"]) + f'''
<section><div class="wrap content-grid"><div class="prose">
<h2>Appliances we repair in {n}</h2>
<div class="cards" style="grid-template-columns:1fr 1fr;margin-bottom:10px">{svc}</div>
<h2>What to know about appliances in {n} homes</h2>
<p>{a["local"]}</p>
<h2>Neighborhoods &amp; ZIP codes</h2>
<p>We serve homes throughout {n}, including:</p>
<ul class="chips">{"".join(f"<li>{c}</li>" for c in a["communities"])}</ul>
<p style="margin-top:14px"><b>ZIP codes:</b> {", ".join(a["zips"])}</p>
<h2>{n} service area map</h2>
{gmap(a["map"], a["zoom"], f"Map of {n}, AZ service area")}
{faq_block(faqs)}
</div>
<aside class="aside">{callcard(f"Appliance repair in {n}")}
<div class="box"><h3>Nearby areas</h3><ul>{near}<li><a href="/service-areas/">All service areas</a></li></ul></div></aside>
</div></section>
{cta(f"Need appliance repair in {n}?")}'''
    pages.append(page(path, f"Appliance Repair in {n}, AZ | Fixed by Perri",
        f"In-home appliance repair in {n}, AZ ({', '.join(a['zips'])}). Fridge, washer, dryer, dishwasher, oven & microwave repair with upfront estimates. Call (520) 954-5559.",
        body, "", (faq_schema(faqs), crumbs_schema([("Home","/"),("Service Areas","/service-areas/"),(n,path)]))))

# CONTACT
contact = page_hero([("Home","/"),("Contact","/contact/")], "Request service", "Let's get it fixed.",
  "Call for the fastest answer, or send the form below and we'll reach out to schedule.", side=callcard("Fastest way to book","Call Perri directly.")) + f'''
<section><div class="wrap contact-grid">
<div>{form()}</div>
<div>
<ul class="contact-list">
<li><span class="ico">{ic("phone")}</span><div><b>Phone</b><a href="tel:{TEL}">{PHONE}</a></div></li>
<li><span class="ico">{ic("mail")}</span><div><b>Email</b><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
<li><span class="ico">{ic("pin")}</span><div><b>Based in</b>Florence, Arizona 85132<br><span style="color:var(--muted)">Serving Florence, Coolidge, Casa Grande &amp; Maricopa</span></div></li>
</ul>
<iframe class="map" loading="lazy" title="Map of Florence, AZ" src="https://www.google.com/maps?q=Florence,+AZ+85132&z=10&output=embed"></iframe>
</div>
</div></section>'''
pages.append(page("/contact/", "Request Appliance Repair | Contact Fixed by Perri",
  "Request in-home appliance repair from Fixed by Perri. Call (520) 954-5559 or send a service request. Serving Florence, Coolidge, Casa Grande & Maricopa, AZ.",
  contact, "contact", (crumbs_schema([("Home","/"),("Contact","/contact/")]),)))

# PRIVACY
privacy = page_hero([("Home","/"),("Privacy Policy","/privacy/")], "Legal", "Privacy Policy", f"Last updated November {YEAR}.", side="") + f'''
<section><div class="wrap prose" style="max-width:800px">
<p>Fixed by Perri ("we," "us") respects your privacy. This policy explains what information we collect through this website and how we use it.</p>
<h2>Information we collect</h2>
<p>When you submit a service request, we collect the details you provide, such as your name, phone number, email address, service address, and a description of your appliance problem. Like most websites, our hosting provider may also log basic technical information such as IP address and browser type.</p>
<h2>How we use it</h2>
<p>We use your information to respond to your request, schedule and perform service, send appointment reminders and follow-ups, and improve our service. We may contact you by phone, text message or email about your request.</p>
<h2>Text messages</h2>
<p>If you provide your phone number, you may receive text messages related to your service request. Message and data rates may apply. Reply STOP to opt out at any time. We do not sell or share your mobile number with third parties for marketing purposes.</p>
<h2>Sharing</h2>
<p>We do not sell your personal information. We share it only with service providers that help us run the business (for example, our scheduling and communication tools), or when required by law.</p>
<h2>Your choices</h2>
<p>You can ask us to update or delete your information at any time by emailing <a href="mailto:{EMAIL}">{EMAIL}</a> or calling <a href="tel:{TEL}">{PHONE}</a>.</p>
<h2>Contact</h2>
<p>Fixed by Perri · Florence, Arizona 85132 · {PHONE} · {EMAIL}</p>
</div></section>'''
pages.append(page("/privacy/", "Privacy Policy | Fixed by Perri", "Privacy policy for Fixed by Perri appliance repair.", privacy))

# 404
nf = f'''<section class="page-hero" style="padding-bottom:0"><div class="wrap" style="text-align:center;padding:40px 22px 0">
<span class="eyebrow">Page not found</span><h1>This page needs a repair.</h1><p class="lede" style="margin:0 auto 24px">The page you're looking for moved or doesn't exist. Try one of these instead.</p>
<div class="hero-ctas" style="justify-content:center"><a class="btn btn-primary" href="/">Go home</a><a class="btn btn-ghost" href="/services/">See services</a><a class="btn btn-ghost" href="tel:{TEL}">Call {PHONE}</a></div></div>{ridge()}</section>'''
page("/404.html", "Page not found | Fixed by Perri", "Page not found.", nf)

# ---------------------------------------------------------------- extras
(ROOT/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{DOMAIN}{p}</loc><changefreq>monthly</changefreq><priority>{'1.0' if p=='/' else '0.8'}</priority></url>\n" for p in pages) + "</urlset>\n")
(ROOT/"robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {DOMAIN}/sitemap.xml\n")
(ROOT/"_redirects").write_text("""# Old GoHighLevel URLs -> new pages (301)
/home                 /                0
/about-us             /about/          301
/about-us/            /about/          301
/contact-us           /contact/        301
/contact-us/          /contact/        301
/our-services         /services/       301
/services-page        /services/       301
/privacy-policy       /privacy/        301
/terms-of-service     /privacy/        301
""".replace(" 0\n"," 301\n"))
(ROOT/"_headers").write_text("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n/img/*\n  Cache-Control: public, max-age=2592000\n/css/*\n  Cache-Control: public, max-age=86400\n")
print(f"Built {len(pages)} pages")
