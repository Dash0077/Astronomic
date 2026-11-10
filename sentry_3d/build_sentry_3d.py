# Builds sentry_3d/sentry_3d.html: a 3D model of Earth and the riskiest Sentry asteroids.
# Data sources (all public, anonymous):
#   - JPL CNEOS Sentry API (risk list):  https://ssd-api.jpl.nasa.gov/doc/sentry.html
#   - JPL Small-Body Database API (orbits): https://ssd-api.jpl.nasa.gov/doc/sbdb.html
#   - Earth image: NASA Blue Marble, via the three-globe npm package on unpkg.com
# pip install requests pandas pillow
import base64, io, json, os, requests, pandas as pd
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, 'data')
os.makedirs(DATA, exist_ok=True)
N_TOP = 15                                   # how many of the highest-risk objects to show


def get_json(url, cache_name):
    """Download JSON once and keep a copy in data/ so reruns don't hit the API again."""
    path = os.path.join(DATA, cache_name)
    if not os.path.exists(path):
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        with open(path, 'w') as f:
            f.write(r.text)
    with open(path) as f:
        return json.load(f)


# 1. The Sentry risk list, sorted by cumulative Palermo scale (higher = more worrying)
sentry = get_json('https://ssd-api.jpl.nasa.gov/sentry.api', 'sentry_list.json')
df = pd.DataFrame(sentry['data'])
for col in ['ip', 'ps_cum', 'diameter', 'v_inf', 'h']:
    df[col] = pd.to_numeric(df[col], errors='coerce')
top = df.nlargest(N_TOP, 'ps_cum')


# 2. Orbital elements for each object from the Small-Body Database
def orbit(des):
    safe = des.replace(' ', '_')
    d = get_json(f'https://ssd-api.jpl.nasa.gov/sbdb.api?sstr={requests.utils.quote(des)}&full-prec=1',
                 f'sbdb_{safe}.json')
    el = {e['name']: float(e['value']) for e in d['orbit']['elements'] if e['value'] is not None}
    return {'epoch_jd': float(d['orbit']['epoch']),
            'a': el['a'], 'e': el['e'], 'i': el['i'], 'om': el['om'], 'w': el['w'], 'ma': el['ma']}


objects = []
for _, r in top.iterrows():
    objects.append({
        'name': r['fullname'].strip(), 'des': r['des'], 'status': 'listed',
        'ip': r['ip'], 'ps_cum': r['ps_cum'], 'diameter_km': r['diameter'],
        'years': r['range'], 'n_imp': int(r['n_imp']), 'v_inf': r['v_inf'],
        'orbit': orbit(r['des']),
    })
    print('got orbit for', r['fullname'].strip())

# 3. Case study: 2024 YR4, removed from the list after more observations
yr4 = get_json('https://ssd-api.jpl.nasa.gov/sentry.api?des=2024%20YR4', 'sentry_2024YR4.json')
objects.append({'name': '(2024 YR4)', 'des': '2024 YR4', 'status': 'removed',
                'removed': yr4.get('removed'), 'orbit': orbit('2024 YR4')})
print('2024 YR4 removed:', yr4.get('removed'))

# 4. Earth image, shrunk to keep the page small, embedded as a data URI
tex_path = os.path.join(DATA, 'earth_blue_marble.jpg')
if not os.path.exists(tex_path):
    r = requests.get('https://unpkg.com/three-globe@2.31.0/example/img/earth-blue-marble.jpg', timeout=120)
    r.raise_for_status()
    open(tex_path, 'wb').write(r.content)
img = Image.open(tex_path).convert('RGB').resize((1024, 512))
buf = io.BytesIO(); img.save(buf, 'JPEG', quality=80)
earth_uri = 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()

# 5. Fill the HTML template
payload = {'objects': objects, 'n_listed': len(df), 'fetched': pd.Timestamp.utcnow().strftime('%Y-%m-%d')}
html = open(os.path.join(HERE, 'template.html')).read()
html = html.replace('/*DATA*/null', json.dumps(payload)).replace('EARTH_TEXTURE_URI', earth_uri)
out = os.path.join(HERE, 'sentry_3d.html')
open(out, 'w').write(html)
print('wrote', out, f'({len(html) // 1024} KB)')
