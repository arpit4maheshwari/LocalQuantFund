from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/whatsapp/webhook")
async def whatsapp_webhook(req: Request):
    data = await req.json()
    # TODO: handle incoming WhatsApp messages
    return {"status": "received"}
