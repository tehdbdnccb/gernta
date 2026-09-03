from __future__ import annotations
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from application.dashboard.service import DashboardService

router=APIRouter(tags=["dashboard"])
def get_service(request:Request)->DashboardService:
    service=getattr(request.app.state,"dashboard_service",None)
    if service is None: raise RuntimeError("DashboardService has not been initialized")
    return service
Dep=Annotated[DashboardService,Depends(get_service)]

@router.get("/portfolio")
async def portfolio(service:Dep): return await service.portfolio()
@router.get("/journal")
async def journal(service:Dep,limit:int=Query(50,ge=1,le=500)): return await service.journal(limit)
@router.get("/trades/runs/{run_id}")
async def analysis(run_id:str,service:Dep):
    try: return await service.trade_analysis(run_id)
    except LookupError as e: raise HTTPException(404,str(e)) from e
