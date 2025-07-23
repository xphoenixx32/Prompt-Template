import React, { useState } from 'react';
import { Copy, Download, RefreshCw, Eye, EyeOff } from 'lucide-react';

const PromptEngineeringGenerator = () => {
  const [formData, setFormData] = useState({
    domain: '',
    specialization: '',
    specificGoal: '',
    action: '',
    details: '',
    constraints: '',
    format: '',
    structure: '',
    unwantedResult: ''
  });
  
  const [showPreview, setShowPreview] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const generatePrompt = () => {
    const prompt = `# <Role>
- You are an expert in ${formData.domain || '{domain}'} with specialization in ${formData.specialization || '{specialization}'}.

# <Task>
- Your task is to ${formData.specificGoal || '{specific goal}'}.

## Reasoning
- Let's think step by step.

## Action
- [Search("${formData.action || '{action}'}")]

## Observation
- Based on the action result to generate output.

# <Context>
- Here is the context you need: 
  - ${formData.details || '{details}'}
  - ${formData.constraints || '{constraints}'}

# <Output Format>
- Return a ${formData.format || '{format}'} file with the following structure: ${formData.structure || '{...}'}
- Don't ${formData.unwantedResult || '{unwanted result}'}`;
    
    return prompt;
  };

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(generatePrompt());
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('複製失敗:', err);
    }
  };

  const downloadPrompt = () => {
    const element = document.createElement('a');
    const file = new Blob([generatePrompt()], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = 'generated_prompt.txt';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const resetForm = () => {
    setFormData({
      domain: '',
      specialization: '',
      specificGoal: '',
      action: '',
      details: '',
      constraints: '',
      format: '',
      structure: '',
      unwantedResult: ''
    });
    setShowPreview(false);
  };

  const fields = [
    {
      key: 'domain',
      title: 'Domain',
      placeholder: '例如：digital marketing, machine learning, financial planning, software development...',
      description: '定義主要專業領域',
      section: 'Role'
    },
    {
      key: 'specialization',
      title: 'Specialization',
      placeholder: '例如：brand strategy and social media, deep learning and NLP, investment analysis, full-stack web development...',
      description: '定義具體專精項目',
      section: 'Role'
    },
    {
      key: 'specificGoal',
      title: 'Specific Goal',
      placeholder: '例如：create a comprehensive social media marketing strategy for a tech startup, analyze customer behavior patterns from sales data...',
      description: '明確描述具體目標',
      section: 'Task'
    },
    {
      key: 'action',
      title: 'Action',
      placeholder: '例如：market research for social media trends, customer segmentation analysis, competitive analysis...',
      description: '定義需要執行的具體行動',
      section: 'Action'
    },
    {
      key: 'details',
      title: 'Context Details',
      placeholder: '例如：Target audience: young professionals aged 25-35, Budget: $50k monthly, Industry: B2B SaaS...',
      description: '提供背景資訊和重要細節',
      section: 'Context'
    },
    {
      key: 'constraints',
      title: 'Constraints',
      placeholder: '例如：Must comply with GDPR regulations, Limited to organic social media only, No budget for paid advertising...',
      description: '說明限制條件和約束',
      section: 'Context'
    },
    {
      key: 'format',
      title: 'Output Format',
      placeholder: '例如：markdown, JSON, PDF report, Excel spreadsheet...',
      description: '指定輸出檔案格式',
      section: 'Output'
    },
    {
      key: 'structure',
      title: 'Structure',
      placeholder: '例如：{title, executive_summary, analysis, recommendations, timeline}, {headers: [], data: [], charts: []}...',
      description: '定義輸出結構',
      section: 'Output'
    },
    {
      key: 'unwantedResult',
      title: 'Unwanted Result',
      placeholder: '例如：provide generic advice without specific data, include unverified claims, exceed 2000 words...',
      description: '明確不希望出現的結果',
      section: 'Output'
    }
  ];

  const sections = ['Role', 'Task', 'Action', 'Context', 'Output'];

  return (
    <div className="max-w-7xl mx-auto p-6 bg-gradient-to-br from-slate-50 to-blue-50 min-h-screen">
      <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
        {/* 標題區 */}
        <div className="bg-gradient-to-r from-slate-700 to-blue-700 text-white p-8">
          <h1 className="text-3xl font-bold mb-2">Structured Prompt Generator</h1>
          <p className="text-slate-200">基於標準化架構的 AI 提示詞生成器</p>
        </div>

        <div className="p-8">
          <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
            {/* 表單區域 - 左側 2/3 */}
            <div className="xl:col-span-2 space-y-6">
              <h2 className="text-2xl font-semibold text-gray-800 mb-6">填入參數</h2>
              
              {sections.map((section) => (
                <div key={section} className="bg-gray-50 rounded-xl p-6 border border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                    <span className="bg-blue-500 text-white px-3 py-1 rounded-full text-sm mr-3">
                      {section}
                    </span>
                    {section} 參數
                  </h3>
                  
                  <div className="space-y-4">
                    {fields.filter(field => field.section === section).map((field) => (
                      <div key={field.key}>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          {field.title}
                        </label>
                        <p className="text-xs text-gray-500 mb-2">{field.description}</p>
                        <textarea
                          value={formData[field.key]}
                          onChange={(e) => handleInputChange(field.key, e.target.value)}
                          placeholder={field.placeholder}
                          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none text-sm"
                          rows={3}
                        />
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            {/* 預覽區域 - 右側 1/3 */}
            <div className="xl:col-span-1">
              <div className="sticky top-8 bg-gray-50 rounded-xl p-6 border border-gray-200">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-semibold text-gray-800">生成預覽</h2>
                  <button
                    onClick={() => setShowPreview(!showPreview)}
                    className="flex items-center gap-2 px-3 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors text-sm"
                  >
                    {showPreview ? <EyeOff size={14} /> : <Eye size={14} />}
                    {showPreview ? '隱藏' : '顯示'}
                  </button>
                </div>
                
                {showPreview && (
                  <div className="bg-white rounded-lg border border-gray-200 p-4 max-h-96 overflow-y-auto mb-4">
                    <pre className="text-xs text-gray-700 whitespace-pre-wrap font-mono">
                      {generatePrompt()}
                    </pre>
                  </div>
                )}

                {/* 操作按鈕 */}
                <div className="space-y-2">
                  <button
                    onClick={copyToClipboard}
                    className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors text-sm"
                  >
                    <Copy size={14} />
                    {copied ? '已複製!' : '複製 Prompt'}
                  </button>
                  
                  <button
                    onClick={downloadPrompt}
                    className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors text-sm"
                  >
                    <Download size={14} />
                    下載檔案
                  </button>
                  
                  <button
                    onClick={resetForm}
                    className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors text-sm"
                  >
                    <RefreshCw size={14} />
                    重置
                  </button>
                </div>

                {/* 架構說明 */}
                <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                  <h3 className="font-semibold text-blue-800 mb-2 text-sm">📋 架構說明</h3>
                  <div className="text-xs text-blue-700 space-y-1">
                    <p><strong>Role:</strong> 定義專業領域和專精項目</p>
                    <p><strong>Task:</strong> 明確說明要完成的具體任務</p>
                    <p><strong>Action:</strong> 指定需要執行的搜尋或分析動作</p>
                    <p><strong>Context:</strong> 提供背景資訊和限制條件</p>
                    <p><strong>Output:</strong> 規範輸出格式和避免的結果</p>
                  </div>
                </div>

                {/* 使用提示 */}
                <div className="mt-4 p-4 bg-amber-50 border border-amber-200 rounded-lg">
                  <h3 className="font-semibold text-amber-800 mb-2 text-sm">💡 使用提示</h3>
                  <ul className="text-xs text-amber-700 space-y-1">
                    <li>• 所有欄位都是選填</li>
                    <li>• 建議至少填寫 Domain 和 Task</li>
                    <li>• 未填寫的欄位會保持 {`{placeholder}`} 格式</li>
                    <li>• Domain 和 Specialization 現在分開填寫</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PromptEngineeringGenerator;