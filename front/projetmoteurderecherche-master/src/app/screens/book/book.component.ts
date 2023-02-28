import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Detail } from '../../cores/detail';
import { LibraryServiceService } from '../../cores/services/library-service.service';


@Component({
  selector: 'app-book',
  templateUrl: './book.component.html',
  styleUrls: ['./book.component.css']
})
export class BookComponent {
  
  showModal = true;
  loading = false;
  book!: Detail;
  id: number = 0;

  constructor(private route: ActivatedRoute, public LibraryServiceService: LibraryServiceService) { }

  getDetails(){
    this.loading = true;
    this.route.params.subscribe(params => {
      this.id = params['id'];
      console.log('Parameter value:', this.id);
    });
  
    this.LibraryServiceService.getBookDetail(this.id).subscribe((res: Detail)=> {
      this.book=res;
      this.loading = false;
    }, (err) => {
      alert('failed loading detail');
    })
  }
  closeModal() {
    this.showModal = false;
  }

  ngOnInit(): void {
    this.getDetails();
  }

}