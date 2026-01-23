import logging
import os
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from backend.config import GOOGLE_CREDENTIALS_PATH, GOOGLE_SPREADSHEET_ID

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

class SheetsService:
    def __init__(self):
        self.service = None
        self.spreadsheet_id = GOOGLE_SPREADSHEET_ID
        self.mock_mode = False
        self._memory = {} # Local in-memory cache {session_id: [messages]}
        self._authenticate()

    def _authenticate(self):
        if not os.path.exists(GOOGLE_CREDENTIALS_PATH):
            logger.warning(f"Credentials file not found at {GOOGLE_CREDENTIALS_PATH}. Running in MOCK mode.")
            self.mock_mode = True
            return

        try:
            creds = service_account.Credentials.from_service_account_file(
                GOOGLE_CREDENTIALS_PATH, scopes=SCOPES)
            self.service = build('sheets', 'v4', credentials=creds)
            # Drive service not strictly needed if we have direct ID access, but kept if needed later
            self.drive_service = build('drive', 'v3', credentials=creds)
            
            if not self.spreadsheet_id:
                logger.error("GOOGLE_SPREADSHEET_ID is not set in .env")
                self.mock_mode = True
                return

            logger.info(f"Successfully connected to Google Sheets. Spreadsheet ID: {self.spreadsheet_id}")
            
        except Exception as e:
             logger.error(f"Failed to authenticate with Google Sheets: {e}. Running in MOCK mode.")
             self.mock_mode = True

    def create_session_sheet(self, session_id: str):
        # Initialize local memory
        if session_id not in self._memory:
            self._memory[session_id] = []

        if self.mock_mode or not self.spreadsheet_id:
            logger.info(f"[MOCK] Created sheet for session {session_id}")
            return

        try:
            # Check if sheet exists
            sheet_metadata = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
            sheets = sheet_metadata.get('sheets', '')
            sheet_exists = any(s['properties']['title'] == session_id for s in sheets)

            if not sheet_exists:
                # Add new sheet
                body = {
                    'requests': [{
                        'addSheet': {
                            'properties': {'title': session_id}
                        }
                    }]
                }
                self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id, body=body).execute()
                
                # Add headers
                self.append_message(session_id, "Role", "Message", is_header=True)
                logger.info(f"Created new worksheet for session {session_id}")
            
        except Exception as e:
            logger.error(f"Error creating session sheet: {repr(e)}")

    def append_message(self, session_id: str, role: str, message: str, is_header=False):
        timestamp = datetime.now().isoformat()
        
        # 1. Update In-Memory Cache (Immediate Context) - skip headers
        if not is_header:
            if session_id not in self._memory:
                self._memory[session_id] = []
            self._memory[session_id].append({
                "Timestamp": timestamp,
                "Role": role,
                "Message": message
            })

        if self.mock_mode or not self.spreadsheet_id:
            logger.info(f"[MOCK] Appended to {session_id}: [{role}] {message}")
            return

        # 2. Update Google Sheets (Persistence)
        try:
            range_name = f"{session_id}!A:C"
            if is_header:
                values = [["Timestamp", role, message]]
            else:
                values = [[timestamp, role, message]]
            
            body = {'values': values}
            
            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                body=body
            ).execute()
        except Exception as e:
            logger.error(f"Error appending message to sheet {session_id}: {repr(e)}")

    def get_history(self, session_id: str):
        # 1. Prefer In-Memory Cache if active
        if session_id in self._memory and self._memory[session_id]:
            return self._memory[session_id]

        if self.mock_mode or not self.spreadsheet_id:
             return []
        
        # 2. Fallback to Sheets if memory empty (e.g. restart)
        try:
            range_name = f"{session_id}!A:C"
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id, range=range_name).execute()
            rows = result.get('values', [])
            
            if not rows:
                return []
            
            # Parse rows to dicts
            headers = rows[0]
            history = []
            for row in rows[1:]:
                # Ensure row has enough columns
                record = {}
                for i, header in enumerate(headers):
                    if i < len(row):
                        record[header] = row[i]
                history.append(record)
            
            # Hydrate memory
            self._memory[session_id] = history
            return history

        except HttpError as e:
             # Likely sheet not found
             return []
        except Exception as e:
            logger.error(f"Error fetching history: {repr(e)}")
            return []

sheets_service = SheetsService()
