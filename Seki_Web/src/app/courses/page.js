import { fetchCourses } from '@/lib/api'
import CourseCard from '@/components/CourseCard'

export default async function CoursesPage() {
  let courses = []
  try {
    courses = await fetchCourses()
  } catch (e) {
    console.error(e)
  }

  return (
    <main className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Todos los cursos</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {courses.map((c) => (
          <CourseCard key={c.id} course={c} />
        ))}
      </div>
    </main>
  )
}
