#Consider in a company having users data
from collections import defaultdict, Counter
users = [
    { "id": 0, "name": "Hero" },
    { "id": 1, "name": "Dunn" },
    { "id": 2, "name": "Sue" },
    { "id": 3, "name": "Chi" },
    { "id": 4, "name": "Thor" },
    { "id": 5, "name": "Clive" },
    { "id": 6, "name": "Hicks" },
    { "id": 7, "name": "Devin" },
    { "id": 8, "name": "Kate" },
    { "id": 9, "name": "Kledlive"}]


#and also the network of people
friendship_pairs = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4),
(4, 5), (5, 6), (5, 7), (6, 8), (7, 8), (8, 9)]

# curating the friends of each other

friendship = {user["id"]:[] for user in users }

for i,j in friendship_pairs:
    friendship[i].append(j)
    friendship[j].append(i)

print(friendship)
#friend of a friend

#foaf not me or already one of my friends
def foaff(user_id):
    foaff = []
    for friend in friendship[user_id]:
        for friend in friendship[friend]:
            if friend not in (friendship[user_id] and foaff) and friend!=user_id:
                foaff.append(friend)
    return foaff

print(foaff(6))

interests = [
    (0, "Hadoop"), (0, "Big Data"), (0, "HBase"), (0, "Java"),
    (0, "Spark"), (0, "Storm"), (0, "Cassandra"),
    (1, "NoSQL"), (1, "MongoDB"), (1, "Cassandra"), (1, "HBase"),
    (1, "Postgres"), (2, "Python"), (2, "scikit-learn"), (2, "scipy"),
    (2, "numpy"), (2, "statsmodels"), (2, "pandas"), (3, "R"), (3, "Python"),
    (3, "statistics"), (3, "regression"), (3, "probability"),
    (4, "machine learning"), (4, "regression"), (4, "decision trees"),
    (4, "libsvm"), (5, "Python"), (5, "R"), (5, "Java"), (5, "C++"),
    (5, "Haskell"), (5, "programming languages"), (6, "statistics"),
    (6, "probability"), (6, "mathematics"), (6, "theory"),
    (7, "machine learning"), (7, "scikit-learn"), (7, "Mahout"),
    (7, "neural networks"), (8, "neural networks"), (8, "deep learning"),
    (8, "Big Data"), (8, "artificial intelligence"), (9, "Hadoop"),
    (9, "Java"), (9, "MapReduce"), (9, "Big Data")]

def people_who_like(target_interest):
    """return id of people who like target interest"""
    return [user_id
            for user_id, interest   in interests
            if interest == target_interest]

print(people_who_like("machine learning"))

user_id_by_interest = defaultdict(list)

for user_id, interest in interests:
    user_id_by_interest[interest].append(user_id)

print(user_id_by_interest)

interest_by_user_id = defaultdict(list)

for user_id, interest in interests:
    interest_by_user_id[user_id].append(interest)

print(interest_by_user_id)

#finding who has the most interest with a user
"""def most_common_interest_with(user_id):
    other_interested_user =[]
    for interest in interest_by_user_id[user_id]:
        for others_id in user_id_by_interest[interest]:
            if others_id != user_id:
                other_interested_user.append(others_id)

    return Counter(other_interested_user)"""

#In pythonic way this is:
def most_common_interest_with(user_id):
    return Counter(
        others_id for interest in interest_by_user_id[user_id]
        for others_id in user_id_by_interest[interest] if others_id != user_id
    )

print(most_common_interest_with(3))



