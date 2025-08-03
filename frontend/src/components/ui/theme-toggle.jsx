import { Palette } from "lucide-react"
import { useTheme } from "@/components/theme-provider"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

export function ThemeToggle() {
  const { setTheme } = useTheme()

  const allThemes = [
    { value: "light", colors: ["#ffffff", "#f8fafc"] },
    { value: "gray", colors: ["#d1d5db", "#9ca3af"] },
    { value: "rose-pastel", colors: ["#fce7f3", "#f9a8d4"] },
    { value: "blue-pastel", colors: ["#dbeafe", "#93c5fd"] },
    { value: "green-pastel", colors: ["#dcfce7", "#86efac"] },
    { value: "lavender-pastel", colors: ["#e9d5ff", "#c4b5fd"] },
    { value: "peach-pastel", colors: ["#fed7aa", "#fdba74"] },
    { value: "mint-pastel", colors: ["#d1fae5", "#6ee7b7"] },
    { value: "yellow-pastel", colors: ["#fef3c7", "#fde047"] },
    { value: "coral-pastel", colors: ["#fecaca", "#f87171"] },
    { value: "lilac-pastel", colors: ["#f3e8ff", "#d8b4fe"] },
    { value: "cyan-pastel", colors: ["#cffafe", "#67e8f9"] },
    { value: "salmon-pastel", colors: ["#fde2e7", "#fda4af"] },
    { value: "dark", colors: ["#1f2937", "#374151"] },
    { value: "violet-dark", colors: ["#2d1b69", "#5b21b6"] },
    { value: "blue-dark", colors: ["#1e3a8a", "#3730a3"] },
    { value: "green-dark", colors: ["#14532d", "#166534"] },
    { value: "red-dark", colors: ["#7f1d1d", "#991b1b"] },
    { value: "orange-dark", colors: ["#9a3412", "#c2410c"] },
    { value: "indigo-dark", colors: ["#312e81", "#4338ca"] },
    { value: "teal-dark", colors: ["#134e4a", "#0f766e"] },
    { value: "magenta-dark", colors: ["#831843", "#be185d"] },
    { value: "purple-dark", colors: ["#581c87", "#7c3aed"] },
    { value: "emerald-dark", colors: ["#064e3b", "#059669"] },
  ]

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" size="icon">
          <div className="relative h-[1.2rem] w-[1.2rem]">
            <div className="absolute inset-0 grid grid-cols-2 grid-rows-2 gap-0.5 rounded-sm overflow-hidden">
              <div className="bg-red-400"></div>
              <div className="bg-blue-400"></div>
              <div className="bg-green-400"></div>
              <div className="bg-yellow-400"></div>
            </div>
          </div>
          <span className="sr-only">Alternar tema</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-48 max-h-80 overflow-y-auto">
        <div className="grid grid-cols-4 gap-2 p-2">
          {allThemes.map((theme) => (
            <button
              key={theme.value}
              onClick={() => setTheme(theme.value)}
              className="relative h-8 w-8 rounded-md border border-gray-200 hover:border-gray-400 transition-colors overflow-hidden"
              title={theme.value}
            >
              <div className="absolute inset-0 flex">
                <div 
                  className="w-1/2 h-full" 
                  style={{ backgroundColor: theme.colors[0] }}
                ></div>
                <div 
                  className="w-1/2 h-full" 
                  style={{ backgroundColor: theme.colors[1] }}
                ></div>
              </div>
            </button>
          ))}
        </div>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}