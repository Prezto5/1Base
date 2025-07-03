import { storyblokInit, apiPlugin } from '@storyblok/react'

export const storyblokConfig = storyblokInit({
  accessToken: import.meta.env.VITE_STORYBLOK_ACCESS_TOKEN,
  use: [apiPlugin],
  apiOptions: {
    region: 'eu' // или 'us' в зависимости от региона
  }
})

export default storyblokConfig 