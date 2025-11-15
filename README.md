# Haze - Sports Betting Platform

A comprehensive sports betting application with real-time odds, live betting, social features, and payment integration.

## 🏗️ Architecture

### Tech Stack
- **Frontend Web**: React with TypeScript
- **Frontend Mobile**: React Native
- **Backend**: Python FastAPI
- **Database**: PostgreSQL
- **Real-time**: WebSockets
- **Payment**: Stripe/PayPal integration
- **Sports Data**: The Odds API

### Project Structure
```
Haze/
├── backend/              # Python FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── models/      # Database models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── services/    # Business logic
│   │   └── core/        # Configuration
│   └── tests/
├── frontend-web/        # React web application
│   └── src/
│       ├── components/  # Reusable components
│       ├── pages/       # Page components
│       ├── services/    # API services
│       └── store/       # State management
└── frontend-mobile/     # React Native mobile app
    └── src/
        ├── components/
        ├── screens/
        └── navigation/
```

## ✨ Features

### Core Features
- ✅ User authentication and account management
- ✅ Sports and events listing
- ✅ Real-time odds display
- ✅ Bet placement and management
- ✅ Wallet/balance system
- ✅ Bet history and statistics
- ✅ Live betting capabilities
- ✅ Multiple sports support

### Additional Features
- ✅ Payment integration (Stripe/PayPal)
- ✅ Admin panel
- ✅ Live score updates
- ✅ Social features (following, leaderboards)

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- The Odds API key

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Configure your environment variables
alembic upgrade head  # Run database migrations
uvicorn app.main:app --reload
```

### Web Frontend Setup
```bash
cd frontend-web
npm install
cp .env.example .env
npm start
```

### Mobile Frontend Setup
```bash
cd frontend-mobile
npm install
cp .env.example .env
npm run ios    # For iOS
npm run android  # For Android
```

## 🔑 Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/haze
SECRET_KEY=your-secret-key
ODDS_API_KEY=your-odds-api-key
STRIPE_SECRET_KEY=your-stripe-key
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
```

## 📱 API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend-web
npm test
```

## 📄 License

MIT

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
