import uuid
import psycopg2
import time

from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel,types
from psycopg2.extras import RealDictCursor #gets column name from table

while(True):
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres'
                                ,password='password1231',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connection was successful!!")
        break
    except Exception as error:
        print("Connection to database failed....")
        print("Error: ",error)
        time.sleep(3)



app = FastAPI() 


class Post(BaseModel):
    '''validation of incoming post content'''
    id: str
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
    cursor.execute("""SELECT * from products""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):

    cursor.execute("""INSERT INTO products (title, content, published) VALUES(%s,%s,%s) RETURNING *"""
    ,(post.title,post.content, post.published))

    new_post = cursor.fetchone()

    conn.commit()

    return {"data": new_post}
    
@app.get("/posts/latest")
async def get_latest_post():
    latest_post = my_posts[-1]
    return {"latest post": latest_post}

@app.get("/posts/{id}")
async def get_posts(id: str, response: Response):
    cursor.execute("""SELECT * from products WHERE id =%s""",(id),)
    test_post = cursor.fetchone()
    #post = find_post(id)
    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id:{id} was not found.")
    return {"post_detail": test_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: str):
    # deleting post#
    cursor.execute("""DELETE FROM products WHERE id = %s returning *""", id,)

    deleted_post = cursor.fetchone()
    
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id:{id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
async def get_post(id: str,post: Post):

    cursor.execute("""UPDATE products set title =%s,content=%s,published=%s WHERE id =%s RETURNING *""",
                    (post.title,post.content,post.published,id),)
    index = cursor.fetchone()

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id:{id} does not exist")
    
    conn.commit()
    return {"data": index, "status": "resource updated successfully"}
