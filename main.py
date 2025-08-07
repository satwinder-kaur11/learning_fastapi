from typing import Union, Annotated,Literal
from fastapi.responses import JSONResponse
from fastapi import FastAPI,Path,HTTPException,Query
from pydantic import BaseModel,Field,computed_field
import json

app = FastAPI()

class Patient(BaseModel):
    id   : Annotated[str, Field(..., description='id of the patient',examples=['P001'])]
    name : Annotated[str,Field(...,description='name of the patient')]
    city : Annotated[str,Field(...,description='city where the patient is living')]
    age  : Annotated[int,Field(...,gt=0,lt=120,description='age of the patient')]
    gender : Annotated[Literal['male','female','others'],Field(...,description='gender of the patient')]
    height : Annotated[float,Field(...,description='height of the patient in metres')]
    weight : Annotated[float,Field(...,description='weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self)-> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi <18.5:
            return 'UnderWeight'
        elif self.bmi <25:
            return 'Normal'
        elif self.bmi <30:
            return 'normal'
        else:
            return 'obese'

@app.get("/")
def read_root():
    return {"namaste": "World"}

def load_data():
    with open ("patients.json",'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open ('patients.json','w') as f:
        json.dump(data,f)

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id:str=Path(...,description='id of the patient in DB',example='P001')):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail = 'Patient not found')

@app.get('/sort')
def sort_patients(sort_by:str=Query(...,Description='sort on the basis of  height,weight,or bmi'),
                  order: str =Query('asc',Description=' sort on asc or desc order')):
    
    valid_fields =['height','weight','bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f'invalid filed select from {valid_fields}')
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='invalid order selcect between asc and  desc')
    
    data =load_data()

    sort_data =True if  order== 'desc' else 'False'

    sorted_data = sorted(data.values(),key=lambda x: x.get(sort_by,0),reverse=sort_data)
    return sorted_data


@app.post('/create')
def create_patient(patient:Patient):
    data =load_data()
    if patient.id in data:
        raise HTTPException(status_code=400,detail="patient already exixts")
    # patient is a pydantic and data is dictonary so uh have to convert pydantic into dict using model_dump()
    data[patient.id] = patient.model_dump(exclude=['id'])

save_data(data)
