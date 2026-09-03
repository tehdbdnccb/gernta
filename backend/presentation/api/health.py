from fastapi import APIRouter, Request
router=APIRouter(tags=["system"])
@router.get("/health")
async def health(request:Request): return {"status":"ok","environment":getattr(request.app.state,"environment","unknown")}
