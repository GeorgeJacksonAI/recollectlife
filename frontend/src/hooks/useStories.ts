import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';

export interface Story {
  id: number;
  title: string;
  description: string;
  created_at: string;
  updated_at: string;
  user_id: number;
}

interface CreateStoryDto {
  title: string;
  description?: string;
}

interface UpdateStoryDto {
  title?: string;
  description?: string;
}

// Fetch all stories for current user
export const useStories = () => {
  return useQuery({
    queryKey: ['stories'],
    queryFn: async () => {
      const response = await api.get<Story[]>('/api/stories/');
      return response.data;
    },
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
};

// Fetch single story by ID
export const useStory = (storyId: number | undefined) => {
  return useQuery({
    queryKey: ['stories', storyId],
    queryFn: async () => {
      const response = await api.get<Story>(`/api/stories/${storyId}`);
      return response.data;
    },
    enabled: !!storyId,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

// Create new story
export const useCreateStory = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: CreateStoryDto) => {
      const response = await api.post<Story>('/api/stories/', data);
      return response.data;
    },
    onSuccess: () => {
      // Invalidate stories list to refetch
      queryClient.invalidateQueries({ queryKey: ['stories'] });
    },
  });
};

// Update existing story
export const useUpdateStory = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, data }: { id: number; data: UpdateStoryDto }) => {
      const response = await api.put<Story>(`/api/stories/${id}`, data);
      return response.data;
    },
    onSuccess: (updatedStory) => {
      // Invalidate both list and individual story queries
      queryClient.invalidateQueries({ queryKey: ['stories'] });
      queryClient.invalidateQueries({ queryKey: ['stories', updatedStory.id] });
    },
  });
};

// Delete story
export const useDeleteStory = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: number) => {
      await api.delete(`/api/stories/${id}`);
      return id;
    },
    onSuccess: () => {
      // Invalidate stories list to refetch
      queryClient.invalidateQueries({ queryKey: ['stories'] });
    },
  });
};
