# Sentry Orbit Room (Project 7)

**Open the 3D model:** https://claude.ai/artifact/SSPspCFBKV9WAWe4YcnmT8
(Private link: only people it has been shared with can open it.)

An interactive 3D model of Earth and the 15 highest-risk asteroids on NASA JPL's Sentry impact-risk list, plus 2024 YR4 (removed from the list on 2026-03-05), moving on their real orbits around the Sun. Click an asteroid to see its riskiest impact date and what could happen if it hit.

## What you see

- **Sun** in the middle; faint gray rings mark 1, 2, 3 and 4 AU (1 AU = Earth–Sun distance).
- **Earth**: the spinning globe on the blue orbit.
- **Asteroids**: orange-to-red orbits (redder = higher Palermo score). 2024 YR4 has a dashed teal orbit because it was cleared.

## How to use it

| To do this | Do this |
|---|---|
| Rotate the view | Click and drag (one finger on a phone) |
| Zoom | Scroll, or pinch on a phone |
| Pause or play time | **Pause/Play** button; the date shows the moment you're viewing |
| Change the speed of time | **Speed** slider (0–60 days per second) |
| Return to the real date | **Back to today** |
| Zoom in on Earth | **View Earth** |
| Follow one asteroid | Click its row in the list on the right |
| Stop following | Drag the view yourself |

**The list:** *Palermo* is the risk score (below 0 = less than the normal background risk). *Chance* is the impact probability, e.g. "1:2,940" = 1 in 2,940. The top panel adds possible impact years, diameter and orbit shape: *a* = average distance from the Sun (AU), *e* = how stretched the orbit is (0 = circle), *i* = tilt compared with Earth's orbit (degrees).

## What's real

Orbits, positions and all risk numbers come from NASA JPL. Earth, the Sun and the asteroids are drawn much larger than real scale so you can see them, and the rocky asteroid shapes are only for looks.

## Rebuild it

```bash
python3 sentry_3d/build_sentry_3d.py
```

Downloads are cached in `data/`. To get the newest risk list, delete `data/sentry_list.json` and `data/sbdb_*.json` first. Output: `sentry_3d/sentry_3d.html`.

## Data sources

- JPL CNEOS Sentry API (risk list): https://ssd-api.jpl.nasa.gov/doc/sentry.html
- JPL Small-Body Database API (asteroid orbits): https://ssd-api.jpl.nasa.gov/doc/sbdb.html
- Earth's orbit: JPL "Approximate Positions of the Planets" (J2000 elements)
- Earth image: NASA Blue Marble
