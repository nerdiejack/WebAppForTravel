// Cookie management utilities

export const getCookie = (name) => {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop().split(';').shift()
  return null
}

export const setCookie = (name, value, days = 365) => {
  const date = new Date()
  date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000))
  const expires = `expires=${date.toUTCString()}`
  document.cookie = `${name}=${value};${expires};path=/`
}

export const shouldShowIntro = () => {
  // Get the visit count
  let visitCount = parseInt(getCookie('visitCount')) || 0
  
  // Increment visit count
  visitCount++
  
  // Save the new visit count
  setCookie('visitCount', visitCount)
  
  // Show intro on first visit and when (visitCount - 1) is divisible by 15
  // This will show at visits: 1, 16, 31, 46, etc.
  return visitCount === 1 || (visitCount - 1) % 15 === 0
} 