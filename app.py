import rumps
import huaweisms.api.user
import huaweisms.api.sms
import huaweisms.api.wlan
from dotenv import load_dotenv
import os
import webbrowser
from datetime import timedelta

# Load environment variables
load_dotenv()

# Get the password from environment variables
PASSWORD = os.getenv("PASSWORD")

class HuaweiSMSApp(rumps.App):
    def __init__(self):
        super(HuaweiSMSApp, self).__init__("SMS", icon="sms_icon_light.png")
        self.menu = ["Fetch SMS", "View Messages", "Connected Devices", "About"]
        self.messages = []

    @rumps.clicked("Connected Devices")
    def view_connected_devices(self, _):
        try:
            ctx = huaweisms.api.user.quick_login("admin", PASSWORD)
            devices_info = huaweisms.api.wlan.get_connected_hosts(ctx)
            
            if 'response' in devices_info and 'Hosts' in devices_info['response']:
                hosts = devices_info['response']['Hosts']['Host']
                devices_text = "📡 Connected Devices Report \n\n"
                
                for i, host in enumerate(hosts, 1):
                    device_name = host.get('HostName', 'Unknown Device')
                    ip_address = host.get('IpAddress', 'N/A').split(';')[0] 
                    mac_address = host.get('MacAddress', 'N/A')
                    connection_time = timedelta(seconds=int(host.get('AssociatedTime', '0')))
                    network = host.get('AssociatedSsid', 'N/A')
                    frequency = host.get('Frequency', 'N/A')

                    devices_text += f"{'🖥️' if 'MBP' in device_name else '📱'} Device {i}: {device_name}\n"
                    devices_text += f"   • IP: {ip_address}\n"
                    devices_text += f"   • MAC: {mac_address}\n"
                    devices_text += f"   • Connection Time: {connection_time}\n"
                    devices_text += f"   • Network: {network} ({frequency})\n\n"

                devices_text += f"Total Devices Connected: {len(hosts)}\n"
                devices_text += f"Network Name: {hosts[0].get('AssociatedSsid', 'N/A')}\n"
                devices_text += f"Frequency: {hosts[0].get('Frequency', 'N/A')}"

                rumps.alert("Connected Devices", devices_text)
            else:
                rumps.alert("Info", "No devices connected or unable to retrieve information")
        except Exception as e:
            rumps.alert("Error", f"An error occurred: {str(e)}")
    
    
    @rumps.clicked("About")
    def show_about(self, _):
        about_text = """
        Huawei SMS Fetcher
        
        Created by: Mohammed Fahad
        
        This amazing open source app allows you to fetch and view SMS messages from your Huawei router.
        Enjoy the convenience of accessing your messages right from your menu bar!
        

        """
        response = rumps.alert(title="About Huawei SMS Fetcher", message=about_text, ok="Visit GitHub", cancel="Close")
        if response:
            webbrowser.open("https://github.com/H4ck3r-x0")


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
