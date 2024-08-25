import rumps
import huaweisms.api.user
import huaweisms.api.sms



from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get the password from environment variables
PASSWORD = os.getenv("PASSWORD")

class HuaweiSMSApp(rumps.App):
    def __init__(self):
        super(HuaweiSMSApp, self).__init__("SMS", icon="sms_icon.png")
        self.menu = ["Fetch SMS", "View Messages"]
        self.messages = []

    @rumps.clicked("View Messages")
    def view_messages(self, _):
        if not self.messages:
            rumps.alert("No Messages", "There are no messages to display.")
            return

        message_text = ""
        for message in self.messages:
            message_text += f"From: {message['Phone']}\n"
            message_text += f"Date: {message['Date']}\n"
            message_text += f"Content: {message['Content'].encode('latin1').decode('utf-8')}\n\n"
            rumps.alert(title="SMS Messages", message=message_text, ok="Close")


    @rumps.clicked("Fetch SMS")
    def fetch_sms(self, _):
        try:
            # Login to the router
            ctx = huaweisms.api.user.quick_login("admin", PASSWORD)
            
            # Get SMS messages
            sms_response = huaweisms.api.sms.get_sms(ctx)

            if 'response' in sms_response and 'Messages' in sms_response['response']:
                messages = sms_response['response']['Messages']['Message']
                
                if isinstance(messages, list) and len(messages) > 0:
                    self.messages = messages
                    rumps.notification("SMS Fetch", "Success", f"{len(messages)} messages fetched")

                    for message in messages:
                        content = message.get('Content', 'No content')
                        try:
                            # Decode content if it's in bytes
                            content = content.encode('latin1').decode('utf-8')
                        except (AttributeError, UnicodeDecodeError) as e:
                            content = f'Unable to decode content: {e}'
                        
                        rumps.notification("New SMS", "Message Content", content)
                else:
                    rumps.notification("SMS Fetch", "Result", "No messages found.")
            else:
                rumps.notification("SMS Fetch", "Error", "Error retrieving messages.")
        
        except Exception as e:
            rumps.notification("Sorry", "", "Try Again Later 😚")


if __name__ == "__main__":
    HuaweiSMSApp().run()
