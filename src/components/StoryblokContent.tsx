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
      <Card className="w-full max-w-4xl">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl">Loading Storyblok Content...</CardTitle>
        </CardHeader>
        <CardContent className="text-center">
          <p className="text-muted-foreground">
            Загружаем контент из Storyblok CMS...
          </p>
          <p className="text-sm text-muted-foreground mt-4">
            Убедитесь, что API ключ правильно настроен в .env файле
          </p>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="w-full max-w-4xl">
      <StoryblokComponent blok={story.content} />
    </div>
  )
} 