"""Сохранить четыре снимка локального стенда и включить их в README."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'services' / 'screenshots'
PLOTS = [('predictions', 'http://localhost:9091/graph?g0.expr=label_replace%28%28sum%28increase%28model_prediction_bucket%7Ble%3D%220.5%22%7D%5B5m%5D%29%29%29%2C+%22interval%22%2C+%22%E2%89%A4+0.5%22%2C+%22%22%2C+%22%22%29+or+label_replace%28%28sum%28increase%28model_prediction_bucket%7Ble%3D%221.0%22%7D%5B5m%5D%29%29+-+sum%28increase%28model_prediction_bucket%7Ble%3D%220.5%22%7D%5B5m%5D%29%29%29%2C+%22interval%22%2C+%22%280.5%2C+1%5D%22%2C+%22%22%2C+%22%22%29+or+label_replace%28%28sum%28increase%28model_prediction_bucket%7Ble%3D%222.0%22%7D%5B5m%5D%29%29+-+sum%28increase%28model_prediction_bucket%7Ble%3D%221.0%22%7D%5B5m%5D%29%29%29%2C+%22interval%22%2C+%22%281%2C+2%5D%22%2C+%22%22%2C+%22%22%29+or+label_replace%28%28sum%28increase%28model_prediction_bucket%7Ble%3D%223.0%22%7D%5B5m%5D%29%29+-+sum%28increase%28model_prediction_bucket%7Ble%3D%222.0%22%7D%5B5m%5D%29%29%29%2C+%22interval%22%2C+%22%282%2C+3%5D%22%2C+%22%22%2C+%22%22%29+or+label_replace%28%28sum%28increase%28model_prediction_bucket%7Ble%3D%225.0%22%7D%5B5m%5D%29%29+-+sum%28increase%28model_prediction_bucket%7Ble%3D%223.0%22%7D%5B5m%5D%29%29%29%2C+%22interval%22%2C+%22%283%2C+5%5D%22%2C+%22%22%2C+%22%22%29+or+label_replace%28%28sum%28increase%28model_prediction_bucket%7Ble%3D%228.0%22%7D%5B5m%5D%29%29+-+sum%28increase%28model_prediction_bucket%7Ble%3D%225.0%22%7D%5B5m%5D%29%29%29%2C+%22interval%22%2C+%22%285%2C+8%5D%22%2C+%22%22%2C+%22%22%29+or+label_replace%28%28sum%28increase%28model_prediction_bucket%7Ble%3D%2212.0%22%7D%5B5m%5D%29%29+-+sum%28increase%28model_prediction_bucket%7Ble%3D%228.0%22%7D%5B5m%5D%29%29%29%2C+%22interval%22%2C+%22%288%2C+12%5D%22%2C+%22%22%2C+%22%22%29+or+label_replace%28%28sum%28increase%28model_prediction_bucket%7Ble%3D%2220.0%22%7D%5B5m%5D%29%29+-+sum%28increase%28model_prediction_bucket%7Ble%3D%2212.0%22%7D%5B5m%5D%29%29%29%2C+%22interval%22%2C+%22%2812%2C+20%5D%22%2C+%22%22%2C+%22%22%29+or+label_replace%28%28sum%28increase%28model_prediction_bucket%7Ble%3D%2235.0%22%7D%5B5m%5D%29%29+-+sum%28increase%28model_prediction_bucket%7Ble%3D%2220.0%22%7D%5B5m%5D%29%29%29%2C+%22interval%22%2C+%22%2820%2C+35%5D%22%2C+%22%22%2C+%22%22%29+or+label_replace%28%28sum%28increase%28model_prediction_bucket%7Ble%3D%22%2BInf%22%7D%5B5m%5D%29%29+-+sum%28increase%28model_prediction_bucket%7Ble%3D%2235.0%22%7D%5B5m%5D%29%29%29%2C+%22interval%22%2C+%22%3E+35%22%2C+%22%22%2C+%22%22%29&g0.tab=0&g0.range_input=2m'), ('rate', 'http://localhost:9091/graph?g0.expr=60+%2A+sum%28rate%28prediction_requests_total%5B1m%5D%29%29&g0.tab=0&g0.range_input=2m'), ('errors', 'http://localhost:9091/graph?g0.expr=sum+by+%28status_class%29+%28prediction_requests_total%7Bstatus_class%3D~%224xx%7C5xx%22%7D%29&g0.tab=0&g0.range_input=2m')]
DASH = 'http://localhost:3001/d/car-price-lab4/lab4'


def capture():
    DEST.mkdir(exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={'width': 1600, 'height': 1150})
        for name, url in PLOTS:
            page.goto(url)
            page.locator('.graph-tab-content svg path, .graph-container svg path, .rickshaw_graph svg path, .flot-overlay, .uplot canvas').first.wait_for(timeout=45000)
            page.screenshot(path=DEST / f'{name}.png', full_page=True)
        origin = DASH.split('/d/')[0]
        login = page.request.post(origin + '/login', data={'user': 'admin', 'password': 'admin'})
        if not login.ok:
            raise RuntimeError(f'Grafana login: HTTP {login.status}')
        page.goto(DASH + '?from=now-2m&to=now&kiosk')
        page.locator('canvas').first.wait_for(timeout=45000)
        page.wait_for_timeout(2000)
        page.screenshot(path=DEST / 'grafana.png', full_page=True)
        browser.close()
    readme = ROOT / 'README.md'
    content = readme.read_text()
    heading = '### Снимки работающего стенда'
    if heading not in content:
        pictures = [('predictions','Предсказания'), ('rate','Запросы в минуту'),
                    ('errors','Ошибки HTTP'), ('grafana','Дашборд Grafana')]
        readme.write_text(content.rstrip() + '\n\n' + heading + '\n\n' +
                          '\n\n'.join(f'![{label}](services/screenshots/{name}.png)' for name, label in pictures) + '\n')


if __name__ == '__main__':
    capture()
