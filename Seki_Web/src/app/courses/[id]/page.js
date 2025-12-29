import { fetchCourseById } from '@/lib/api'

export default async function CourseDetail({ params }) {
  const { id } = params
  let course = null
  try {
    course = await fetchCourseById(id)
  } catch (e) {
    console.error(e)
  }

  if (!course) {
    return <div className="container mx-auto p-6">Curso no encontrado</div>
  }

  return (
    <main className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-4">{course.title}</h1>
      <p className="text-gray-700 mb-4">{course.description}</p>
      <section className="prose">
        <h2>Contenido</h2>
        <ul>
          {(course.lessons || []).map((l) => (
            <li key={l.id}>{l.title}</li>
          ))}
        </ul>
      </section>
    </main>
  )
}
