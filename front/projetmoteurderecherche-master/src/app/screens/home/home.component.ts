import { Component} from '@angular/core';
import { Book } from '../../cores/book';
import { Suggestion } from '../../cores/suggestion';
import { debounceTime } from 'rxjs/operators';
import { LibraryServiceService } from '../../cores/services/library-service.service';
import { BehaviorSubject } from 'rxjs';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})

export class HomeComponent {

  library: Book[]= [];
  filteredItems: Suggestion = {founded: [],similar:[]};
  searchSubject = new BehaviorSubject<string>('');
  showAutoComplete: boolean = false;

  constructor(public LibraryServiceService: LibraryServiceService) { }

  onKeyUp(event: KeyboardEvent) {
    const searchValue = (event.target as HTMLInputElement).value;
    this.searchSubject.next(searchValue);
  }

  suggestion() {
    const searchTerm = this.searchSubject.getValue();
    const lowercaseQuery = searchTerm.toLowerCase();
    if(lowercaseQuery !== "") {
      this.LibraryServiceService.getSuggestionsJSON(lowercaseQuery).subscribe((res: Suggestion)=> {
        this.filteredItems=res;
        this.showAutoComplete = true;
      }, (err) => {
        alert('failed loading suggestions');
      })
    }
    
  }


  research(searchTerm: string){
    this.LibraryServiceService.getWordJSON(searchTerm).subscribe((res: Book[])=> {
      this.library=res;
      this.showAutoComplete = false;
    }, (err) => {
      alert('failed research');
    })
  }



  getLibrary(){
    this.LibraryServiceService.getLibraryJSON().subscribe((res: Book[])=> {
      this.library=res;
    }, (err) => {
      alert('failed loading Books');
    })
  }

  ngOnInit(): void {
    this.getLibrary();

    this.searchSubject
      .pipe(debounceTime(3000))
      .subscribe(() => {
        this.suggestion(); // Call your function here
    });
  }

}


