import React, { useState } from 'react';
import { Send, Database, BarChart3, MessageSquare, Loader2, CheckCircle, AlertCircle } from 'lucide-react';

interface QueryResult {
  answer: string;
  sql_query?: string;
  data?: any[];
  visualization?: string;
  error?: string;
}

function App() {
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<QueryResult | null>(null);
  const [showSQL, setShowSQL] = useState(false);

  const exampleQuestions = [
    "What is my total sales?",
    "Calculate the RoAS (Return on Ad Spend)",
    "Which product had the highest CPC?",
    "Which products are currently not eligible for ads?",
    "Show total clicks and impressions by product"
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      setResult({
        answer: 'Failed to connect to the AI agent. Please make sure the backend is running.',
        error: 'Connection error'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleExampleClick = (exampleQuestion: string) => {
    setQuestion(exampleQuestion);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-sm border-b border-gray-200/50 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
              <Database className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
                E-commerce AI Data Agent
              </h1>
              <p className="text-sm text-gray-600">Ask questions about your e-commerce data in natural language</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Main Query Interface */}
          <div className="lg:col-span-2 space-y-6">
            
            {/* Query Form */}
            <div className="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/50 p-6">
              <div className="flex items-center space-x-2 mb-4">
                <MessageSquare className="h-5 w-5 text-blue-600" />
                <h2 className="text-lg font-semibold text-gray-900">Ask Your Question</h2>
              </div>
              
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="relative">
                  <textarea
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="e.g., What is my total sales across all products?"
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 resize-none h-20 bg-white/50 backdrop-blur-sm"
                    disabled={loading}
                  />
                </div>
                
                <button
                  type="submit"
                  disabled={loading || !question.trim()}
                  className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 rounded-xl font-medium hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
                >
                  {loading ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" />
                      <span>Processing...</span>
                    </>
                  ) : (
                    <>
                      <Send className="h-4 w-4" />
                      <span>Ask Question</span>
                    </>
                  )}
                </button>
              </form>
            </div>

            {/* Results */}
            {result && (
              <div className="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/50 p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-2">
                    {result.error ? (
                      <AlertCircle className="h-5 w-5 text-red-600" />
                    ) : (
                      <CheckCircle className="h-5 w-5 text-green-600" />
                    )}
                    <h2 className="text-lg font-semibold text-gray-900">Results</h2>
                  </div>
                  
                  {result.sql_query && (
                    <button
                      onClick={() => setShowSQL(!showSQL)}
                      className="text-sm text-blue-600 hover:text-blue-700 underline"
                    >
                      {showSQL ? 'Hide SQL' : 'Show SQL'}
                    </button>
                  )}
                </div>

                <div className="space-y-4">
                  {/* Answer */}
                  <div className={`p-4 rounded-xl ${result.error ? 'bg-red-50 border border-red-200' : 'bg-blue-50 border border-blue-200'}`}>
                    <p className={`${result.error ? 'text-red-800' : 'text-blue-800'}`}>
                      {result.answer}
                    </p>
                  </div>

                  {/* SQL Query */}
                  {showSQL && result.sql_query && (
                    <div className="bg-gray-50 border border-gray-200 rounded-xl p-4">
                      <h3 className="text-sm font-semibold text-gray-700 mb-2">Generated SQL:</h3>
                      <pre className="text-xs bg-gray-800 text-green-400 p-3 rounded-lg overflow-x-auto">
                        <code>{result.sql_query}</code>
                      </pre>
                    </div>
                  )}

                  {/* Data Table */}
                  {result.data && result.data.length > 0 && (
                    <div className="overflow-hidden rounded-xl border border-gray-200">
                      <div className="bg-gray-50 px-4 py-2 border-b border-gray-200">
                        <h3 className="text-sm font-semibold text-gray-700">Data Results ({result.data.length} rows)</h3>
                      </div>
                      <div className="overflow-x-auto max-h-96">
                        <table className="min-w-full divide-y divide-gray-200">
                          <thead className="bg-gray-50">
                            <tr>
                              {Object.keys(result.data[0]).map((key) => (
                                <th key={key} className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                  {key}
                                </th>
                              ))}
                            </tr>
                          </thead>
                          <tbody className="bg-white divide-y divide-gray-200">
                            {result.data.map((row, index) => (
                              <tr key={index} className="hover:bg-gray-50 transition-colors duration-150">
                                {Object.values(row).map((value: any, cellIndex) => (
                                  <td key={cellIndex} className="px-4 py-2 whitespace-nowrap text-sm text-gray-900">
                                    {typeof value === 'number' ? 
                                      (value % 1 === 0 ? value.toLocaleString() : value.toFixed(2)) : 
                                      String(value)
                                    }
                                  </td>
                                ))}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            
            {/* Example Questions */}
            <div className="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/50 p-6">
              <div className="flex items-center space-x-2 mb-4">
                <BarChart3 className="h-5 w-5 text-purple-600" />
                <h2 className="text-lg font-semibold text-gray-900">Example Questions</h2>
              </div>
              
              <div className="space-y-2">
                {exampleQuestions.map((example, index) => (
                  <button
                    key={index}
                    onClick={() => handleExampleClick(example)}
                    className="w-full text-left p-3 rounded-lg bg-gradient-to-r from-gray-50 to-gray-100 hover:from-blue-50 hover:to-purple-50 transition-all duration-200 text-sm text-gray-700 hover:text-gray-900 border border-gray-200 hover:border-blue-200"
                  >
                    {example}
                  </button>
                ))}
              </div>
            </div>

            {/* Database Info */}
            <div className="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/50 p-6">
              <div className="flex items-center space-x-2 mb-4">
                <Database className="h-5 w-5 text-green-600" />
                <h2 className="text-lg font-semibold text-gray-900">Database Schema</h2>
              </div>
              
              <div className="space-y-4 text-sm">
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                  <h3 className="font-semibold text-blue-900 mb-1">Ad Sales Metrics</h3>
                  <p className="text-blue-700 text-xs">date, product_id, ad_spend, clicks, impressions, cpc</p>
                </div>
                
                <div className="bg-green-50 border border-green-200 rounded-lg p-3">
                  <h3 className="font-semibold text-green-900 mb-1">Total Sales Metrics</h3>
                  <p className="text-green-700 text-xs">date, product_id, total_sales, units_sold</p>
                </div>
                
                <div className="bg-purple-50 border border-purple-200 rounded-lg p-3">
                  <h3 className="font-semibold text-purple-900 mb-1">Product Eligibility</h3>
                  <p className="text-purple-700 text-xs">eligibility_datetime_utc, product_id, eligibility, message</p>
                </div>
              </div>
            </div>

            {/* Features */}
            <div className="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/50 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Features</h2>
              
              <div className="space-y-3 text-sm">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                  <span className="text-gray-700">Natural language to SQL conversion</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-gray-700">Multi-table joins & complex queries</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                  <span className="text-gray-700">Real-time data visualization</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
                  <span className="text-gray-700">Gemini 2.5 powered AI</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;