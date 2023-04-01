import requests
from django.shortcuts import render
from decouple import config


API_TOKEN = config("API_TOKEN")


# def search_aircraft(request):
#     # url = "https://dir.aviapages.com/api/aircraft?images=true"
#     company_url = "https://dir.aviapages.com/api/companies/"
#     airports_url = "https://dir.aviapages.com/api/airports/"
#     headers = {"Authorization": API_TOKEN}
#     if request.method == "GET":
#         search_query = request.GET.get("q", "").upper()
#         url_serial = f"https://dir.aviapages.com/api/aircraft?images=true&search_serial_number={search_query}"
#         url_tail = f"https://dir.aviapages.com/api/aircraft?images=true&search_serial_number={search_query}"
#         if len(search_query) < 2:
#             error_message = "Search query should be at least 2 characters long."
#             return render(request, "avia/search.html", {"error_message": error_message})

#         # params = {"search": search_query}
#         # response = requests.get(url=url, params=params, headers=headers)
#         results = []
#         # try:
#         while url and len(results) < 300:
#             response = requests.get(url=url, headers=headers)
#             if response.status_code == 200:
#                 result = response.json()
#                 for aircraft in result["results"]:
#                     if search_query in aircraft.get(
#                         "tail_number"
#                     ) or search_query in aircraft.get("serial_number"):
#                         company_detail = requests.get(
#                             url=f"{company_url}?search_name={aircraft.get('company_name')}",
#                             headers=headers,
#                         ).json()["results"]
#                         airports_detail = requests.get(
#                             url=f"{airports_url}?search_icao={aircraft.get('home_base')}",
#                             headers=headers,
#                         ).json()["results"]
#                         results.append(
#                             {
#                                 "aircraft": aircraft,
#                                 "company": company_detail,
#                                 "airport": airports_detail,
#                             }
#                         )
#             url = result["next"]
#         if len(results) == 0:
#             error_message = f"No results found for {search_query}"
#             return render(request, "avia/search.html", {"error_message": error_message})
#         else:
#             return render(request, "avia/search.html", {"results": results})
#         # except TypeError:
#         #     error_message = "An error occurred while searching for aircraft. Make sure to performe search only by the tail number or serial number of the aircraft."
#         #     return render(request, "avia/search.html", {"error_message": error_message})
#     else:
#         return render(request, "avia/search.html")


def search(url):
    company_url = "https://dir.aviapages.com/api/companies/"
    airports_url = "https://dir.aviapages.com/api/airports/"
    headers = {"Authorization": API_TOKEN}

    results = []
    while url and len(results) < 300:
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            for aircraft in result["results"]:
                company_detail = requests.get(
                    url=f"{company_url}?search_name={aircraft.get('company_name')}",
                    headers=headers,
                ).json()["results"]
                airports_detail = requests.get(
                    url=f"{airports_url}?search_icao={aircraft.get('home_base')}",
                    headers=headers,
                ).json()["results"]
                results.append(
                    {
                        "aircraft": aircraft,
                        "company": company_detail,
                        "airport": airports_detail,
                    }
                )
        url = result["next"]
    return results


def search_aircraft(request):
    if request.method == "GET":
        search_query = request.GET.get("q", "").upper()
        if len(search_query) < 2:
            error_message = "Search query should be at least 2 characters long."
            return render(request, "avia/search.html", {"error_message": error_message})
        url_tail = f"https://dir.aviapages.com/api/aircraft?images=true&search_tail_number={search_query}"
        url_serial = f"https://dir.aviapages.com/api/aircraft?images=true&search_serial_number={search_query}"
        search_tail = search(url=url_tail)
        search_serial = search(url=url_serial)
        results = search_tail + search_serial
        if len(results) == 0:
            error_message = f"No results found for {search_query}. Make sure to performe search only by the tail number or serial number of the aircraft."
            return render(request, "avia/search.html", {"error_message": error_message})
        else:
            return render(request, "avia/search.html", {"results": results})
