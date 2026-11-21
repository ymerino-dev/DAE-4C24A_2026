import Header from './components/Header/Header.jsx'
import Hero from './components/Hero/Hero.jsx'
import MovieList from './components/MovieList/MovieList.jsx'
import Footer from './components/Footer/Footer.jsx'
import movies from './data/movies.js'

function App() {
  return (
    <>
      <Header />

      <main id="home">
        <Hero featuredMovie={movies[0]} />
        <MovieList movies={movies} />
      </main>

      <Footer />
    </>
  )
}

export default App
