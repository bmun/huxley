from invoice_automation.src.handler.registration_handler import RegistrationHandler

# TODO: Change to prod versions before deployment
CLIENT_ID = "ABYdHrqfKuQBK7bDiZpCK9C6Cq9bhayJJZbPCRyJLu7rO2nNqX"
CLIENT_SECRET = "KKJQ9uQJdlydvcCZigkZ3PlbEXQ8ZUjohKrEwzjN"
REDIRECT_URI = "http://localhost:8000/callback"
ENVIRONMENT = "sandbox"
REFRESH_TOKEN = "AB11669879742bImBH3CSnFynJA2Xng2YFA6N2aYK3KPciyikJ"
COMPANY_ID = "4620816365199192370"

handler = RegistrationHandler(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, ENVIRONMENT, REFRESH_TOKEN, COMPANY_ID)
