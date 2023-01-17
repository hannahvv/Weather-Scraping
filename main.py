from bs4 import BeautifulSoup
import requests


USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
LANGUAGE = "en-US,en;q=0.5"

def get_weather(url):
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accepted-Langauge'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html = session.get(url)

    soup = BeautifulSoup(html.text, "html.parser")

    result = {}
    if(soup.find("div", attrs={'id': "wob_loc"}) is None):
        print("not a valid location")
        return
    result['location'] = soup.find("div", attrs={'id': "wob_loc"}).text
    result['time'] = soup.find("div", attrs={"id": "wob_dts"}).text
    result['weather'] = soup.find("span", attrs={"id": "wob_dc"}).text
    result['temp_F'] = soup.find("span", attrs={"id": "wob_tm"}).text
    result['temp_C'] = soup.find("span", attrs={"id": "wob_ttm"}).text
    result['precipitation'] = soup.find("span", attrs={"id": "wob_pp"}).text
    result['humidity'] = soup.find("span", attrs={"id": "wob_hm"}).text
    result['wind_mph'] = soup.find("span", attrs={"id": "wob_ws"}).text
    result['wind_kmh'] = soup.find("span", attrs={"id": "wob_tws"}).text


    weekly = []

    week = soup.find("div", attrs={"id": "wob_dp"})
    week = week.findAll("div", attrs={"class": "wob_df"})
    for day in week:
        day_name = day.findAll("div")[0].attrs['aria-label']
        day_weather = day.find("img").attrs["alt"]
        day_temp = day.findAll("span", {"class": "wob_t"})

        max_temp_C = day_temp[0].text
        max_temp_F = day_temp[1].text

        min_temp_C = day_temp[2].text
        min_temp_F = day_temp[3].text

        weekly.append({"name": day_name, "weather": day_weather, "max_temp_C": max_temp_C, "max_temp_F": max_temp_F,
                     "min_temp_C": min_temp_C,"min_temp_F": min_temp_F})

    result['weekly'] = weekly

    return result


if __name__ == "__main__":

    URL = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"

    region = input("Enter a location")
    URL += region
    data = get_weather(URL)

    if(data is not None):
        print("Weather for:", data["location"])
        print("Now:", data["time"])
        print(f"Temperature now: {data['temp_C']}°C/{(data['temp_F'])}°F")
        print("Description:", data['weather'])
        print("Precipitation:", data["precipitation"])
        print("Humidity:", data["humidity"])
        print(f"Wind: {data['wind_mph']} / {data['wind_kmh']}")
        print()
        print("Weekly Spread:")
        for dayweather in data["weekly"]:
            print("_"*40, dayweather["name"], "_"*40)
            print("Description:", dayweather["weather"])
            print(f"Max temperature: {dayweather['max_temp_C']}°C/{dayweather['max_temp_F']}°F")
            print(f"Min temperature: {dayweather['min_temp_C']}°C/{dayweather['min_temp_F']}°F")

