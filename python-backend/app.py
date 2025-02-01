from flask import Flask, request, jsonify
from EventScraperJP import pia_jp_scrap, eplus_jp_scrap, ltike_jp_scrap, combine_sheets

app = Flask(__name__)

@app.route('/start_scrape', methods=['POST'])
def start_scrape():
    data = request.get_json()
    selected_sites = data.get('selectedSites', [])
    print('Selected sites:', selected_sites)
    
    sheet_names = []
    months = [4, 5]
    from_date = "20250418"
    to_date = "20250514"
    
    if 'pagePia' in selected_sites:
        pia_jp_scrap()
        sheet_names.append("Events_t.pia.jp")
    if 'pageEplus' in selected_sites:
        eplus_jp_scrap(months)
        sheet_names.append("Events_eplus.jp")
    if 'pageLTike' in selected_sites:
        ltike_jp_scrap(from_date, to_date)
        sheet_names.append("Events_l-tike.com")

    if len(sheet_names) > 1:
        combine_sheets(sheet_names)

    return jsonify({'status': 'success', 'selectedSites': selected_sites})

if __name__ == '__main__':
    app.run(debug=True)