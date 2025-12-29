import Link from 'next/link'

export default function CourseCard({ course }) {
  return (
    <article className="border rounded p-4 shadow-sm hover:shadow-md transition">
      <h3 className="text-xl font-semibold mb-2">{course.title}</h3>
      <p className="text-sm text-gray-600 mb-3">{course.description}</p>
      <div className="flex justify-between items-center">
        <span className="text-xs text-gray-500">{course.level || 'Nivel básico'}</span>
        <Link href={`/courses/${course.id}`} className="text-blue-600">Ver curso</Link>
      </div>
    </article>
  )
}
