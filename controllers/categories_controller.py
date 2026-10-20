
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status

import dtos.categories
import models
from custom_exceptions.not_found_exception import NotFoundException
from factories.services import category_service_factory
from services.abc_category_service import ABCCategoryService

router = APIRouter(prefix='/api/categories', tags=['categories'])

CategoryServ = Annotated[ABCCategoryService, Depends(category_service_factory)]

#OPEN MUKANA:
#@router.post('/', status_code=status.HTTP_201_CREATED)
#def create_category(_service: CategoryServ, req: dtos.CreateCategoryReq) -> dtos.CategoryDto:
    #category = _service.create(req)
    #return dtos.CategoryDto.model_validate(category)

#OPEN MUKANA:
#@router.get('/')
#def get_all(_repository: Session = Depends(get_db)):
    #_qry = _repository.query(models.Category)
    #categories = _qry.all()
    #return categories

@router.get('/')
def get_all(_service: CategoryServ) -> List[dtos.categories.CategoryDto]:
    return _service.get_all()


@router.get('/{category_id}')
def get_by_id(category_id: int, _service: CategoryServ) -> dtos.categories.CategoryDto:
    try:
        return _service.get_by_id(category_id)
    except NotFoundException as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(req: dtos.categories.CreateCategoryReq,
           _service: CategoryServ) -> dtos.categories.CategoryDto:
    return _service.create(req)


@router.put('/{category_id}')
def update(category_id: int, req: dtos.categories.CreateCategoryReq,
           _service: CategoryServ) -> dtos.categories.CategoryDto:
    try:
        return _service.update(category_id, req)
    except NotFoundException as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(category_id: int, _service: CategoryServ):
    try:
        _service.delete(category_id)
    except NotFoundException as error:
        raise HTTPException(status_code=404, detail=str(error))