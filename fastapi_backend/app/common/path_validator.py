import re
from typing import List


check_path_list: List[str] = [
    "/api/v1/test/*"
]

def url_pattern_check(path: str) -> bool:
    for pattern in check_path_list:
        if re.match(pattern, path):
            return True
    
    return False