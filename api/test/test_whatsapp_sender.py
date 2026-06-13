from api.services.whatsapp_sender import (
    WhatsAppSender
)

sender = WhatsAppSender()

response = sender.send_text_message(

    phone_number="+8801787178833",

    message="Hello from Hasanah Mart AI"
)

print(response)