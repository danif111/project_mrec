import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BookComponent } from './screens/book/book.component';
import { HomeComponent } from './screens/home/home.component';

const routes: Routes = [
  {
    path: '', component : HomeComponent,
  },
  {
    path: 'book/:id', component: BookComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
