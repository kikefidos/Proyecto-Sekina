'use client'

import { useEffect, useState } from 'react'

export default function Courses() {
  const [courses, setCourses] = useState([])

  useEffect(() => {
    fetch('http://localhost:3001/courses')
      .then(res => res.json())
      .then(data => setCourses(data.slice(0, 3))) // Mostrar primeros 3
      .catch(err => console.error(err))
  }, [])

  return (
    <section className="container p-6">
      <h2 className="text-2xl font-bold mb-4">Cursos Destacados</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {courses.map((course) => (
          <div key={course.id} className="card">
            <h3 className="text-xl font-semibold mb-2">{course.title}</h3>
            <p className="text-sm text-gray-600 mb-3">{course.description}</p>
            <div className="flex justify-between items-center">
              <span className="text-xs text-gray-500">{course.level || 'Principiante'}</span>
              <a href={`/courses/${course.id}`} className="text-blue-600">Ver</a>
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}