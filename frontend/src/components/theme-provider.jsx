import { createContext, useContext, useEffect, useState } from "react"

const ThemeProviderContext = createContext({
  theme: "system",
  setTheme: () => null,
})

export function ThemeProvider({
  children,
  defaultTheme = "system",
  storageKey = "vite-ui-theme",
  ...props
}) {
  const [theme, setTheme] = useState(
    () => localStorage.getItem(storageKey) || defaultTheme
  )

  useEffect(() => {
    const root = window.document.documentElement

    // Remove todas as classes de tema
    root.classList.remove(
      "light", "dark", "rose-pastel", "blue-pastel", "green-pastel", 
      "lavender-pastel", "peach-pastel", "mint-pastel", "yellow-pastel", 
      "coral-pastel", "lilac-pastel", "cyan-pastel", "salmon-pastel",
      "gray", "violet-dark", "blue-dark", "green-dark", "red-dark", "orange-dark",
      "indigo-dark", "teal-dark", "magenta-dark", "purple-dark", "emerald-dark"
    )



    root.classList.add(theme)
  }, [theme])

  const value = {
    theme,
    setTheme: (theme) => {
      localStorage.setItem(storageKey, theme)
      setTheme(theme)
    },
  }

  return (
    <ThemeProviderContext.Provider {...props} value={value}>
      {children}
    </ThemeProviderContext.Provider>
  )
}

export const useTheme = () => {
  const context = useContext(ThemeProviderContext)

  if (context === undefined)
    throw new Error("useTheme must be used within a ThemeProvider")

  return context
}