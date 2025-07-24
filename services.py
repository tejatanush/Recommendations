import random
from database import get_collection
from bson import ObjectId
def fetch_all_courses():
    collection = get_collection()
    courses = list(collection.find())
    for course in courses:
        course["_id"] = str(course["_id"])
    return courses

def recommend_courses(course_list, all_courses, tags):
    shuffled_courses = all_courses.copy()
    random.shuffle(shuffled_courses)

    course_list = [str(cid) for cid in course_list]
    purchased_course_ids = set(course_list)

    recommended_ids = set()
    rec_from_tags_ids = set()

    # 📌 From purchased course list
    if course_list:
        if len(course_list) <= 3:
            recs_per_course = 5
        elif len(course_list) <= 8:
            recs_per_course = 4
        else:
            recs_per_course = 3

        course_dict = {course["_id"]: course for course in shuffled_courses}

        for course_id in course_list:
            if course_id not in course_dict:
                continue

            source_course = course_dict[course_id]

            for rank in ["1", "2", "3"]:
                if len(recommended_ids) >= recs_per_course * len(course_list):
                    break

                source_tags = set(source_course.get("tags", {}).get(rank, []))
                if not source_tags:
                    continue

                for course in shuffled_courses:
                    if course["_id"] in purchased_course_ids or course["_id"] in recommended_ids or course["_id"] == course_id:
                        continue

                    target_tags = set(course.get("tags", {}).get(rank, []))

                    if source_tags & target_tags:
                        recommended_ids.add(course["_id"])

    # 📌 From tags
    if tags:
        normalized_tags = [tag.lower().strip() for tag in tags]
        rec_from_tags_limit = 12

        for tag in normalized_tags:
            for course in shuffled_courses:
                if len(rec_from_tags_ids) >= rec_from_tags_limit:
                    break

                if (course["_id"] in purchased_course_ids or 
                    course["_id"] in recommended_ids or 
                    course["_id"] in rec_from_tags_ids):
                    continue

                all_tags = set()
                for r in ["1", "2", "3"]:
                    all_tags.update(t.lower().strip() for t in course.get("tags", {}).get(r, []))

                if tag in all_tags:
                    rec_from_tags_ids.add(course["_id"])

    # ✅ Return string versions of ObjectIds
    final_ids = list(rec_from_tags_ids | recommended_ids)
    return [str(cid) for cid in final_ids]