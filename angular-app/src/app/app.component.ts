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
              <span class="topic-badge">Topic: {{ qa.topic }}</span>
            </div>
            <div class="qa-content">
              <div class="question-section">
                <label>Question:</label>
                <textarea readonly class="question-box">{{ qa.question }}</textarea>
              </div>
              <div class="answer-section">
                <label>Answer:</label>
                <textarea readonly class="answer-box">{{ qa.answer }}</textarea>
              </div>
              <div class="tool-info" *ngIf="qa.tool_used">
                <strong>Tool:</strong><span style="color: red;"> {{ qa.tool_used }}</span>&nbsp;<strong>Description:</strong> {{ qa.description }}
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
      background: #6f42c1;
      color: white;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 0.8em;
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
      min-height: 80px;
      background: white;
      font-family: inherit;
    }
    
    .question-box {
      border-left: 4px solid #007bff;
    }
    
    .answer-box {
      border-left: 4px solid #28a745;
    }
    
    .tool-info {
      grid-column: 1 / -1;
      color: #6c757d;
      font-style: italic;
      margin-top: 10px;
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
}