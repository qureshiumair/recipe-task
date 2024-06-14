from fastapi import APIRouter, Depends, HTTPException,Request
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi.encoders import jsonable_encoder
from app.database import get_db
from app.utils import jwt_auth
from app.models import Recipes
from app.schema import Recipe

router = APIRouter(dependencies=[Depends(jwt_auth.validate_access_token)])

@router.get("/get-recipe/v1")
def fetchRecipe(title: str = None, ingredients: str = None, db: Session = Depends(get_db)):
    '''
    This endpoint is use to get the  recipe details matched with title or ingredients.
    '''
    recipe_info = db.query(Recipes).filter(or_( Recipes.title==title, Recipes.ingredients==ingredients)).first()
    if not recipe_info:
        raise HTTPException(status_code=404,detail="No recipe found!")
    
    return jsonable_encoder(recipe_info)


@router.get("/get-recipe/all/v1")
def fetchAllRecipe(username:str=Depends(jwt_auth.validate_access_token),pageNum:int = 1,limit:int = 10,db: Session = Depends(get_db)):
    '''
    This endpoint is use to get the all recipe details.
    '''
    all_recipes = db.query(Recipes).filter_by(created_by=username).offset(pageNum-1*limit).limit(limit).all()
    if not all_recipes:
        raise HTTPException(status_code=404,detail="No recipe added by you!")
    
    return jsonable_encoder(all_recipes)


@router.post("/create-recipe/v1")
def createRecipe(body: Recipe, db: Session = Depends(get_db), username: str = Depends(jwt_auth.validate_access_token)):
    '''
    This endpoint is use to add new recipe details by the user.
    '''
    if db.query(Recipes).filter_by(title=body.title).first():
        raise HTTPException(status_code=409,detail="Recipe already present!")
    recipe_obj = Recipes(**body.model_dump(),created_by=username)
    db.add(recipe_obj)
    db.commit()
    return {"status":"Recipe details saved successfully!"}
    


@router.delete("/delete-recipe/v1")
def deleteRecipe(title:str, db: Session = Depends(get_db)):
    '''
    This endpoint is use to delete the existing stored recipe.
    '''
    recipe_obj = db.query(Recipes).filter_by(title=title).first()
    if not recipe_obj:
        raise HTTPException(status_code=404, detail="Recipe not found!")
    
    db.delete(recipe_obj)
    db.commit()
    return {"status":"Recipe deleted successfully!"}


@router.patch("/update-recipe/v1")
def updateRecipe(body:Recipe, db: Session = Depends(get_db)):
    '''
    This endpoint is use to update the existing stored recipe.
    '''
    recipe_obj = db.query(Recipes).filter_by(title=body.title).first()
    if not recipe_obj:
        raise HTTPException(status_code=404, detail="Recipe not found!")
    
    is_updated = False
    for attribute in ["description","ingredients","instructions"]:
        if getattr(recipe_obj,attribute) != getattr(body,attribute):
            is_updated = True
            setattr(recipe_obj,attribute,getattr(body,attribute))


    if not is_updated:
        raise HTTPException(status_code=400,detail="No updates found!")
    
    db.commit()
    return {"status":"Recipe details updated successfully!"}

