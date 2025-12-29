'use client'

export default function Spinner({ size = 6 }) {
  const sizeClass = size === 8 ? 'w-8 h-8' : size === 6 ? 'w-6 h-6' : 'w-4 h-4'
  return (
    <div className={`${sizeClass} inline-block animate-spin border-2 border-t-transparent rounded-full`} />
  )
}
