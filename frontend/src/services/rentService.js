import axios from 'axios'

const API_URL = 'http://localhost:8000/grpc/api/rent/consult'

export async function consultRentStatus({ movie_id }) {
  const url = `${API_URL}/${movie_id}`
  const res = await axios.get(url)
  return res.data
}
