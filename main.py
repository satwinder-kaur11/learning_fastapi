from typing import Union

from fastapi import FastAPI,Path,HTTPException,Query
import json
app = FastAPI()


@app.get("/")
def read_root():
    return {"namaste": "World"}

def load_data():
    with open ("patients.json",'r') as f:
        data = json.load(f)
    return data

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

