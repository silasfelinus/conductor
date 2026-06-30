import { extractControlBlock, readRoadmap } from '../../utils/repo'

export default defineEventHandler((event) => {
  try {
    const slug = getRouterParam(event, 'slug')
    if (!slug) {
      setResponseStatus(event, 400)
      return { success: false, message: 'Project slug is required', statusCode: 400 }
    }

    const roadmap = readRoadmap(slug)
    return {
      success: true,
      data: {
        slug,
        controlDirection: extractControlBlock(slug),
        roadmap,
        milestones: roadmap.milestones ?? [],
        tasks: roadmap.tasks ?? [],
      },
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Unable to load project'
    setResponseStatus(event, 500)
    return { success: false, message, statusCode: 500 }
  }
})
