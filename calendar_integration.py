from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

# Set up Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

service = build('calendar', 'v3', credentials=creds)

async def handle_calendar_command(ctx, action, args):
    if action == 'events':
        await list_upcoming_events(ctx)
    elif action == 'add':
        # Implement add event functionality
        pass
    else:
        await ctx.send("Invalid calendar action. Use 'events' or 'add'.")

async def list_upcoming_events(ctx):
    if not creds or not creds.valid:
        await ctx.send("Calendar credentials are not set up or invalid.")
        return

    try:
        events_result = service.events().list(calendarId='primary', timeMin=datetime.utcnow().isoformat() + 'Z',
                                              maxResults=10, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            await ctx.send('No upcoming events found.')
        else:
            response = "Upcoming events:\n"
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                response += f"{start}: {event['summary']}\n"
            await ctx.send(response)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Add more calendar-related functions as needed