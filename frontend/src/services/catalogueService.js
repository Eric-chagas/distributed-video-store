import axios from 'axios'

const API_URL = 'http://localhost:8000/grpc/api/movies'

export async function getMovies({ movie_id }) {
  const url = `${API_URL}/${movie_id}`
  const res = await axios.get(url)
  return res.data
}
