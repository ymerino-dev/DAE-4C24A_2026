import { BrowserRouter, Route, Routes } from 'react-router-dom';

import MovieForm from './components/MovieForm/MovieForm';
import MovieList from './components/MovieList/MovieList';
import NavBar from './components/NavBar/NavBar';

function App() {
  return (
    <BrowserRouter>
      <NavBar />
      <main className="app-main">
        <Routes>
          <Route path="/" element={<MovieList />} />
          <Route path="/create" element={<MovieForm />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;
