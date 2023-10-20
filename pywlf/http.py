import requests


def verify_url(url: str) -> bool:
    """判断url是否可用

    Args:
        url (str): url

    Returns:
        bool: True | False
    """
    res = False
    try:
        requests.packages.urllib3.disable_warnings()
        rep = requests.get(url, verify=False, timeout=30)
        if rep.status_code != 400:
            res = True
    except Exception as e:
        pass
    return res
