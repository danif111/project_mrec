import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs'
import { Book } from '../book'; 
import { Detail } from '../detail';
import { Suggestion } from '../suggestion';

@Injectable({
  providedIn: 'root'
})
export class LibraryServiceService {

  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
    })
  };

  constructor(private http: HttpClient) { }
  port: string="http://127.0.0.1:8000";
  
  getLibraryJSON(): Observable<Book[]>{
    return this.http.get<Book[]>(this.port+"/books/", this.httpOptions);
    
  }

  getBookDetail(id: number): Observable<Detail>{
    return this.http.get<Detail>(this.port+"/book/"+id,this.httpOptions);
  }

  getSuggestionsJSON(search: String): Observable<Suggestion>{
    return this.http.get<Suggestion>(this.port+"/suggest/word/"+search,this.httpOptions);
  }

  getWordJSON(search: String): Observable<Book[]>{
    return this.http.get<Book[]>(this.port+"/search/word/"+search,this.httpOptions);
  }

  getData(): Observable<Book[]> {
    return this.http.get<Book[]>('assets/library.json');
  }
}
