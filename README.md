
# BLOG API KEY

# How this project works?

The user will need to log in first if he already has an account; otherwise, the user will need to register.

The user will be able to create comments for blogs, but the user cannot create 2 comments for the same blog. User can update, delete, and create comments they have created. 
But the user can not update, create, or delete the blog, they can perform only get request, ready only. 


When the user logs in, a token will be created for this user automatically, so user  can carry this token and does not need to log in on each request, and when the user logs out, the token will be deleted.

Users should log in in order to create, delete, and update comments.

If a user is not authenticated, some urls allow only get request and this user can perform only 1 request per day. 

If the user is authenticated, he can perform around 200 requests per day to the server.
User can not update, delete other users comments only the admin can do that.

Admin has access to update, create, delete created comments and also they can perform create, delete, update request on blogs.
