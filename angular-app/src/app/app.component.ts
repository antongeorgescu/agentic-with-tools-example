import { Component, inject } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule],
  template: `
    <div class="qa-generator-app">
      <header class="app-header">
        <h1>🚀 Q&A Generator App</h1>
        <div class="controls">
          <label for="npairs">Number of Q&A pairs:</label>
          <input type="number" id="npairs" [(ngModel)]="npairs" min="1" max="10" />
          <button class="run-button" (click)="runGenerator()" [disabled]="isLoading">
            {{ isLoading ? 'Generating...' : 'Run Generator' }}
          </button>
          <button class="list-button" (click)="listTopics()">
            List Topics
          </button>
          <button class="list-button" (click)="listTools()">
            List Tools
          </button>
        </div>
      </header>

      <div *ngIf="error" class="error-message">
        <strong>Error:</strong> {{ error }}
      </div>

      <div *ngIf="isLoading" class="loading-message">
        <p>🔄 Calling Flask API to generate {{ npairs }} Q&A pairs...</p>
      </div>

      <!-- Top Layer: Q&A Pairs -->
      <section class="qa-section" *ngIf="qaResults.length > 0">
        <h2>📝 Generated Q&A Pairs ({{ qaResults.length }})</h2>
        <div class="qa-grid">
          <div class="qa-pair" *ngFor="let qa of qaResults; let i = index">
            <div class="qa-header">
              <strong>Pair {{ i + 1 }}</strong>
              <span class="sin-badge" *ngIf="qa.sin_number && qa.sin_number !== 'N/A'">SIN: {{ qa.sin_number }}</span>
              <span class="topic-badge"><span class="topic-num">Topic #{{ qa.topic_index }}</span><span class="topic-desc">{{ qa.topic }}</span></span>
            </div>
            <div class="qa-content">
              <div class="question-section">
                <label>Question:</label>
                <div class="question-display">
                  <ng-container *ngFor="let part of getQuestionParts(qa.question)">
                    <span [class]="part.isSin ? 'sin-highlight' : 'regular-text'">{{ part.text }}</span>
                  </ng-container>
                </div>
              </div>
              <div class="answer-section">
                <label>Answer:</label>
                <div class="answer-display">
                  <ng-container *ngFor="let answerPart of getAnswerParts(qa.answer)">
                    <span [class]="answerPart.isSin ? 'sin-highlight' : answerPart.isAccountInfo ? 'account-info-text' : 'regular-text'">{{ answerPart.text }}</span>
                  </ng-container>
                </div>
              </div>
              <div class="tool-info" *ngIf="qa.tool_used">
                <div class="tool-details">
                  <div><strong>Tool:</strong> <span class="tool-name">{{ qa.tool_used }}</span></div>
                  <div><strong>Description:</strong> {{ qa.description }}</div>
                  <div *ngIf="qa.tool_return" class="tool-return">
                    <strong>Tool Result:</strong> <span class="tool-result">{{ qa.tool_return }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Middle Layer: Topics List -->
      <section class="topics-section" *ngIf="topicsUsed.length > 0">
        <h2>🎯 Topics Used ({{ topicsUsed.length }})</h2>
        <div class="topics-grid">
          <div class="topic-card" *ngFor="let topic of topicsUsed">
            <span class="topic-name">{{ topic }}</span>
          </div>
        </div>
      </section>

      <!-- Bottom Layer: Tools Used -->
      <section class="tools-section" *ngIf="toolsUsed.length > 0">
        <h2>🔧 Tools Used ({{ toolsUsed.length }})</h2>
        <div class="tools-grid">
          <div class="tool-card" *ngFor="let tool of toolsUsed">
            <div class="tool-name">{{ tool }}</div>
            <div class="tool-count" *ngIf="toolUsageCount[tool]">
              Used {{ toolUsageCount[tool] }} times
            </div>
          </div>
        </div>
      </section>

      <div *ngIf="!qaResults.length && !isLoading && !error" class="welcome-message">
        <p>👋 Welcome! Click "Run Generator" to generate Q&A pairs using the Flask API.</p>
      </div>
    </div>
  `,
  styles: [`
    .qa-generator-app {
      padding: 20px;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      max-width: 1200px;
      margin: 0 auto;
    }
    
    .app-header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 20px;
      border-radius: 8px;
      margin-bottom: 20px;
    }
    
    .app-header h1 {
      margin: 0 0 15px 0;
      font-size: 2em;
    }
    
    .controls {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }
    
    .controls input {
      padding: 8px;
      border: none;
      border-radius: 4px;
      width: 80px;
    }
    
    .run-button {
      background: #28a745;
      color: white;
      border: none;
      padding: 10px 20px;
      border-radius: 4px;
      cursor: pointer;
      font-size: 16px;
      font-weight: bold;
    }
    
    .run-button:hover:not(:disabled) {
      background: #218838;
    }
    
    .run-button:disabled {
      background: #6c757d;
      cursor: not-allowed;
    }
    
    .list-button {
      background: #6f42c1;
      color: white;
      border: none;
      padding: 10px 15px;
      border-radius: 4px;
      cursor: pointer;
      font-size: 14px;
      margin-left: 10px;
    }
    
    .list-button:hover {
      background: #5a359c;
    }
    
    .qa-section, .topics-section, .tools-section {
      margin-bottom: 30px;
      background: white;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .qa-section h2 {
      color: #2c5aa0;
      border-bottom: 2px solid #e9ecef;
      padding-bottom: 10px;
    }
    
    .topics-section h2 {
      color: #6f42c1;
      border-bottom: 2px solid #e9ecef;
      padding-bottom: 10px;
    }
    
    .tools-section h2 {
      color: #e83e8c;
      border-bottom: 2px solid #e9ecef;
      padding-bottom: 10px;
    }
    
    .qa-grid {
      display: grid;
      gap: 20px;
    }
    
    .qa-pair {
      border: 1px solid #dee2e6;
      border-radius: 6px;
      padding: 15px;
      background: #f8f9fa;
    }
    
    .qa-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 15px;
    }
    
    .topic-badge {
      display: inline-flex;
      align-items: baseline;
      gap: 6px;
      background: #6f42c1;
      color: white;
      padding: 4px 10px;
      border-radius: 4px;
      font-size: 0.8em;
      max-width: 100%;
      flex-wrap: wrap;
    }
    .topic-num {
      font-weight: 700;
      white-space: nowrap;
      flex-shrink: 0;
    }
    .topic-desc {
      font-weight: 400;
      opacity: 0.88;
    }

    .sin-badge {
      background: #856404;
      color: #fff3cd;
      padding: 4px 10px;
      border-radius: 4px;
      font-size: 0.85em;
      font-weight: 700;
      letter-spacing: 0.05em;
      border: 1px solid #ffc107;
    }
    
    .qa-content {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 15px;
    }
    
    @media (max-width: 768px) {
      .qa-content {
        grid-template-columns: 1fr;
      }
    }
    
    .question-section, .answer-section {
      display: flex;
      flex-direction: column;
    }
    
    .question-section label, .answer-section label {
      font-weight: bold;
      margin-bottom: 5px;
      color: #495057;
    }
    
    .question-box, .answer-box {
      padding: 10px;
      border: 1px solid #ced4da;
      border-radius: 4px;
      resize: vertical;
      min-height: 120px;
      background: white;
      font-family: inherit;
      font-size: 14px;
    }
    
    .question-box {
      border-left: 4px solid #007bff;
    }
    
    .answer-box {
      border-left: 4px solid #28a745;
    }

    .question-display {
      padding: 10px;
      border: 1px solid #ced4da;
      border-radius: 4px;
      min-height: 120px;
      background: white;
      font-family: inherit;
      font-size: 14px;
      border-left: 4px solid #007bff;
      white-space: pre-wrap;
      word-wrap: break-word;
    }

    .sin-highlight {
      background: #fff3cd;
      color: #856404;
      font-weight: 700;
      border-radius: 3px;
      padding: 0 2px;
    }

    .answer-display {
      padding: 10px;
      border: 1px solid #ced4da;
      border-radius: 4px;
      min-height: 120px;
      background: white;
      font-family: inherit;
      font-size: 14px;
      border-left: 4px solid #28a745;
      white-space: pre-wrap;
      word-wrap: break-word;
    }

    .account-info-text {
      color: #007bff;
      font-weight: 600;
    }

    .regular-text {
      color: #495057;
    }

    .tool-info {
      grid-column: 1 / -1;
      margin-top: 10px;
      background: #f8f9fa;
      padding: 10px;
      border-radius: 4px;
      border-left: 4px solid #6c757d;
    }
    
    .tool-details {
      font-size: 0.9em;
    }
    
    .tool-details > div {
      margin-bottom: 4px;
    }
    
    .tool-name {
      color: #dc3545;
      font-weight: bold;
    }
    
    .tool-return {
      margin-top: 8px;
      padding-top: 8px;
      border-top: 1px solid #dee2e6;
    }
    
    .tool-result {
      color: #2f06e6;
      font-weight: normal;
      font-style: normal;
    }
    
    .topics-grid, .tools-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 10px;
    }
    
    .topic-card {
      background: #e7e3ff;
      border: 1px solid #6f42c1;
      border-radius: 4px;
      padding: 10px;
      text-align: center;
    }
    
    .topic-name {
      font-weight: bold;
      color: #6f42c1;
    }
    
    .tool-card {
      background: #ffe3f1;
      border: 1px solid #e83e8c;
      border-radius: 4px;
      padding: 10px;
      text-align: center;
    }
    
    .tool-name {
      font-weight: bold;
      color: #e83e8c;
      margin-bottom: 5px;
    }
    
    .tool-count {
      font-size: 0.8em;
      color: #6c757d;
    }
    
    .loading-message, .welcome-message {
      text-align: center;
      padding: 40px;
      color: #6c757d;
      font-size: 1.1em;
    }
    
    .error-message {
      background: #f8d7da;
      color: #721c24;
      padding: 15px;
      border: 1px solid #f5c6cb;
      border-radius: 4px;
      margin-bottom: 20px;
    }
  `]
})
export class AppComponent {
  private http = inject(HttpClient);
  
  title = 'Q&A Generator App';
  npairs = 1;
  isLoading = false;
  error = '';
  
  qaResults: any[] = [];
  topicsUsed: string[] = [];
  toolsUsed: string[] = [];
  toolUsageCount: { [key: string]: number } = {};
  
  constructor() {
    console.log('Q&A Generator App initialized');
  }
  
  async runGenerator() {
    if (this.npairs < 1 || this.npairs > 10) {
      this.error = 'Number of pairs must be between 1 and 10';
      return;
    }
    
    this.isLoading = true;
    this.error = '';
    this.qaResults = [];
    this.topicsUsed = [];
    this.toolsUsed = [];
    this.toolUsageCount = {};
    
    try {
      console.log(`Calling Flask API: localhost:5000/run_new_caller/${this.npairs}`);
      
      const response = await this.http.get<any>(`http://localhost:5000/run_new_caller/${this.npairs}`).toPromise();
      
      console.log('Flask API Response:', response);
      
      if (response?.success && response?.result) {
        // Extract Q&A pairs
        this.qaResults = response.result.qa_pairs || [];
        
        // Extract unique topics from Q&A pairs
        const topicsSet = new Set<string>();
        this.qaResults.forEach(qa => {
          if (qa.topic) {
            topicsSet.add(qa.topic);
          }
        });
        this.topicsUsed = Array.from(topicsSet);
        
        // Extract tools used
        this.toolsUsed = response.result.tools_used || response.tools_used || [];
        
        // Extract tool usage count
        if (response.result.tool_summary?.tool_usage_count) {
          this.toolUsageCount = response.result.tool_summary.tool_usage_count;
        }
        
        console.log(`Successfully generated ${this.qaResults.length} Q&A pairs`);
        console.log(`Topics used: ${this.topicsUsed.length}`);
        console.log(`Tools used: ${this.toolsUsed.length}`);
        
      } else {
        this.error = response?.error || 'Unexpected response format from Flask API';
      }
      
    } catch (error: any) {
      console.error('Error calling Flask API:', error);
      
      if (error.status === 0) {
        this.error = 'Cannot connect to Flask API at localhost:5000. Please make sure the Flask server is running.';
      } else if (error.error?.error) {
        this.error = `API Error: ${error.error.error}`;
      } else {
        this.error = `Network error: ${error.message || 'Unknown error occurred'}`;
      }
    } finally {
      this.isLoading = false;
    }
  }

  private readonly SIN_PATTERN = /\b(\d{3}-\d{3}-\d{3})\b/g;

  /** Split text into segments, flagging SIN numbers for highlighting. */
  private splitBySin(text: string): { text: string; isSin: boolean; isAccountInfo: boolean }[] {
    const result: { text: string; isSin: boolean; isAccountInfo: boolean }[] = [];
    let lastIndex = 0;
    let match: RegExpExecArray | null;
    this.SIN_PATTERN.lastIndex = 0;
    while ((match = this.SIN_PATTERN.exec(text)) !== null) {
      if (match.index > lastIndex) {
        result.push({ text: text.slice(lastIndex, match.index), isSin: false, isAccountInfo: false });
      }
      result.push({ text: match[0], isSin: true, isAccountInfo: false });
      lastIndex = match.index + match[0].length;
    }
    if (lastIndex < text.length) {
      result.push({ text: text.slice(lastIndex), isSin: false, isAccountInfo: false });
    }
    return result;
  }

  getQuestionParts(question: string): { text: string; isSin: boolean; isAccountInfo: boolean }[] {
    if (!question) return [{ text: '', isSin: false, isAccountInfo: false }];
    return this.splitBySin(question);
  }

  getAnswerParts(answer: string): { text: string; isSin: boolean; isAccountInfo: boolean }[] {
    if (!answer) return [{ text: '', isSin: false, isAccountInfo: false }];

    const result: { text: string; isSin: boolean; isAccountInfo: boolean }[] = [];

    // Unified answer format: intro sentence | findings section | closing sentence
    const findingsMarker = 'here is a comprehensive overview of the findings:';
    const closingMarker = 'Please do not hesitate';

    const findingsIdx = answer.indexOf(findingsMarker);

    if (findingsIdx === -1) {
      // Fallback for legacy / plain-text answers — just highlight SINs
      return this.splitBySin(answer);
    }

    const introText   = answer.slice(0, findingsIdx + findingsMarker.length);
    const remainder   = answer.slice(findingsIdx + findingsMarker.length);
    const closingIdx  = remainder.indexOf(closingMarker);
    const findingsText = closingIdx !== -1 ? remainder.slice(0, closingIdx) : remainder;
    const closingText  = closingIdx !== -1 ? remainder.slice(closingIdx) : '';

    // Intro — regular styling with SIN highlighting
    result.push(...this.splitBySin(introText));

    // Findings — account-info styling (blue/bold) with SIN highlighting
    let lastIndex = 0;
    let match: RegExpExecArray | null;
    this.SIN_PATTERN.lastIndex = 0;
    while ((match = this.SIN_PATTERN.exec(findingsText)) !== null) {
      if (match.index > lastIndex) {
        result.push({ text: findingsText.slice(lastIndex, match.index), isSin: false, isAccountInfo: true });
      }
      result.push({ text: match[0], isSin: true, isAccountInfo: true });
      lastIndex = match.index + match[0].length;
    }
    if (lastIndex < findingsText.length) {
      result.push({ text: findingsText.slice(lastIndex), isSin: false, isAccountInfo: true });
    }

    // Closing — regular styling with SIN highlighting
    if (closingText) {
      result.push(...this.splitBySin(closingText));
    }

    return result;
  }

  listTopics() {
    // Call Flask API to get topics
    this.http.get<any>('http://localhost:5000/run_new_caller/topics_list').subscribe({
      next: (response) => {
        // Open new window and display raw response
        const newWindow = window.open('', '_blank');
        if (newWindow) {
          const topics: string[] = response?.topics || [];
          const rows = topics
            .map((t: string, i: number) => `<tr><td class="idx">#${i + 1}</td><td>${t}</td></tr>`)
            .join('');
          newWindow.document.write(`
            <html>
              <head>
                <title>List Topics</title>
                <style>
                  body { font-family: 'Segoe UI', Arial, sans-serif; padding: 24px; background: #f5f5f5; }
                  h1 { font-size: 1.3em; margin-bottom: 16px; color: #4a2c8a; }
                  table { border-collapse: collapse; width: 100%; background: #fff; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,.1); }
                  th { background: #6f42c1; color: #fff; padding: 10px 14px; text-align: left; font-size: .9em; }
                  td { padding: 9px 14px; border-bottom: 1px solid #eee; font-size: .9em; vertical-align: top; }
                  td.idx { width: 60px; font-weight: 700; color: #6f42c1; white-space: nowrap; }
                  tr:last-child td { border-bottom: none; }
                  tr:hover td { background: #f3eeff; }
                </style>
              </head>
              <body>
                <h1>Topics List (${topics.length} topics)</h1>
                <table>
                  <thead><tr><th>#</th><th>Topic description</th></tr></thead>
                  <tbody>${rows}</tbody>
                </table>
              </body>
            </html>
          `);
          newWindow.document.close();
        }
      },
      error: (error) => {
        console.error('Error calling list_topics API:', error);
        // Open new window and display error
        const newWindow = window.open('', '_blank');
        if (newWindow) {
          newWindow.document.write(`
            <html>
              <head>
                <title>List Topics - Error</title>
                <style>
                  body {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                    background-color: #f8f9fa;
                  }
                  .error {
                    color: #dc3545;
                    background-color: #f8d7da;
                    border: 1px solid #f5c6cb;
                    padding: 15px;
                    border-radius: 4px;
                  }
                </style>
              </head>
              <body>
                <h1>List Topics - Error</h1>
                <div class="error">
                  <strong>Error:</strong> ${error.message || 'Failed to fetch topics'}
                  <br><br>
                  <strong>Status:</strong> ${error.status || 'Unknown'}
                  <br><br>
                  <strong>Details:</strong> ${JSON.stringify(error, null, 2)}
                </div>
              </body>
            </html>
          `);
          newWindow.document.close();
        }
      }
    });
  }

  listTools() {
    // Call Flask API to get tools
    this.http.get<any>('http://localhost:5000/run_new_caller/tool_list').subscribe({
      next: (response) => {
        // Open new window and display raw response
        const newWindow = window.open('', '_blank');
        if (newWindow) {
          newWindow.document.write(`
            <html>
              <head>
                <title>List Tools - Raw Response</title>
                <style>
                  body {
                    font-family: 'Courier New', monospace;
                    padding: 20px;
                    background-color: #f5f5f5;
                  }
                  pre {
                    background-color: #ffffff;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    padding: 15px;
                    overflow: auto;
                  }
                </style>
              </head>
              <body>
                <h1>List Tools - Raw Response</h1>
                <pre>${JSON.stringify(response, null, 2)}</pre>
              </body>
            </html>
          `);
          newWindow.document.close();
        }
      },
      error: (error) => {
        console.error('Error calling tool_list API:', error);
        // Open new window and display error
        const newWindow = window.open('', '_blank');
        if (newWindow) {
          newWindow.document.write(`
            <html>
              <head>
                <title>List Tools - Error</title>
                <style>
                  body {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                    background-color: #f8f9fa;
                  }
                  .error {
                    color: #dc3545;
                    background-color: #f8d7da;
                    border: 1px solid #f5c6cb;
                    padding: 15px;
                    border-radius: 4px;
                  }
                </style>
              </head>
              <body>
                <h1>List Tools - Error</h1>
                <div class="error">
                  <strong>Error:</strong> ${error.message || 'Failed to fetch tools'}
                  <br><br>
                  <strong>Status:</strong> ${error.status || 'Unknown'}
                  <br><br>
                  <strong>Details:</strong> ${JSON.stringify(error, null, 2)}
                </div>
              </body>
            </html>
          `);
          newWindow.document.close();
        }
      }
    });
  }
}