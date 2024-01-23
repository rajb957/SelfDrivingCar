import random
import json
points=[]
for i in range(0,100):
    points.append((random.randint(100,700),random.randint(100,500)))

def convex_hull(points):
    points = sorted(set(points))
    if len(points) <= 1:
        return points
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]

points = convex_hull(points)
inner_points = []
for p in points:
    p = (p[0]-100*(p[0]-400)/abs(p[0]-400),p[1]-100*(p[1]-300)/abs(p[1]-300))
    inner_points.append(p)

d={'outer_points':points , 'inner_points': inner_points}
# write points and inner_points to a json file named level.py
with open('level.json','w') as f:
    json.dump(d, f)

