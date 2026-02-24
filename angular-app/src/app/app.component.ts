import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService, QAPair, Tool } from './api.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'Q&A Generator App';
  
  // Data properties
  currentQAPair: QAPair = { question: '', answer: '' };
  topics: string[] = [];
  tools: Tool[] = [];
  toolsUsed: string[] = [];
  
  // Loading states
  isLoading = false;
  error: string | null = null;

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadInitialData();
    this.runGeneration();
  }

  loadInitialData() {
    // Load topics list
    this.apiService.getTopics().subscribe({
      next: (response) => {
        this.topics = response.topics;
      },
      error: (err) => {
        console.error('Error loading topics:', err);
        this.error = 'Failed to load topics';
      }
    });

    // Load tools list
    this.apiService.getTools().subscribe({
      next: (response) => {
        this.tools = response.tools;
      },
      error: (err) => {
        console.error('Error loading tools:', err);
        this.error = 'Failed to load tools';
      }
    });
  }

  runGeneration() {
    this.isLoading = true;
    this.error = null;
    
    this.apiService.generateQAPairs(1).subscribe({
      next: (response) => {
        if (response.result && response.result.qa_pairs && response.result.qa_pairs.length > 0) {
          this.currentQAPair = response.result.qa_pairs[0];
          
          // Convert tools_used to array if it's a Set
          if (response.tools_used) {
            this.toolsUsed = response.tools_used;
          } else if (response.result.tools_used) {
            this.toolsUsed = Array.isArray(response.result.tools_used) 
              ? response.result.tools_used 
              : Array.from(response.result.tools_used as any);
          }
        }
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Error generating Q&A pairs:', err);
        this.error = 'Failed to generate Q&A pairs';
        this.isLoading = false;
      }
    });
  }

  onRunClick() {
    this.runGeneration();
  }

  getToolDescription(toolName: string): string {
    const tool = this.tools.find(t => t.name === toolName);
    return tool ? tool.description : toolName;
  }
}