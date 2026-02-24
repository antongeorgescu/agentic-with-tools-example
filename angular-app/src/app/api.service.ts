import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface QAPair {
  question: string;
  answer: string;
  tool_used?: string;
  tool_description?: string;
}

export interface QAResponse {
  success: boolean;
  count: number;
  actual_count: number;
  tools_used: string[];
  result: {
    qa_pairs: QAPair[];
    tools_used: Set<string> | string[];
    tool_summary: any;
  };
}

export interface Tool {
  name: string;
  description: string;
}

export interface TopicsResponse {
  topics: string[];
}

export interface ToolsResponse {
  tools: Tool[];
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:5000';

  constructor(private http: HttpClient) { }

  generateQAPairs(npairs: number): Observable<QAResponse> {
    return this.http.get<QAResponse>(`${this.baseUrl}/run_new_caller/${npairs}`);
  }

  getTopics(): Observable<TopicsResponse> {
    return this.http.get<TopicsResponse>(`${this.baseUrl}/run_new_caller/topics_list`);
  }

  getTools(): Observable<ToolsResponse> {
    return this.http.get<ToolsResponse>(`${this.baseUrl}/run_new_caller/tool_list`);
  }
}