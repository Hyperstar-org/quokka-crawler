import requests

cookies = {
    'datr': 'gVyTZ-VCn8GiWn_0ep7Iz_il',
    'sb': 'gVyTZ0MeyGbB88L9JU5SJdO7',
    'ps_l': '1',
    'ps_n': '1',
    'c_user': '100081552710469',
    'cppo': '1',
    'ar_debug': '1',
    'fr': '1gVBLAtTnSwW4MASa.AWUregh61P403Bfn6vi2qMmYGfUVIV8z3MOH5A.BnrXjR..AAA.0.0.BnrXjR.AWUQODdrawU',
    'xs': '19%3AYFva1u9-3p6Vow%3A2%3A1739274928%3A-1%3A6804%3A%3AAcXRpy-H5eB0DHrXTxH09TvAe9WsKPnsJyYuF8hpgw',
    'presence': 'C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1739422117762%2C%22v%22%3A1%7D',
    'wd': '515x723',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded',
    # 'cookie': 'datr=gVyTZ-VCn8GiWn_0ep7Iz_il; sb=gVyTZ0MeyGbB88L9JU5SJdO7; ps_l=1; ps_n=1; c_user=100081552710469; cppo=1; ar_debug=1; fr=1gVBLAtTnSwW4MASa.AWUregh61P403Bfn6vi2qMmYGfUVIV8z3MOH5A.BnrXjR..AAA.0.0.BnrXjR.AWUQODdrawU; xs=19%3AYFva1u9-3p6Vow%3A2%3A1739274928%3A-1%3A6804%3A%3AAcXRpy-H5eB0DHrXTxH09TvAe9WsKPnsJyYuF8hpgw; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1739422117762%2C%22v%22%3A1%7D; wd=515x723',
    'origin': 'https://accountscenter.facebook.com',
    'priority': 'u=1, i',
    'referer': 'https://accountscenter.facebook.com/personal_info/contact_points/?contact_point_type=phone_number&contact_point_value=%2B84338668340&dialog_type=contact_detail',
    'sec-ch-prefers-color-scheme': 'dark',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-full-version-list': '"Not A(Brand";v="8.0.0.0", "Chromium";v="132.0.6834.162", "Google Chrome";v="132.0.6834.162"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"macOS"',
    'sec-ch-ua-platform-version': '"13.4.0"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'x-asbd-id': '129477',
    'x-fb-friendly-name': 'useTwoStepVerificationSendCodeMutation',
    'x-fb-lsd': 'MhONw2OWOFlyOlAFEbfq4A',
}

data = 'av=100081552710469&__user=100081552710469&__a=1&__req=i&__hs=20132.HYP%3Aaccounts_center_pkg.2.1...0&dpr=2&__ccg=EXCELLENT&__rev=1020065976&__s=dzzhx6%3Aic0eqv%3A0qioq4&__hsi=7470761322334491342&__dyn=7xeUmwlEnwn8K2Wmh0no6u5U4e0yoW3q32360CEbotw47wUx609vCwjE0AC0yE6ucw5Mx61vw9m1YwBgao6C0Mo2swlo5qfK0EUjwGzE2ZwNwmE2eU5O0HUvw6iyES1Tw8W0Lo6-3u362-0VE6O1FwlU6S0IUuwm85K0UE&__csr=gp8-HkjmWSDnncJkmRAZtUHIBfiFljFSGFGCRFz-YLtZf988UAxfHGmfjGV4XyUIjFUAwUxFoTAQ8qiJqFamfAWVkUmxZaUGHjWF2oyudDHwBWxm4EhgTyVK-8x2Vaz9-4Am9xapbK444-4lUpw04Gcw264ih9BWy8KAHWK2vVaGaAwfOU56U7QheE8A2kje585C3x09i0f6BWxNe8yeA1uHhH859paw1vt5Dyp60VGGmJ4WwEQmi5uGXBqFAw9JHwlE-ewXgqG78giho62qq5FFU1Je0tJ5CJyAE8A2lcAM3pG9GVYEhybwzwj8W8CUj4Pwuoc48G9K6E8FqBGbKE&__comet_req=5&fb_dtsg=NAcME61dlxrIKPFFh7i6xKYYuIbo1eY6JYvVG_VCIOh3LqKmZekJELA%3A19%3A1739274928&jazoest=25386&lsd=MhONw2OWOFlyOlAFEbfq4A&__spin_r=1020065976&__spin_b=trunk&__spin_t=1739422167&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=useTwoStepVerificationSendCodeMutation&variables=%7B%22encryptedContext%22%3A%22AWPOCkFFXHmXvsl6pQOlTJngc6ry2mgy2gFJHxlZBF7R4qhMkBvRNbmrhXk_O9ycncVZxPhJjH4WoZoH1ENJOC2r4XEGRhtEGjbSYU1DaLMs2vU_2Pbct9VFBasqpmEc01uUC3WuJicGFd066EDIdTmZRyt2GauFhhOSgXmkYj9soMYDIK8ZtGzzoP0J4KT_hKoa11hbk-tJsJw0TT52FJ1hVK3YSS59YP7lkhTI5rZ8_HJ1S32Ue7lZE1JLlBBA8Lv7DJ9qhs1doouP8gZTOTe_LD2P03-5E5YUZxzhAtku6_bs24LFkTZF3hV0B5UZmvBfHvrJbQeP6UknnGhqxGd9FSbUmzyXTbp0c6LRpImhf68ocfVx09G_00Fv7L01MOPyPr4aXdciaMB5hrmc46OgpYs7Z0w3M3DJ6UtzyU7p1jlXhaadt5J7hT_fYsnc0Z4bZhewRmPL%22%2C%22challenge%22%3A%22SMS%22%2C%22maskedContactPoint%22%3A%22***%20***%20**40%22%7D&server_timestamps=true&doc_id=7767429506681192'

response = requests.post('https://accountscenter.facebook.com/api/graphql/', cookies=cookies, headers=headers, data=data)
print(response.text)