import { useStoryblok, StoryblokComponent } from "@storyblok/react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useEffect } from "react"

interface StoryblokContentProps {
  slug?: string
}

export function StoryblokContent({ slug = 'home' }: StoryblokContentProps) {
  const story = useStoryblok(slug, { version: "draft" })

  useEffect(() => {
    // Инициализация Storyblok
    import("@/lib/storyblok")
  }, [])

  if (!story || !story.content) {
    return (
      <Card className="w-full max-w-2xl mt-6">
        <CardHeader>
          <CardTitle>Storyblok Content</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">Loading content from Storyblok...</p>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="w-full max-w-2xl mt-6">
      <CardHeader>
        <CardTitle>Storyblok Content</CardTitle>
      </CardHeader>
      <CardContent>
        <StoryblokComponent blok={story.content} />
      </CardContent>
    </Card>
  )
} 