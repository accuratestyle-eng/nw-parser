from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import os

app = Flask(__name__)

# Вставь свою куку между кавычками ниже
NW_COOKIE_STRING = os.environ.get("NW_COOKIE", "_ga=GA1.1.1501333512.1788886828; intercom-id-ry2uoa7g=d19d13f0-7573-47c6-896d-294c54bf00b4; intercom-device-id-ry2uoa7g=125fa3e3-5b76-4f07-8edc-2207777976d5; _tt_enable_cookie=1; _ttp=01M20ZDP98E1XZ42Y8Q6DHPTNZ_.tt.1.1788886833449; ttcsid_CI3M5NRC77U7QBTMIDVG=1788886833451::E3lNKpYuQ_svLMlTLfv3.1.1788886843461.1; ttcsid=1788886833451::BZV_oU1x3hbBLcZNxLEq.1.1788886843460.0::1.-9203.0::15452.5.1309.203::0.0.0; llat_p56=investor; sdi_s15=6e9ba909b8089d04a5c2d86bc90b6b53; _fbp=fb.1.1794241569843.613061814398636116; __cf_bm=dSfu1jOsBXatfWvaxFID8k6t0V2KEsHmhw1IuTC0zHg-1794248450.915148-1.0.1.1-u2U_MxUQW6TYYHT2kjJa3hf6OsRh_hp.gT6hmAttO3z23sXcq3ThcGbe4VLx2.OQrN5NVI2Eq0kXxPRpAEZAKhud6CJRl7DJLO9QxVHssUzq5Z7W33oz00Gn22pd2pNQ; sipf_a21=xyka4o9gckbvgtsfj1s7arsz; _gcl_au=1.1.2012374265.1788886828.676123366.1794248461.1794248467.633192609.1794241573.1794248467; CognitoIdentityServiceProvider.13n3b86qk35vsl2l1b6vvu6gap.LastAuthUser=e811f390-d0a1-706f-58b4-b47231a31cf1; CognitoIdentityServiceProvider.13n3b86qk35vsl2l1b6vvu6gap.e811f390-d0a1-706f-58b4-b47231a31cf1.accessToken=eyJraWQiOiJnS2ZCbjdaNnAyZVM0SmNhbmI0YXM5eEtsVVZjRFdNYUJkRHM2b0RBano0PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJlODExZjM5MC1kMGExLTcwNmYtNThiNC1iNDcyMzFhMzFjZjEiLCJpc3MiOiJodHRwczovL2NvZ25pdG8taWRwLnVzLXdlc3QtMi5hbWF6b25hd3MuY29tL3VzLXdlc3QtMl9xSEFnTlVMR3AiLCJjbGllbnRfaWQiOiIxM24zYjg2cWszNXZzbDJsMWI2dnZ1NmdhcCIsIm9yaWdpbl9qdGkiOiIxZmNmZWVlZC0wZGI5LTQ2NzUtODVjYi1iNGI0NDEwMDljZWEiLCJldmVudF9pZCI6IjlhYjk1ZDJjLTZmYWUtNGU0YS04ZGRkLWQ3OGUzNTUwMjViMSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE3OTQyNDg1MTgsImV4cCI6MTc5NDI1MjExOCwiaWF0IjoxNzk0MjQ4NTE4LCJqdGkiOiJmOTgyZTJlOS00MDFmLTQ0OTMtOTk2Zi1mZmI2MjZkZDlmNDkiLCJ1c2VybmFtZSI6ImU4MTFmMzkwLWQwYTEtNzA2Zi01OGI0LWI0NzIzMWEzMWNmMSJ9.XJC8NDDwxkiA7-xWsmcdT5aWngZTfEg-Wc_k8i_EX_M0kaLq6jwh8cwNJbXFDD7HdPzrbhUsDDx4GDQzewA_rkzpm3_Zk1Uq02M1Ze3ggjjV_n1Zc3BT3ubKf_WELKTkd1-Ohquv1raP4q0twzxNqvtBj06QtWCWk1HGfIg0e1l9DDe9cFnfeJ8OLs41vmTEjQt_8KYyXAdx7OrALGzTgU2f28CQpXCpD2xhdtTARPna4-R0jLBSfn3TDKYvCusRnh4RC0S843rDKK3TW5v4uDsCa0W0mZ849I6cAxj2XxpQAckckI0aRhoDHDq9NWxDe9KgZdrmnORsKcxqqYLblg; CognitoIdentityServiceProvider.13n3b86qk35vsl2l1b6vvu6gap.e811f390-d0a1-706f-58b4-b47231a31cf1.idToken=eyJraWQiOiJCM0NDcEVpamJwUU9RQ3VkR1d3OGJIZWRkVGczSm1iSmZQR3lmOHM5bnhvPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJlODExZjM5MC1kMGExLTcwNmYtNThiNC1iNDcyMzFhMzFjZjEiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9jb2duaXRvLWlkcC51cy13ZXN0LTIuYW1hem9uYXdzLmNvbS91cy13ZXN0LTJfcUhBZ05VTEdwIiwiY29nbml0bzp1c2VybmFtZSI6ImU4MTFmMzkwLWQwYTEtNzA2Zi01OGI0LWI0NzIzMWEzMWNmMSIsIm9yaWdpbl9qdGkiOiIxZmNmZWVlZC0wZGI5LTQ2NzUtODVjYi1iNGI0NDEwMDljZWEiLCJhdWQiOiIxM24zYjg2cWszNXZzbDJsMWI2dnZ1NmdhcCIsImV2ZW50X2lkIjoiOWFiOTVkMmMtNmZhZS00ZTRhLThkZGQtZDc4ZTM1NTAyNWIxIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3OTQyNDg1MTgsImV4cCI6MTc5NDI1MjExOCwiaWF0IjoxNzk0MjQ4NTE4LCJqdGkiOiI0NDIyYWMzZC01NTY5LTRmOGMtYmIxMC02ZmE0MjljMjg5NTEiLCJlbWFpbCI6Inp6Y29tcGFueWxsY0BnbWFpbC5jb20ifQ.ceIEPgdI2epCp7FeMnJfwQLvu9f8SF4AlQowemGzM8VJdNi-LCFbuF4jdEg7KnJo2oM4vn4wcvczHFAA5KEVuu26txFlQGiRAnjulnHNcsVsYfhiggWdemDi9Tuj-YDB26fg7oBY88VCHtTNOd9ERep-ilOtV_lsYvGiaKFtQ7G3s9fc-UdpK9FVqx3kNkCFmIEuMlN68ZXRVR2hclYs5gw5bYCW0zW9y7oUxYmGMy-aGXbVJmeK55Psxc4al4am_4X79Tgb5ax8sb6V2JtGwb14Xet7Ovy_lS_WiIu6lA94bEe5Pe9mYDTxzzyAR1hhHImfdH5O4MyMUay3ze36Kw; CognitoIdentityServiceProvider.13n3b86qk35vsl2l1b6vvu6gap.e811f390-d0a1-706f-58b4-b47231a31cf1.refreshToken=eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.iGR1wJMz1ltvmYPO6sCDznP4uDmuyTNkD6rXqCHADpXedvjUUNjHHLhPJBXINI9RehhHby5n9-7neNS52KOkfaBY8J5S_ZPTqEOJ60F1lSXUoVW4_yygsODU2FfhqUtFsknvG7ROq54Y3shubK1bOhv6fEbwSjLv0vKpMCXsyiT1WVjqWT0Q0XGwUQTeNAvYDfLeKfvfmfU9EpTcqWvEzE8U-XOABus0BBUoc2qduapkcpFoAXxR3FFr9WxxnIMzSMc9M_98Ll-Bb6ldX3rFjuEgKqeOb2BfTpPE6Q9IcBRwGrhirWL6SesVYSFCQyxPpVKw2hw9H5G7qkY9iM_UWw.nq1YaanTSDjxrolq.VPTVpbWIkc91w6HAsgpyXoz7C0PhAKFYdlhp_jOkpKS11n8IKGi2bZgfVrxvrFvKUPtSZHopwJyNgrmbwUqEzIguw-EM-cMiDe4Di9V_mnuUplrPzTgbhWfJrxqIts-X7JDaSpVOkXNUHU5iCORXN8BXVQHFWnLks90FCFSKJppoUOiB5iAzXKtxTtLhO9okw2NwiwOtw96CLTGRlw3qCsuPhtsAeBJLrJUyWdZeOpkPm2S3HhGc2YZvD-FV_nMZ8pTxcne5Qh5T63DLgNFgN7MCWh_OuRhBRsg1atjt6UQ-OcDlYSRsGQh9Ned-reSHVWs1qXogMDZSORiN0AgRHa2fjm7YZ93QUApTQvQMjoxHFC82h_8nc20BHw1hGKEHIwUxTezoL2s2kJlrnJ_cpK0cw_sTbqQt6fRORUMledWbH6dmYRFQPLgIUQn91xm8PoL4W7uKDa96ZBD02xDgswA8_06Objw2z51iVKApR9uWQZ8CWeJKGNJ5OAb3d19SqG4orO2SAdad9XbpzAbEqDad93dzG_RPnUolgmnbh5pONwUE42Ld01mqlttSgoXm_7FaXynkWSVlY7WjGCBItwLbLzZBKjgu1SoKl9mLFbqD-Hipuhv1dWF1LeUTHPa0pSPodLxDCaDdyf4K5PzYh9mVt9AMq979hB9J-sP_q9HIogNEaVo3aC4g3XCrl-TMCi-ElQRuYkKaED12bN3m4EEhQdZncf8YTKJZxWTNneu6Yi5665k098mKHHUQcT3CR8f88W72TeVpR8drxsOy0khB3FLOgN7hHBC44qaSDl5VE3WFgqfJgCiN2lT9Hjfo3akJ8ROEVnai2a0MIQbWjrFpRDrnsihtR64MZR-49drIwp_Kqy79d-BIVmh4oK-N-6ywEOrAHn56esQmyKiVWD7qC7UKQKGTA-Cd9lcp_Ixr18vyluMWNPjzjXNso7CvcG_biC1FToiveSeVJ1TVim4Ha-2MJHuD8jsSOzTBe1rP7PkvtLbkCE6XXjeuaOPMsq9uciFBsOwVDaZQjyChM1aec_BIVIhH3zaTyn8URS1E9s-PEr3bZABZs5LribNjA047zSN8kDNTgIV2LSM1vUzkq-dH3_961hiVA-P_FPWIRyWw3uBYS3aN0cl-iI-AbTWn3mm_iiqlDm0SHUnEmp8nlZuzPE9tVsf-6HKJPIGCZEe5HJMvlVXWcSUp8qfDBW4PwMKVfwK4Ytx7S1tBodL3Wbk0AEGsVF5iKaGfLPUCVEcKQBBrTegryPtiDzx_x8_PkgVH97NUULaF69ustX7nRUD0bdHnC_mpWrXf92tYnqcfATol.gRqPg-B2saUjgLxaOkQRXg; CognitoIdentityServiceProvider.13n3b86qk35vsl2l1b6vvu6gap.e811f390-d0a1-706f-58b4-b47231a31cf1.signInDetails={%22loginId%22:%22zzcompanyllc@gmail.com%22%2C%22authFlowType%22:%22USER_SRP_AUTH%22}; CognitoIdentityServiceProvider.13n3b86qk35vsl2l1b6vvu6gap.e811f390-d0a1-706f-58b4-b47231a31cf1.clockDrift=-524; lsut_h73=investor; lsmi_x84=ccf18athdtlqvskbdfwtmmyp; fs_lua=1.1794248535395; fs_uid=#HX2XR#4411a0fd-a0f4-40bf-8dee-68e949fbcfbd:a987cff6-6809-49b0-9e2a-064f5727e2e3:1794248458587::3####/1820422842; _ga_L01QCY9LG4=GS2.1.s1794246688$o4$g1$t1794248536$j46$l0$h528540657; _ga_SZSZDK1F0R=GS2.1.s1794246688$o4$g1$t1794248536$j46$l0$h1251214382; lsmc_k29={%22bounds%22:{%22south%22:26.470753708680693%2C%22west%22:-99.99243266872355%2C%22north%22:32.944318527580066%2C%22east%22:-90.65405361699071}%2C%22center%22:{%22lat%22:29.759784142857143%2C%22lng%22:-95.32324314285714}%2C%22eventTrigger%22:%22mapUIChange%22%2C%22relatedMarketId%22:%22Houston%22%2C%22zoom%22:7}; intercom-session-ry2uoa7g=YnpKZ2tzS09PYitiNDZsRmNLS1BFcEorWnNxMzdGZmlHOWdUL3hMcTVSREVKNjRwb3ZyUjB3aVVCYTA5SkhEbWo0RXl6RVRjeTYvUHd5Unp0d3RJQzU1dDJaV3JYbDEwOWlyR1VDU1J0aWtOd0dLWU1NZm9tVU4vQ0twdldaNWdaT1lFSENMQjIwcGpxOUNKUWVVNy9YYjlnLzFjbHRHK3RGdUhxam42T21BYUxSQTV6OWorczc2aXdmVEs3MjNWZHRMVlZnTjJQaEhPTm5BUElVWER5UT09LS1Hd1NWODVkTUxBUjZDeTd1ZkpyZzZRPT0=--583794f001f15293ab52ec16142b42b59ac0ccbf; idch_p23=false; _dd_s=logs=1&id=f8d7f93e-7b40-49c0-bc3a-54842f485e16&created=1794248455165&expire=1794249506438&rum=1")

@app.route('/parse_nw', methods=['POST'])
def parse_nw():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    html_content = ""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        cookies = []
        for item in NW_COOKIE_STRING.split(';'):
            if '=' in item:
                name, value = item.strip().split('=', 1)
                cookies.append({
                    "name": name,
                    "value": value,
                    "domain": ".newwestern.com",
                    "path": "/"
                })
        context.add_cookies(cookies)
        
        page = context.new_page()
        
        try:
            page.goto(url, wait_until="networkidle", timeout=15000)
            page.wait_for_selector("text=$", timeout=10000)
            html_content = page.content()
        except Exception as e:
            html_content = f"Error or Cloudflare block: {str(e)}"
            
        browser.close()

    return jsonify({"html": html_content})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
