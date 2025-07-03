import { useState, useEffect } from "react"
import { TooltipProvider } from "@/components/ui/tooltip"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent } from "@/components/ui/card"
import { TwentyFirstToolbar } from "@21st-extension/toolbar-react"
import { ReactPlugin } from "@21st-extension/react"
import { Pencil, Save, X } from "lucide-react"

interface ContentData {
  title: string
  description: string
}

function App() {
  const [content, setContent] = useState<ContentData>({
    title: "Go dev",
    description: "Добро пожаловать в мою простую CMS! Здесь вы можете редактировать любой текст."
  })
  
  const [editingTitle, setEditingTitle] = useState(false)
  const [editingDescription, setEditingDescription] = useState(false)
  const [tempTitle, setTempTitle] = useState("")
  const [tempDescription, setTempDescription] = useState("")

  // Загружаем данные из localStorage при монтировании
  useEffect(() => {
    const savedContent = localStorage.getItem('cms-content')
    if (savedContent) {
      setContent(JSON.parse(savedContent))
    }
  }, [])

  // Сохраняем данные в localStorage
  const saveToStorage = (newContent: ContentData) => {
    localStorage.setItem('cms-content', JSON.stringify(newContent))
  }

  const startEditingTitle = () => {
    setTempTitle(content.title)
    setEditingTitle(true)
  }

  const startEditingDescription = () => {
    setTempDescription(content.description)
    setEditingDescription(true)
  }

  const saveTitle = () => {
    const newContent = { ...content, title: tempTitle }
    setContent(newContent)
    saveToStorage(newContent)
    setEditingTitle(false)
  }

  const saveDescription = () => {
    const newContent = { ...content, description: tempDescription }
    setContent(newContent)
    saveToStorage(newContent)
    setEditingDescription(false)
  }

  const cancelTitleEdit = () => {
    setTempTitle("")
    setEditingTitle(false)
  }

  const cancelDescriptionEdit = () => {
    setTempDescription("")
    setEditingDescription(false)
  }

  return (
    <TooltipProvider>
      <TwentyFirstToolbar
        config={{
          plugins: [ReactPlugin],
        }}
      />
      <div className="min-h-screen bg-background flex items-center justify-center p-8">
        <Card className="w-full max-w-2xl">
          <CardContent className="p-8 space-y-8">
            
            {/* Редактируемый заголовок */}
            <div className="text-center">
              {editingTitle ? (
                <div className="space-y-4">
                  <Input
                    value={tempTitle}
                    onChange={(e) => setTempTitle(e.target.value)}
                    className="text-center text-4xl font-bold h-auto py-4"
                    placeholder="Введите заголовок"
                    autoFocus
                  />
                  <div className="flex justify-center gap-2">
                    <Button size="sm" onClick={saveTitle}>
                      <Save className="w-4 h-4 mr-2" />
                      Сохранить
                    </Button>
                    <Button size="sm" variant="outline" onClick={cancelTitleEdit}>
                      <X className="w-4 h-4 mr-2" />
                      Отменить
                    </Button>
                  </div>
                </div>
              ) : (
                <div className="group relative">
                  <h1 className="text-4xl font-bold mb-2">{content.title}</h1>
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={startEditingTitle}
                    className="opacity-0 group-hover:opacity-100 transition-opacity"
                  >
                    <Pencil className="w-4 h-4 mr-2" />
                    Редактировать заголовок
                  </Button>
                </div>
              )}
            </div>

            {/* Редактируемое описание */}
            <div className="text-center">
              {editingDescription ? (
                <div className="space-y-4">
                  <Textarea
                    value={tempDescription}
                    onChange={(e) => setTempDescription(e.target.value)}
                    className="text-center resize-none"
                    rows={4}
                    placeholder="Введите описание"
                    autoFocus
                  />
                  <div className="flex justify-center gap-2">
                    <Button size="sm" onClick={saveDescription}>
                      <Save className="w-4 h-4 mr-2" />
                      Сохранить
                    </Button>
                    <Button size="sm" variant="outline" onClick={cancelDescriptionEdit}>
                      <X className="w-4 h-4 mr-2" />
                      Отменить
                    </Button>
                  </div>
                </div>
              ) : (
                <div className="group relative">
                  <p className="text-lg text-muted-foreground mb-4 leading-relaxed">
                    {content.description}
                  </p>
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={startEditingDescription}
                    className="opacity-0 group-hover:opacity-100 transition-opacity"
                  >
                    <Pencil className="w-4 h-4 mr-2" />
                    Редактировать описание
                  </Button>
                </div>
              )}
            </div>

            {/* Информация о CMS */}
            <div className="text-center pt-8 border-t">
              <p className="text-sm text-muted-foreground">
                Простая CMS - наведите на текст для редактирования
              </p>
              <p className="text-xs text-muted-foreground mt-2">
                Все изменения автоматически сохраняются в браузере
              </p>
            </div>

          </CardContent>
        </Card>
      </div>
    </TooltipProvider>
  )
}

export default App