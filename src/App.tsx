import { TooltipProvider } from "@/components/ui/tooltip"
import { TwentyFirstToolbar } from "@21st-extension/toolbar-react"
import { ReactPlugin } from "@21st-extension/react"
import { StoryblokContent } from "@/components/StoryblokContent"

function App() {
  return (
    <TooltipProvider>
      <TwentyFirstToolbar
        config={{
          plugins: [ReactPlugin],
        }}
      />
      <div className="min-h-screen bg-background flex items-center justify-center p-8">
        <StoryblokContent />
      </div>
    </TooltipProvider>
  )
}

export default App