from rest_framework.throttling import UserRateThrottle

class AllBlogsThrottle(UserRateThrottle):
    scope = "all-blog"

class AllAuthorsThrottle(UserRateThrottle):
    scope = "all-authors"

class AllCommentsThrottle(UserRateThrottle):
    scope = "all-comment"

class CreateCommentThrottle(UserRateThrottle):
    scope = "create-comment"

