import { ThemeToggle } from "@/components/ui/theme-toggle"
import { TooltipProvider } from "@/components/ui/tooltip"
import { TwentyFirstToolbar } from "@21st-extension/toolbar-react"
import { ReactPlugin } from "@21st-extension/react"

function App() {
  return (
    <TooltipProvider>
      <TwentyFirstToolbar
        config={{
          plugins: [ReactPlugin],
        }}
      />
      <div className="min-h-screen bg-background flex items-center justify-center p-8">
        <div className="fixed top-6 right-6">
          <ThemeToggle />
        </div>
        
        <div className="text-center">
          <h1 className="text-6xl font-bold">Go dev</h1>
        </div>
      </div>
    </TooltipProvider>
  )
}

export default App