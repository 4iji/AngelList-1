import requests

response = requests.get("https://community-angellist.p.mashape.com/follows/batch?ids=86500%2C173917",
                        headers={
                            "X-Mashape-Key": "zGjsCCgLLjmshuot9mzX4sZL932qp1d26q2jsnIoIiuaLAm9Tu",
                            "Accept": "application/json"
                        }
                        )
