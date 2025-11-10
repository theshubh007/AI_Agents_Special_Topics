# 💰 Full Stack E2E Agentic Multimodal Application

**Course:** FA25: CMPE-297 Sec 49 - Special Topics

---

## 📋 Assignment Overview

This repository demonstrates a complete full-stack multimodal agent application with frontend, backend, and RAG (Retrieval-Augmented Generation) capabilities. The project showcases a Personal Expense Assistant built with Google's Agent Development Kit (ADK), featuring multimodal input processing (text, images, receipts), database integration, and an interactive web interface.

**Assignment Goals:**
- Build full-stack agentic application with frontend and backend
- Implement multimodal capabilities (text, image, document processing)
- Integrate RAG for intelligent information retrieval
- Connect to proper database backend
- Deploy end-to-end working application
- Demonstrate complete code walkthrough

## 📹 Video Demonstration
[Walkthrough YouTube Video](https://www.youtube.com/)

---

## 📂 Project Structure

```
E2E_Agentic_Multimodel_App/
├── backend/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── expense_agent.py          # Main agent implementation
│   │   ├── tools/
│   │   │   ├── receipt_processor.py  # Image/receipt processing
│   │   │   ├── expense_tracker.py    # Expense management
│   │   │   └── analytics.py          # Data analysis tools
│   │   └── rag/
│   │       ├── vector_store.py       # Vector database integration
│   │       └── retriever.py          # RAG retrieval logic
│   ├── database/
│   │   ├── models.py                 # Database models
│   │   ├── connection.py             # DB connection setup
│   │   └── migrations/               # Database migrations
│   ├── api/
│   │   ├── routes.py                 # API endpoints
│   │   └── middleware.py             # Authentication, CORS
│   ├── requirements.txt
│   └── main.py                       # Backend entry point
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.tsx     # Chat UI component
│   │   │   ├── ReceiptUpload.tsx     # Image upload component
│   │   │   ├── ExpenseDashboard.tsx  # Analytics dashboard
│   │   │   └── ExpenseList.tsx       # Expense list view
│   │   ├── services/
│   │   │   └── api.ts                # API client
│   │   ├── App.tsx                   # Main app component
│   │   └── index.tsx                 # Entry point
│   ├── package.json
│   └── tsconfig.json
├── database/
│   └── schema.sql                    # Database schema
├── docker-compose.yml                # Container orchestration
├── .env.example                      # Environment variables template
└── README.md                         # This file
```

---

## 🏗️ Architecture Overview

### Three-Tier Architecture

**1. Frontend Layer (React/TypeScript)**
- Interactive chat interface
- Multimodal input (text, image upload)
- Real-time expense visualization
- Responsive dashboard
- Receipt image preview

**2. Backend Layer (Python/FastAPI + ADK)**
- ADK-powered intelligent agent
- Multimodal processing (Gemini 2.0)
- RESTful API endpoints
- Business logic and validation
- RAG integration

**3. Data Layer (PostgreSQL + Vector DB)**
- Relational database for structured data
- Vector database for RAG (Chroma/Pinecone)
- Expense records storage
- User data management
- Embedding storage

### Multimodal Capabilities

**Text Processing:**
- Natural language expense queries
- Conversational interface
- Intent understanding
- Context maintenance

**Image Processing:**
- Receipt photo upload
- OCR for text extraction
- Automatic expense categorization
- Amount and date detection

**Document Processing:**
- PDF receipt handling
- Multi-page document support
- Structured data extraction

---

## 🎯 Key Features

### 1. Multimodal Expense Tracking
- Upload receipt photos
- Extract expense details automatically
- Manual entry via chat
- Voice input support (optional)

### 2. Intelligent Agent Capabilities
- Natural language understanding
- Context-aware responses
- Expense categorization
- Budget recommendations
- Spending pattern analysis

### 3. RAG Integration
- Retrieve past expense patterns
- Contextual recommendations
- Historical data analysis
- Personalized insights

### 4. Database Backend
- Persistent expense storage
- User authentication
- Transaction history
- Category management
- Budget tracking

### 5. Analytics Dashboard
- Spending trends visualization
- Category breakdown
- Monthly comparisons
- Budget vs actual
- Export capabilities

---

## 📋 Implementation Guide

### Phase 1: Backend Setup

**Step 1: Environment Configuration**
- Install Python 3.10+
- Set up virtual environment
- Install ADK and dependencies
- Configure Google Cloud credentials
- Set up database connection

**Step 2: Database Setup**
- Install PostgreSQL
- Create database schema
- Set up vector database (Chroma)
- Run migrations
- Seed initial data

**Step 3: Agent Development**
- Create expense agent with ADK
- Implement multimodal tools
- Configure Gemini 2.0 model
- Set up receipt processing
- Integrate RAG retriever

**Step 4: API Development**
- Create FastAPI application
- Define API endpoints
- Implement authentication
- Add CORS middleware
- Set up error handling

### Phase 2: Frontend Development

**Step 1: React Setup**
- Initialize React app with TypeScript
- Install UI libraries (Material-UI/Tailwind)
- Set up routing
- Configure API client
- Set up state management

**Step 2: Component Development**
- Build chat interface
- Create receipt upload component
- Develop expense dashboard
- Implement expense list view
- Add analytics charts

**Step 3: Integration**
- Connect to backend API
- Implement real-time updates
- Add image upload functionality
- Handle multimodal responses
- Error handling and loading states

### Phase 3: RAG Implementation

**Step 1: Vector Store Setup**
- Initialize vector database
- Create embedding pipeline
- Index expense data
- Set up retrieval logic

**Step 2: RAG Integration**
- Connect agent to vector store
- Implement context retrieval
- Add relevance scoring
- Optimize query performance

### Phase 4: Deployment

**Step 1: Containerization**
- Create Dockerfiles
- Set up docker-compose
- Configure environment variables
- Test local deployment

**Step 2: Cloud Deployment**
- Deploy backend to Cloud Run
- Deploy frontend to Firebase/Vercel
- Set up Cloud SQL
- Configure secrets management

---

## 🚀 Usage Examples

### Example 1: Receipt Upload

**User Action:**
- Upload receipt photo via web interface

**Agent Processing:**
1. Receives image through multimodal API
2. Uses Gemini 2.0 vision to extract text
3. Identifies: amount, date, merchant, category
4. Stores in database
5. Returns structured expense data

**User Sees:**
- Extracted expense details
- Suggested category
- Confirmation prompt

### Example 2: Natural Language Query

**User:** "How much did I spend on groceries last month?"

**Agent Processing:**
1. Understands intent (spending query)
2. Retrieves relevant data from database
3. Uses RAG to find similar past queries
4. Calculates total
5. Generates natural response

**Response:** "You spent $450 on groceries last month, which is 15% more than the previous month."

### Example 3: Budget Analysis

**User:** "Am I on track with my budget?"

**Agent Processing:**
1. Retrieves current month expenses
2. Compares with budget limits
3. Uses RAG for historical patterns
4. Generates insights
5. Provides recommendations

**Response:** "You've spent 65% of your monthly budget with 10 days remaining. Based on your usual spending pattern, you're on track to stay within budget."

---

## 🎓 Key Technologies

### Backend Stack
- **Google ADK:** Agent framework
- **Gemini 2.0:** Multimodal LLM
- **FastAPI:** Web framework
- **PostgreSQL:** Relational database
- **Chroma/Pinecone:** Vector database
- **SQLAlchemy:** ORM
- **Pydantic:** Data validation

### Frontend Stack
- **React:** UI framework
- **TypeScript:** Type safety
- **Material-UI/Tailwind:** UI components
- **Axios:** HTTP client
- **Chart.js/Recharts:** Data visualization
- **React Query:** Data fetching

### Infrastructure
- **Docker:** Containerization
- **Google Cloud Run:** Backend hosting
- **Firebase/Vercel:** Frontend hosting
- **Cloud SQL:** Managed database
- **Secret Manager:** Credentials management

---

## 💡 Best Practices

### Agent Design
- Clear tool definitions
- Proper error handling
- Context management
- Multimodal input validation
- Response formatting

### Database Design
- Normalized schema
- Proper indexing
- Foreign key constraints
- Migration management
- Backup strategy

### API Design
- RESTful conventions
- Proper status codes
- Request validation
- Rate limiting
- API documentation

### Frontend Design
- Component reusability
- State management
- Error boundaries
- Loading states
- Responsive design

### Security
- Authentication and authorization
- Input sanitization
- SQL injection prevention
- CORS configuration
- Environment variable management

---

## 🐛 Troubleshooting

### Issue: Multimodal Processing Fails
**Solutions:**
- Verify Gemini API credentials
- Check image format and size
- Validate API quota limits
- Review error logs
- Test with sample images

### Issue: Database Connection Errors
**Solutions:**
- Verify connection string
- Check database is running
- Validate credentials
- Review firewall rules
- Test connection manually

### Issue: RAG Retrieval Poor Quality
**Solutions:**
- Improve embedding quality
- Adjust similarity threshold
- Increase indexed data
- Optimize query formulation
- Review vector dimensions

### Issue: Frontend-Backend Communication
**Solutions:**
- Check CORS configuration
- Verify API endpoints
- Review network requests
- Validate request/response format
- Check authentication tokens

---

## 🔗 Resources

### Official Documentation
- **Codelab:** https://codelabs.developers.google.com/personal-expense-assistant-multimodal-adk
- **ADK Documentation:** https://developers.google.com/adk
- **Gemini API:** https://ai.google.dev/docs

### Related Articles
- **Multimodal ADK Part 1:** https://medium.com/google-cloud/going-multimodal-with-agent-development-kit-personal-expense-assistant-with-gemini-2-5-480b031c7d5a
- **Multimodal ADK Part 2:** https://medium.com/google-cloud/going-multimodal-with-agent-development-kit-personal-expense-assistant-with-gemini-2-5-17626aaee9a2

### Additional Resources
- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/
- PostgreSQL: https://www.postgresql.org/docs/
- Chroma: https://docs.trychroma.com/

---

## 📹 Video Demonstration

https://www.youtube.com/

### Video Requirements

Your video walkthrough should cover:

1. **Project Overview (3 min)**
   - Architecture explanation
   - Technology stack
   - Key features demonstration

2. **Backend Code Walkthrough (8 min)**
   - Agent implementation
   - Multimodal tools
   - RAG integration
   - Database models
   - API endpoints

3. **Frontend Code Walkthrough (6 min)**
   - Component structure
   - Chat interface
   - Receipt upload
   - Dashboard implementation
   - API integration

4. **Database Schema (3 min)**
   - Table structure
   - Relationships
   - Vector store setup
   - Migration process

5. **End-to-End Demonstration (10 min)**
   - User registration/login
   - Receipt upload and processing
   - Natural language queries
   - Dashboard analytics
   - RAG-powered insights
   - Error handling

**Total Duration:** 30 minutes

---

## ✅ Completion Checklist

### Backend
- [ ] ADK agent implemented
- [ ] Multimodal processing working (text + images)
- [ ] Receipt OCR functional
- [ ] Database models created
- [ ] PostgreSQL connected
- [ ] Vector database integrated
- [ ] RAG retrieval working
- [ ] API endpoints implemented
- [ ] Authentication added
- [ ] Error handling complete

### Frontend
- [ ] React app initialized
- [ ] Chat interface built
- [ ] Receipt upload component working
- [ ] Dashboard with analytics
- [ ] Expense list view
- [ ] API integration complete
- [ ] Responsive design
- [ ] Error handling
- [ ] Loading states

### Integration
- [ ] Frontend-backend communication working
- [ ] Multimodal input processing end-to-end
- [ ] Database persistence verified
- [ ] RAG providing relevant context
- [ ] Real-time updates functioning

### Deployment
- [ ] Docker containers created
- [ ] docker-compose working locally
- [ ] Environment variables configured
- [ ] Cloud deployment successful
- [ ] Database migrations applied

### Documentation
- [ ] README complete
- [ ] API documentation
- [ ] Setup instructions
- [ ] Architecture diagrams
- [ ] Code comments

### Video
- [ ] Code walkthrough recorded
- [ ] All components explained
- [ ] End-to-end demo shown
- [ ] Video uploaded to YouTube
- [ ] Link added to README

---

## 🎯 Grading Criteria

- **Architecture & Design (20%)** - Full-stack structure, proper separation of concerns
- **Multimodal Capabilities (20%)** - Text and image processing working correctly
- **RAG Integration (15%)** - Vector database and retrieval functioning
- **Database Backend (15%)** - Proper schema, persistence, queries
- **Frontend Quality (15%)** - UI/UX, responsiveness, functionality
- **Code Quality (10%)** - Clean, documented, maintainable code
- **Video Walkthrough (5%)** - Clear explanation and demonstration

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Docker (optional)
- Google Cloud account

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Set up environment variables in `.env`

Run database migrations

Start backend server

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

### Docker Setup

```bash
docker-compose up --build
```

Access application at http://localhost:3000

---

## 📊 Database Schema

### Tables

**users**
- id (primary key)
- email
- password_hash
- created_at

**expenses**
- id (primary key)
- user_id (foreign key)
- amount
- category
- merchant
- date
- description
- receipt_url
- created_at

**categories**
- id (primary key)
- name
- budget_limit
- user_id (foreign key)

**embeddings**
- id (primary key)
- expense_id (foreign key)
- vector
- metadata

---

## 🔐 Security Considerations

- Store API keys in environment variables
- Use Secret Manager for production
- Implement JWT authentication
- Validate all user inputs
- Sanitize database queries
- Enable HTTPS in production
- Implement rate limiting
- Add CORS restrictions
- Encrypt sensitive data
- Regular security audits

---

## 🌟 Advanced Features (Optional)

- Voice input for expense entry
- Multi-currency support
- Recurring expense tracking
- Budget alerts and notifications
- Export to CSV/PDF
- Mobile app version
- Collaborative expense sharing
- Integration with bank APIs
- AI-powered budget recommendations
- Predictive spending analysis

---

**Last Updated:** November 2025
**Course:** CMPE-297 Special Topics
**Assignment:** Full Stack E2E Agentic Multimodal Application
**Due Date:** November 9, 2025

