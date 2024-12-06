from fastapi import APIRouter, HTTPException, Query 
from fastapi.responses import JSONResponse

from services.clients_mzg_service import get_all_customers, get_clubs_by_id_customer, get_contents_type_video_by_id_club, get_url_content_video, get_urls_video_by_customer, get_client_by_id

router = APIRouter(
    prefix='/mzg',
    tags=['myzonego']
)

@router.get("/clients", responses = {
    200: {"description": "Clients successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def get_all():
    customers = await get_all_customers()
    return customers

@router.get("/clients/{id}", responses = {
    200: {"description": "Clients successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def get_client(id: int):
    customer = get_client_by_id(id)
    return customer

@router.get("/clients/{id_customer}/clubs", responses = {
    200: {"description": "Club  successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def getClubsByCustomer(id_customer: str):
    clubs = get_clubs_by_id_customer(id_customer)
    print(clubs)
    return clubs

@router.get("/clubs/{id_club}/contents", responses = {
    200: {"description": "Video list successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def getContentsFromClub( id_club: str ):
    video_list = get_contents_type_video_by_id_club( id_club)
    return video_list

@router.get("/client/{customer_id}/content/video", responses = {
    200: {"description": "Video list successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def get_urls_video_by_customer_service( 
    customer_id: str, 
    count_only: bool = Query(False, description="If true, returns only the count of videos")
 ):
    if customer_id == '58':
        url_content = get_urls_video_by_customer( customer_id )
        if count_only:
            return { "count": len(url_content)}
        else:
            return url_content
    else:
        return { "count": 0 }
