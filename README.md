# E-commerce AI Data Analysis Agent

An intelligent question-answering system that converts natural language queries into SQL and provides insights from e-commerce datasets using Google Gemini 2.5.

## 🚀 Features

- **Natural Language Processing**: Convert plain English questions to SQL queries using Gemini 2.5
- **Multi-table Analysis**: Intelligent joins across ad metrics, sales data, and product eligibility
- **Real-time Visualizations**: Interactive charts and graphs with Plotly
- **Modern Web Interface**: Beautiful React frontend with Tailwind CSS
- **Production Ready**: FastAPI backend with proper error handling and logging
- **Comprehensive Analytics**: RoAS calculations, performance metrics, and eligibility tracking

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **SQLite**: Lightweight database for demo purposes
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive data visualizations
- **Google Gemini 2.5**: LLM for natural language to SQL conversion

### Frontend
- **React + TypeScript**: Modern UI framework
- **Tailwind CSS**: Utility-first styling
- **Lucide React**: Beautiful icons
- **Responsive Design**: Mobile-first approach

## 📊 Database Schema

### Product_Level_Ad_Sales_Metrics
- `date` (DATE): Metrics date
- `product_id` (INT): Product identifier  
- `ad_spend` (FLOAT): Advertising spend
- `clicks` (INT): Ad clicks
- `impressions` (INT): Ad impressions
- `cpc` (FLOAT): Cost per click

### Product_Level_Total_Sales_Metrics
- `date` (DATE): Sales date
- `product_id` (INT): Product identifier
- `total_sales` (FLOAT): Revenue
- `units_sold` (INT): Units sold

### Product_Eligibility
- `eligibility_datetime_utc` (DATETIME): Check timestamp
- `product_id` (INT): Product identifier
- `eligibility` (BOOLEAN): Ad eligibility status
- `message` (TEXT): Status message

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run the FastAPI server**:
   ```bash
   python backend/app.py
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Start the development server**:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

## 🎯 Example Queries

Try these natural language questions:

- "What is my total sales?"
- "Calculate the RoAS (Return on Ad Spend)"
- "Which product had the highest CPC?"
- "Which products are currently not eligible for ads?"
- "Show total clicks and impressions by product"
- "What's the trend in ad spend over time?"
- "Compare sales performance across products"

## 🔧 API Endpoints

### POST /ask
Convert natural language to SQL and execute queries.

**Request**:
```json
{
  "question": "What is my total sales?"
}
```

**Response**:
```json
{
  "answer": "Found 3 result(s). Here's what I discovered from your data:",
  "sql_query": "SELECT SUM(total_sales) as total_sales FROM Product_Level_Total_Sales_Metrics",
  "data": [{"total_sales": 15700.0}],
  "visualization": null,
  "error": null
}
```

### GET /schema
Get database schema information.

### GET /
Health check endpoint.

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React Frontend │────│   FastAPI Backend │────│   SQLite DB     │
│   (TypeScript)   │    │   (Python)       │    │   (Sample Data) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Gemini 2.5 API │
                       │   (X.AI)         │
                       └──────────────────┘
```

## 🔒 Security Features

- Environment variable management for API keys
- CORS protection
- Input validation with Pydantic
- SQL injection prevention through parameterized queries
- Comprehensive error handling and logging

## 📈 Performance Optimizations

- Async FastAPI endpoints
- Database connection pooling
- Efficient data serialization
- Frontend code splitting
- Optimized bundle sizes

## 🧪 Testing

The system includes sample e-commerce data for testing:
- 3 products with ad metrics
- 2 days of sales data
- Eligibility status tracking

## 🚀 Deployment

### Backend Deployment
```bash
# Using uvicorn
uvicorn backend.app:app --host 0.0.0.0 --port 8000

# Or using Docker
docker build -t ecommerce-ai-agent .
docker run -p 8000:8000 ecommerce-ai-agent
```

### Frontend Deployment
```bash
npm run build
# Deploy dist/ folder to your hosting provider
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🔮 Future Enhancements

- [ ] Real-time streaming responses
- [ ] Advanced visualization types
- [ ] Export functionality (CSV, PDF)
- [ ] Historical query caching
- [ ] Multi-tenant support
- [ ] Advanced security features
- [ ] Integration with external data sources

## 📞 Support

For support and questions, please open an issue on GitHub or contact the development team.

---

Built with ❤️ using modern web technologies and AI-powered insights.