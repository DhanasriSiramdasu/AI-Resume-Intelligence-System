def compare_scores(old_result,new_result):
    old_ats=old_result.get("ats_score",0);
    new_ats=new_result.get("ats_score",0);

    old_match=old_result.get("match_score",0);
    new_match=new_result.get("match_score",0);

    return{
        "old_ats_score": old_ats,
        "new_ats_score": new_ats,
        "ats_score_change": round(new_ats - old_ats, 2),
        "old_match_score": old_match,
        "new_match_score": new_match,
        "match_score_change": round(new_match - old_match, 2),
        "new_matched_skills": new_result.get("matched_skills", []),
        "new_missing_skills": new_result.get("missing_skills", [])
    }