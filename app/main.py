import uuid

from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel,types


app = FastAPI() 


class Post(BaseModel):
    '''validation of incoming post content'''
    id: types.UUID1 = None
    title: str
    content: str
    published: bool = True # set default to True when optional param missing
    rating: Optional[str] = None # in this case, the field itself is optional.

my_posts = [{"title": "title of post 1","content": "content of post 2","id": str(uuid.uuid1())},
            {"title": "favourite foods","content":"I like pizza", "id": str(uuid.uuid1())},
            {"title": "test post","content":"post exists to be deleted", "id": "1"}]

def find_post(id: str):
    for p in my_posts:
        
        if p['id'] == id:
            return p

def find_index_post(id: str):
    for i,p in enumerate(my_posts):

        if p['id'] == id:
            return i


@app.get("/")
async def root():
    return {"message": "welcome to my api!!"}

@app.get("/posts")
async def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    print(post)
    print(post.dict())
    post_dict = post.dict()
    post_dict['id'] = uuid.uuid1()
    my_posts.append(post_dict)
    return {"data": post_dict}
    
@app.get("/posts/latest")
async def get_latest_post():
    latest_post = my_posts[-1]
    return {"latest post": latest_post}

@app.get("/posts/{id}")
async def get_posts(id: str, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id:{id} was not found.")
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: str):
    # deleting post#
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id:{id} does not exist")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def get_post(id: str,post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id:{id} does not exist")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict

    return {"data": post_dict}
