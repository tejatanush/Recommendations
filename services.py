import random
from database import get_collection
from bson import ObjectId
def fetch_all_courses():
    collection = get_collection()
    courses = list(collection.find())
    for course in courses:
        course["_id"] = str(course["_id"])
    return courses

def recommend_courses(course_list, all_courses,tags):
    shuffled_courses = all_courses.copy()
    random.shuffle(shuffled_courses)
    purchased_course_ids = set(course_list)
    recommended_ids = set()
    rec_from_tags_ids=set()
    rec_from_tags_list=[]
    if len(course_list)>0:
        course_list = [str(cid) for cid in course_list]
        if len(course_list) <= 3:
            recs_per_course = 5
        elif len(course_list) <= 8:
            recs_per_course = 4
        else:
            recs_per_course = 3
        
        
        # Create course dictionary for quick lookup
        course_dict = {course["_id"]: course for course in shuffled_courses}
        #print(course_dict)
        # Track purchased and recommended courses
        recommended_courses = []
        
        # For each course in user's list, find recommendations
        for course_id in course_list:
            if course_id not in course_dict:
                continue
                
            source_course = course_dict[course_id]
            course_recommendations = []
            
            # Try each rank level (1, 2, 3) in priority order
            for rank in ["1", "2", "3"]:
                if len(course_recommendations) >= recs_per_course:
                    break
                    
                # Get tags for current rank from source course
                source_tags = set(source_course.get("tags", {}).get(rank, []))
                if not source_tags:
                    continue
                
                # Find courses with matching tags
                for course in shuffled_courses:
                    if len(course_recommendations) >= recs_per_course:
                        break
                        
                    # Skip if course is purchased, already recommended, or same course
                    if (course["_id"] in purchased_course_ids or 
                        course["_id"] in recommended_ids or
                        course["_id"] == course_id):
                        continue
                    
                    # Get target course tags for current rank
                    target_tags = set(course.get("tags", {}).get(rank, []))
                    
                    # If there's any common tag, add to recommendations
                    if source_tags & target_tags:  # Intersection check
                        course_recommendations.append(course["title"])
                        recommended_ids.add(course["_id"])
            
            recommended_courses.extend(course_recommendations)
    if len(tags)>0:
        if len(tags)<=2:
            rec_from_tags=4
        else:
            rec_from_tags=2
        
        for tag in tags:
            for course2 in shuffled_courses:
                if len(rec_from_tags_list)>rec_from_tags:
                    break
                if (course2["_id"] in purchased_course_ids or 
                            course2["_id"] in recommended_ids or 
                            course2["_id"] in rec_from_tags_ids):
                            continue
                course_tags = set()
                for r in ["1", "2", "3"]:
                    course_tags.update(course2.get("tags", {}).get(r, []))

                if tag in course_tags:
                    rec_from_tags_list.append(course2["title"])
                    rec_from_tags_ids.add(course2["_id"])
    final_recommendations=rec_from_tags_ids|recommended_ids
    return final_recommendations