#!/usr/bin/env python3
"""
Creates needed objects for session and user authentication
"""
from backend_auth.user_auth import RecruiterAuth, ApplicantAuth, BPAuth
from backend_auth.redis_session import RedisSession

print("Importing", __name__)

bp_auth = BPAuth()
recruiter_auth = RecruiterAuth()
applicant_auth = ApplicantAuth()
session_auth = RedisSession()