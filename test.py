import requests

headers = {"Authorization": "0197ea51807b2909bc64d846f18babd607281086"}
# print(requests.get("http://kf.sharful.com/api/v2/", headers=headers)) # 200
# print(requests.get("http://kf.sharful.com/imports/a73VCS5ESwG3UgkfvfC2K2/data/", headers=headers))  # 200
res = requests.get("http://kf.sharful.com/api/v2/assets.json", headers=headers)
print("forms " + str(res.json()["results"]))
print("status code " + str(res.status_code))
print([r for r in res if r["asset_type"] != "empty"])

# print(requests.get("http://kf.sharful.com/api/v2/assets.json", headers=headers))  # 200

# print(requests.get("http://kf.sharful.com/exports/", headers=headers))  # 200
# print(requests.get("http://kc.sharful.com/api/v2/assets/a73VCS5ESwG3UgkfvfC2K2/data.json", headers=headers))  # 200
# print(requests.get("http://kf.sharful.com/api/v2/assets/a73VCS5ESwG3UgkfvfC2K2/data.json", headers=headers))  # 404
# print(
#     requests.get("http://kc.sharful.com/api/v2/assets/a73VCS5ESwG3UgkfvfC2K2/submissions.json", headers=headers)
# )  # 200
# print(requests.get("http://kf.sharful.com/imports/a73VCS5ESwG3UgkfvfC2K2", headers=headers))  # 404
# print(requests.get("http://kf.sharful.com/api/v2/assets/format=json", headers=headers))  # 200
# print(requests.get("http://kc.sharful.com/assets/?format=json", headers=headers))  # 200
# print(requests.get("http://kf.sharful.com/api/v2/assets/a73VCS5ESwG3UgkfvfC2K2/data.json", headers=headers))  # 404
# print(requests.get("http://kf.sharful.com/api/v2/a73VCS5ESwG3UgkfvfC2K2/data.json", headers=headers)) # 404
# print(requests.get("http://kf.sharful.com//assets/v2/a73VCS5ESwG3UgkfvfC2K2/assets.json", headers=headers))  # 404
# print(requests.get("http://kf.sharful.com//assets/v2/a73VCS5ESwG3UgkfvfC2K2/data", headers=headers))  # 404


# Returns: <Response [200]>
