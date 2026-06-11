#!/usr/bin/env python3
"""
Update cities.json to add dataSource fields for all proxy cities
"""

import json

# Read the current cities.json
with open('/Users/aadarshks/my-ai-project/kerala_map/kerala-master-plan-viewer/cities.json', 'r') as f:
    data = json.load(f)

# Update each city
for city in data['cities']:
    if 'dataSource' not in city:
        city['dataSource'] = 'proxy'
        city['dataSourceUrl'] = 'https://www.openstreetmap.org'
        city['cogUrl'] = ''
        city['planYear'] = ''
        city['status'] = 'proxy-data'

# Write back
with open('/Users/aadarshks/my-ai-project/kerala_map/kerala-master-plan-viewer/cities.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Updated {len(data['cities'])} cities")
print("\nSummary:")
official = [c for c in data['cities'] if c['dataSource'] == 'official']
proxy = [c for c in data['cities'] if c['dataSource'] == 'proxy']
print(f"  Official: {len(official)}")
print(f"  Proxy: {len(proxy)}")
